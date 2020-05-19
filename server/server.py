from flask import Flask, request, jsonify, make_response
import time, string, random, copy, json
from board import Board
from polling import LongPolling
from light_controller import light_actuator


app = Flask(__name__)
board_dict = dict()
color_long_polling = LongPolling(poll_renew = 10)
debug = False
l_actuator = light_actuator()

'''
VARIABLES
'''
length_of_board_id = 10


# when boards are initted they should make a request to this endpoint
# REQUIRES:
#   name
# RETURNS:
#   board_id
@app.route("/init", methods=["POST"])
def init_board():
    global board_dict
    body = get_body(request)
    board_id = ''.join(random.choice(string.ascii_letters) for i in range(length_of_board_id))
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

# REQUIRES
#   board_id
#   red, green, blue
#   led_intensity
#   setpoint
#   blue_light_filter
#   auto_adjust_light (dependant on setpoint)
@app.route("/updateboardstate", methods=["POST"])
def update_board_state():
    body = get_body(request)
    if body == None:
        print("UpdateBoardState - No body included in POST request - response aborted.")
        return "UpdateBoardState - No body included in POST request - response aborted."

    board_id = body.get("board_id")
    red = body.get("red")
    green = body.get("green")
    blue = body.get("blue")
    led_intensity = body.get("led_intensity")
    setpoint = body.get("setpoint")
    blue_light_filter = body.get("blue_light_filter")
    auto_adjust_light = body.get("auto_adjust_light")
    return_message = dict()

    print("auto_adjust_light: " + str(auto_adjust_light))
    print("blue_light_filter: " + str(blue_light_filter))


    board = board_dict[board_id]

    if board == None:
        print("Tried to update board that didn't exist - " + str(board_id))
        return "UpdateBoardState - no board with that ID exists"

    if red == None:
        red = board.color["red"]
        return_message["red_warning"] = "Red not provided - using board's current color instead."
    if blue == None:
        blue = board.color["blue"]
        return_message["blue_warning"] = "Blue not provided - using board's current color instead."
    if green == None:
        green = board.color["green"]
        return_message["green_warning"] = "Green not provided - using board's current color instead."
    if led_intensity == None:
        led_intensity = board.led_intensity
        return_message["led_intensity_warning"] = "LED_intensity not provided - using board's current setting instead."
    if blue_light_filter == None:
        print("Blue light filter was None")
        blue_light_filter = board.blue_light_filter
        return_message["blue_light_filter_warning"] = "Blue Light Filter not provided - using board's current setting instead."
    if auto_adjust_light == True:
        # this is True when auto-mode is selected, but no setpoint is provided
        if setpoint == None and board.auto_adjust_light == False:
            auto_adjust_light = False
            return_message["auto_adjust_light_error"] = "Setpoint not provided when trying to start Auto-Mode."
    if setpoint == None:
        setpoint = board.setpoint
        return_message["setpoint_warning"] = "Setpoint not provided - current board's current setting instead."
    
    board.color["red"] = int(red)
    board.color["blue"] = int(blue)
    board.color["green"] = int(green)
    board.led_intensity = int(led_intensity)
    print("what is blue light filter???")
    print(blue_light_filter)
    print(bool(blue_light_filter))
    board.blue_light_filter = bool(blue_light_filter)
    board.auto_adjust_light = bool(auto_adjust_light) 
    board.setpoint = int(setpoint)
    board.has_update = True

    return_body = dict()
    return_body["board"] = board.__dict__
    return_body["messages"] = return_message

    return jsonify(return_body)



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
    blue_light_filter_bool = body.get("blue_light_filter")

    board = board_dict.get(board_id)
    if board == None:
        return "SubmitColor - No board available with that ID."

    # !!! DELETE WHEN BLUE LIGHT FILTER IS FULLY IMPLEMENTED !!!
    #if blue_light_filter_bool == None:
    #    blue_light_filter_bool = False
    # !!! DELETE WHEN BLUE LIGHT FILTER IS FULLY IMPLEMENTED !!!

    red = int(red)
    green = int(green)
    blue = int(blue)
    led_intensity = int(led_intensity)
    
    
    red = max(0, red)
    red = min(255, red)
    green = max(0, green)
    green = min(255, green)
    blue = max(0, blue)
    blue = min(255, blue)
    led_intensity = max(0, led_intensity)
    led_intensity = min(1, led_intensity)


    board.color = {"red" : int(red), "green" : int(green), "blue" : int(blue)}
    board.led_intensity = int(led_intensity)
    board.blue_light_filter = blue_light_filter_bool
    board.has_update = True
    board_dict[board_id] = board

    return "Board with ID " + str(board_id) + " has following color: (" + str(red) + ", " + str(green) + ", " + str(blue) + "), and Intensity of " + str(led_intensity) + "%"


