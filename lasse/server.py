from flask import Flask, request, jsonify, make_response
import time
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
    board_id = _body.get("board_id")
    print("Trying to init: " + str(board_id))
    new_board = Board(board_id)

    if board_dict.get(board_id) is not None:
        return str(board_id) + " already initted."

    board_dict[board_id] = new_board
    return str(board_id) + " initted."



# delete later...
@app.route("/", methods=["GET"])
def index():
    body = request.get_json()
    return "Jep"



# sends color from Android App to web server. 
# Board ID must be submitted along with the request
# colors are defined by an RGB value (255,255,255)
# possible settings include color intensity, and temperature
@app.route("/submitcolor", methods=["POST", "GET"])
def submitColor():
    global has_color_update, board_dict
    _body = body(request)
    red = _body.get("red")
    green = _body.get("green")
    blue = _body.get("blue")
    board_id = body.get(board_id)

    board = board_dict.get(board_id)
    if board == None:
        return "SubmitColor - No board available with that ID."

    board.color = {"red" : red, "green" : green, "blue" : blue}
    board_dict[board_id] = board

    has_color_update = True
    return "Board with ID " + str(board_id) + " has following color: (" + str(red) + ", " + str(green) + ", " + str(blue) + ")"

# this message 
@app.route("/getcolor", methods=["POST"])
def getColor():
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



@app.route("/submitlight", methods=["POST"])
def submitLight():
    _body = body(request)
    pass

def body(request):
    return request.get_json()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8081, threaded=True)