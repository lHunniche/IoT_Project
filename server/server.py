from flask import Flask, request, jsonify, make_response
import time, string, random
from board import Board
from polling import LongPolling


app = Flask(__name__)
has_color_update = True
board_dict = dict()
long_polling = LongPolling(10)


# when boards are initted they should make a request to this endpoint
@app.route("/init", methods=["POST"])
def init_board():
    global board_dict
    _body = body(request)
    board_id = ''.join(random.choice(string.ascii_letters) for i in range(10))
    board_name = _body.get("name")
    print("Submitted name: ", board_name)

    new_board = Board(board_id, board_name)

    if board_dict.get(board_id) is not None:
        print("Tried to init already initted board.")
        return str(board_id) + " already initted."

    board_dict[board_id] = new_board
    temp_dict = dict()
    temp_dict["board_id"] = board_id
    print("All went well!")
    return jsonify(temp_dict)


# sends color from Android App to web server. 
# Board ID must be submitted along with the request
# colors are defined by an RGB value (255,255,255)
# possible settings include color intensity, and temperature
# SUBMIT NEW COLOR FOR BOARD
@app.route("/submitcolor", methods=["POST"])
def submit_color():
    global has_color_update, board_dict
    _body = body(request)
    red = _body.get("red")
    green = _body.get("green")
    blue = _body.get("blue")
    board_id = _body.get("board_id")

    board = board_dict.get(board_id)
    if board == None:
        return "SubmitColor - No board available with that ID."

    board.color = {"red" : int(red), "green" : int(green), "blue" : int(blue)}
    board_dict[board_id] = board

    has_color_update = True
    return "Board with ID " + str(board_id) + " has following color: (" + str(red) + ", " + str(green) + ", " + str(blue) + ")"



# GET COLOR OF BOARD !-WITH-! LONG POLLING
@app.route("/getcolor", methods=["POST"])
def get_color():
    global has_color_update
    _body = body(request)
    board_id = _body.get("board_id")

    board = board_dict.get(board_id)
    if board == None:
        return "GetColor - No board available with that ID."

    long_polling.remove_expired_polling_addresses()

    if long_polling.is_polling(board_id):
        wait_counter = 0
        while wait_counter < 30:
            if has_color_update:
                break
            time.sleep(2)
            wait_counter += 1
        if not has_color_update:
            return ('', 204)    # The HTTP 204 No Content success status response code indicates
                                # that the request has succeeded, but that the client 
                                # doesn't need to go away from its current page. 
                                # A 204 response is cacheable by default.
    else:
        long_polling.add_poller(board_id)
    
    has_color_update = False
    return jsonify(board.color)


# GET COLOR OF BOARD !-WITHOUT-! LONG POLLING
@app.route("/getcurrentcolor", methods=["GET"])
def get_color_once():
    board_id = request.args.get("board_id")
    board = board_dict.get(board_id)

    if board == None:
        return "GetCurrentColor - No board available with that ID."
    return jsonify(board.color)



# SUBMIT LIGHT SENSED BY BOARD AND APPEND IT TO FILE
@app.route("/submitlight", methods=["POST"])
def submit_light():
    global has_color_update
    _body = body(request)
    board_id = _body.get("board_id")
    light = _body.get("light")
    log_file = open("lightlog.csv", "a")
    log_file.write(light + "," + time.time_ns())
    log_file.close()
    return "Submit light"


# GET A COMPLETE LIST OF ALL BOARDS
# TAKES A SECRET AS ARGUMENT AS SECURITY MEASURE
@app.route("/boards", methods=["GET"])
def get_boards():
    secret_file = open("pie.txt", "r")
    secret_word = str(secret_file.readline())
    secret_file.close()
    provided_secret = request.args.get("secret")
    if secret_word != provided_secret:
        return ('', 401)
    boards_j = [board.__dict__ for board in list(board_dict.values())]
    boards_json = {
        "boards": boards_j
    }
    return jsonify(boards_json)



'''
Helper methods below here.
Adds some nice headers, and method to easy access body of request
'''
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] = "*"
    return response

def body(request):
    return request.get_json()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8081, threaded=True) # 19409