# GET COLOR OF BOARD !-WITH-! LONG POLLING
@app.route("/getupdates", methods=["POST"])
def get_color():
    global board_dict
    body = get_body(request)
    board_id = body.get("board_id")
    lux_in_room = body.get("lux_in_room")

    board = board_dict.get(board_id)
    if board == None:
        return "RE-INIT:No board with that ID exists"

    color_long_polling.remove_expired_polling_addresses()

    if color_long_polling.is_polling(board_id):
        wait_counter = 0
        while wait_counter < 10:
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
    updated_board.lux_in_room = lux_in_room
    board_dict[board_id] = updated_board

    # perform any last minute adjustments before sending board off
    temp_board = copy.deepcopy(updated_board)

    adjust_rgb_for_intensity(temp_board)
    adjust_rgb_for_blue_filter(temp_board)
    return jsonify(temp_board.__dict__)


# GET COLOR OF BOARD !-WITHOUT-! LONG POLLING
@app.route("/getboardinfo", methods=["GET"])
def get_board_info():
    board_id = request.args.get("board_id")
    board = board_dict.get(board_id)

    if board == None:
        return "GetBoardInfo - No board available with that ID."
    
    # perform any last minute adjustments before sending board off
    temp_board = copy.deepcopy(board)
    adjust_rgb_for_intensity(temp_board)
    adjust_rgb_for_blue_filter(temp_board)
    return jsonify(temp_board.__dict__)


# GET RAW BOARD DARTA
# REQUIRES:
#   board_id

@app.route("/getboardinforaw", methods=["GET"])
def get_board_info_raw():
    board_id = request.args.get("board_id")
    board = board_dict.get(board_id)

    if board == None:
        return "GetBoardInfo - No board available with that ID."

    return jsonify(board.__dict__)


# TOGGLES BLUE LIGHT FILTER (BOOLEAN) ON A BOARD 
# REQUIRES:
#   board_id
# RETURNS:
#   message
@app.route("/togglebluelightfilter", methods=["POST"])
def toggle_blue_light_filter():
    body = get_body(request)
    board_id = body.get("board_id")
    board = board_dict.get(board_id)

    if board == None:
        return "ToggleBlueLightFilter - No board available with that ID."
    
    board.blue_light_filter = not board.blue_light_filter
    return_body = {"blue_light_filter" : board.blue_light_filter}

    return jsonify(return_body)


# REQUIRES:
#   board_id
#   setpoint for light
# RETURNS:
#   message
@app.route("/toggleautolight", methods=["POST"])
def toggle_auto_light_mode():
    body = get_body(request)
    board_id = body.get("board_id")
    setpoint = body.get("setpoint")

    board = board_dict.get(board_id)
    if board == None:
        return "ToggleAutoLight - Error"
    board.auto_adjust_light = not board.auto_adjust_light
    if setpoint != None:
        board.setpoint = setpoint

    return_body = {"auto_adjust_light" : board.auto_adjust_light}
    if board.auto_adjust_light:
        board.led_intensity_before_auto = board.led_intensity
    else:
        board.led_intensity = board.led_intensity_before_auto
        
    board.has_update = True
    return jsonify(return_body)


# REQUIRES:
#   board_id
#   measured_light
# RETURNS:
#   message
@app.route("/autolightupdate", methods=["POST"])
def auto_light_actuator():
    body = get_body(request)
    board_id = body.get("board_id")
    measured_light = body.get("measured_light")

    board = board_dict.get(board_id)
    if board == None:
        return "AutoLightUpdate - Error"
    initial_led_intensity = board.led_intensity
    updated_board = l_actuator.submit_reading(board, measured_light, board.setpoint)
    updated_board.has_update = True
    board_dict[board_id] = updated_board
    updated_led_intensity = updated_board.led_intensity

    return_message = "Intensity changed from " + str(initial_led_intensity) + " to " + str(updated_led_intensity) + "."
    return_body = {"return_message" : return_message}
    return jsonify(return_body)


# REQUIRES:
#   board_id
#   setpoint
# RETURNS:
#   message
@app.route("/updatesetpoint", methods=["POST"])
def update_setpoint():
    body = get_body(request)
    board_id = body.get("board_id")
    setpoint = body.get("setpoint")

    board = board_dict.get(board_id)
    if board == None:
        return "UpdateSetpoint - Board Error"
    
    board.setpoint = setpoint

    return "Setpoint updated"


# SUBMIT LIGHT SENSED BY BOARD AND APPEND IT TO FILE
# REQUIRES:
#   board_id
#   measured_light
# RETURNS:
#   message
@app.route("/submitlightdata", methods=["POST"])
def submit_light():
    body = get_body(request)
    board_id = body.get("board_id")
    light = body.get("measured_light")
    log_file = open("lightlog.csv", "a")
    log_file.write(light + "," + time.time_ns())
    log_file.close()
    return "Submit light data"


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
def adjust_rgb_for_intensity(temp_board):
    adjustment = temp_board.led_intensity / 100

    temp_board.color["red"] = int(temp_board.color["red"] * adjustment)
    temp_board.color["green"] = int(temp_board.color["green"] * adjustment)
    temp_board.color["blue"] = int(temp_board.color["blue"] * adjustment)
    
    return temp_board


# alter the RGB values for when blue light filtering is enabled
def adjust_rgb_for_blue_filter(temp_board):
    if temp_board.blue_light_filter:
        temp_board.color["blue"] = 0
    return temp_board


@app.route("/reset", methods=["POST"])
def reset_board_dict():
    global board_dict
    board_dict = dict()

    return "You just wiped our board dict, thank you very much."





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




