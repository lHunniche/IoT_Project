from flask import Flask, request, jsonify, make_response
import time, string, random, copy
from board import Board
from polling import LongPolling
from light_controller import light_actuator


app = Flask(__name__)
has_color_update = True
board_dict = dict()
color_long_polling = LongPolling(poll_renew = 10)
debug = False
l_actuator = light_actuator()


# when boards are initted they should make a request to this endpoint
# REQUIRES:
#   name
@app.route("/init", methods=["POST"])
def init_board():
    global board_dict
    body = get_body(request)
    board_id = ''.join(random.choice(string.ascii_letters) for i in range(10))
    board_name = body.get("name")
    if debug:
        print("Submitted name: ", board_name)

    new_board = Board(board_id, board_name)

    if board_dict.get(board_id) is not None:
        if debug: 
            print("Tried to init already initted board.")
        return str(board_id) + " already initted."

    board_dict[board_id] = new_board
    temp_dict = dict()
    temp_dict["board_id"] = board_id
    if debug: 
        print("All went well!")
    return jsonify(temp_dict)


# sends color from Android App to web server. 
# Board ID must be submitted along with the request
# colors are defined by an RGB value (255,255,255)
# possible settings include color intensity, and temperature
# SUBMIT NEW COLOR FOR BOARD
@app.route("/submitcolor", methods=["POST"])
def submit_color():
    global board_dict
    body = get_body(request)
    red = body.get("red")
    green = body.get("green")
    blue = body.get("blue")
    led_intensity = body.get("led_intensity")
    board_id = body.get("board_id")

    board = board_dict.get(board_id)
    if board == None:
        return "SubmitColor - No board available with that ID."

    # !!! DELETE WHEN PWM IS FULLY IMPLEMENTED !!!
    #if led_intensity == None:
    #    led_intensity = 50
    # !!! DELETE WHEN PWM IS FULLY IMPLEMENTED !!!

    board.color = {"red" : int(red), "green" : int(green), "blue" : int(blue)}
    board.led_intensity = int(led_intensity)
    board.has_update = True
    board_dict[board_id] = board

    return "Board with ID " + str(board_id) + " has following color: (" + str(red) + ", " + str(green) + ", " + str(blue) + "), and Intensity of " + str(led_intensity) + "%"


# GET COLOR OF BOARD !-WITH-! LONG POLLING
@app.route("/getcolor", methods=["POST"])
def get_color():
    global board_dict
    body = get_body(request)
    board_id = body.get("board_id")

    board = board_dict.get(board_id)
    if board == None:
        return "RE-INIT:No board with that ID exists"

    color_long_polling.remove_expired_polling_addresses()

    if color_long_polling.is_polling(board_id):
        wait_counter = 0
        while wait_counter < 30:
            if debug:
                print(board_id + ": waiting for new color...")
            if board_dict.get(board_id).has_update:
                break
            time.sleep(2)
            wait_counter += 1
        if not board_dict.get(board_id).has_update:
            return ('', 204)    # The HTTP 204 No Content success status response code indicates
                                # that the request has succeeded, but that the client 
                                # doesn't need to go away from its current page. 
                                # A 204 response is cacheable by default.
    else:
        color_long_polling.add_poller(board_id)
    
    updated_board = board_dict.get(board_id)
    updated_board.has_update = False
    board_dict[board_id] = updated_board

    return jsonify(adjust_rgb_for_intensity(updated_board))


# GET COLOR OF BOARD !-WITHOUT-! LONG POLLING
@app.route("/getcurrentcolor", methods=["GET"])
def get_color_once():
    board_id = request.args.get("board_id")
    board = board_dict.get(board_id)

    if board == None:
        return "GetCurrentColor - No board available with that ID."
    return jsonify(adjust_rgb_for_intensity(board))



# REQUIRES:
#   board_id
#   setpoint for light
@app.route("/toggleautolight", methods=["POST"])
def toggle_auto_light_mode():
    body = get_body(request)
    board_id = body.get("board_id")
    setpoint = body.get("setpoint")

    board = board_dict.get(board_id)
    if board == None:
        return "ToggleAutoLight - Error"
    board.auto_adjust_light = not board.auto_adjust_light
    board.has_update = True
    if setpoint != None:
        board.setpoint = setpoint

    if board.auto_adjust_light:
        return "AutoLight enabled in " + board.name
    else:
        return "AutoLight disabled in " + board.name


# REQUIRES:
#   board_id
#   measured_light
@app.route("/autolightupdate", methods=["POST"])
def auto_light_actuator():
    body = get_body(request)
    board_id = body.get("board_id")
    measured_light = body.get("measured_light")

    board = board_dict.get(board_id)
    initial_led_intensity = board.led_intensity
    updated_board = l_actuator.submit_reading(board, measured_light, board.setpoint)
    board.dict[board_id] = updated_board
    updated_led_intensity = updated_board.led_intensity

    return "Intensity changed from " + str(initial_led_intensity) + " to " + str(updated_led_intensity) + "."


@app.route("/updatesetpoint", methods=["POST"])
def update_setpoint():
    pass


# SUBMIT LIGHT SENSED BY BOARD AND APPEND IT TO FILE
@app.route("/submitlight", methods=["POST"])
def submit_light():
    global has_color_update
    body = get_body(request)
    board_id = body.get("board_id")
    light = body.get("light")
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



# return RGB values adjusted for brightness
def adjust_rgb_for_intensity(board):
    temp_board = copy.deepcopy(board)
    adjustment = temp_board.led_intensity / 100

    temp_board.color["red"] = int(temp_board.color["red"] * adjustment)
    temp_board.color["green"] = int(temp_board.color["green"] * adjustment)
    temp_board.color["blue"] = int(temp_board.color["blue"] * adjustment)
    
    return temp_board.color


'''
Helper methods below here.
Adds some nice headers, and method to easy access body of request
'''
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] = "*"
    return response

def get_body(request):
    return request.get_json()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8081, threaded=True) # 19409