#Endpoint specifications
from hypothesis import given, settings,HealthCheck
import hypothesis.strategies as st
import requests
import random

domain = "http://klevang.dk"
port = 19409
base_url = domain + ":" +  str(port)

urls = {
    "init": base_url + "/init",
    "submitcolor": base_url + "/submitcolor",
    "getupdates": base_url + "/getupdates",
    "getcurrentcolor": base_url + "/getcurrentcolor",
    "toggleautolight": base_url + "/toggleautolight",
    "autolightupdate": base_url + "/autolightupdate",
    "updatesetpoint": base_url + "/updatesetpoint",
    "submitlightdata": base_url + "/submitlightdata",
    "boards": base_url + "/boards",
    "getboardinfo": base_url + "/getboardinfo",
    "reset": base_url + "/reset"
}


def post(url, body):
    response = requests.post(url, json = body)
    return response

def get(url):
    response = requests.get(url)
    return response


#/init?name=<nameofboard>
#Inits a new board with a provided name(String)
#and returns a unique generated id (String)
def init(name, board_ids):
    response = post(urls["init"], {"name": name})
    board_id = response.json()["board_id"]
    board_ids.append(board_id)
    #printprint("Initting: ", name)
    return board_id


#/submitcolor 
# <red(Integer)> 
# <green(Integer)> 
# <blue(Integer)>
# <blue_light_filter(Boolean)>
# <board_id(String)>
# <led_intensity(Integer)>
@given(\
    red = st.integers(), \
    green = st.integers(), \
    blue=st.integers(), \
    led_intensity = st.integers(), \
    blue_light_filter = st.booleans()
    )
@settings(max_examples = 1)
def submit_color(board_ids, red, green, blue, led_intensity, blue_light_filter):
    rand_board_index = random.SystemRandom().randint(0, len(board_ids) - 1)
    #print(len(board_ids))
    board_id = board_ids[rand_board_index]
    #print(rand_board_index)
    #print(board_id, " chosen from ")
    #print(board_ids)
    post(urls["submitcolor"], body ={
        "board_id": board_id,
        "red": red,
        "green": green,
        "blue": blue,
        "led_intensity": led_intensity,
        "blue_light_filter": blue_light_filter
    })
    url = urls["getboardinfo"] + "?board_id="+board_id
    board_info = get(url).json()
    color = board_info["color"]
    updated_red = color["red"]
    updated_green = color["green"]
    updated_blue = color["blue"]
    updated_led_intensity = board_info["led_intensity"]
    updated_blue_light_filter = board_info["blue_light_filter"]
    assert(updated_red <= 255)
    assert(updated_red >= 0)
    assert(updated_green <= 255)
    assert(updated_green >= 0)
    assert(updated_blue <= 255)
    assert(updated_blue >= 0)
    assert(updated_led_intensity <= 100)
    assert(updated_led_intensity >= 0)
    assert(updated_blue_light_filter == blue_light_filter)

#/getupdates
# <board_id(String)>
# LONGPOLLING
# Returns the board (with adjusted light intensity and blue light filter)
#@given()
def get_updates(board_ids):
    print("Get Updates")
    # with long polling, maybe later
    return None

#/getcurrentcolor
# <board_id(String)>
# Returns the board (with adjusted light intensity and blue light filter)
#@given()
def get_current_color(board_ids):
    print("Get Current Color")
    # trivial, just fetches board.
    return None

#/toggleautolight
# <board_id(String)>
# <setpoint(Integer)>
# Returns String message
@given(placeholder = st.none())
@settings(max_examples = 1)
def toggle_auto_light(placeholder, board_ids):
    #print("Toggle Auto Light")
    rand_board_index = random.SystemRandom().randint(0, len(board_ids) - 1)
    board_id = board_ids[rand_board_index]
    url = urls["getboardinfo"] + "?board_id="+board_id
    board_info_before = get(url).json()

    auto_mode_before = board_info_before["auto_adjust_light"]
    if auto_mode_before == True:
        auto_mode_after = not auto_mode_before
        current_setpoint = board_info_before["setpoint"]
        current_led_intensity = board_info_before["led_intensity_before_auto"]

        post(urls["toggleautolight"], body ={
        "board_id": board_id,
        "auto_adjust_light" : auto_mode_after,
        "setpoint" : current_setpoint
        })
        
        board_info_after = get(url).json()
        auto_mode_new = board_info_after["auto_adjust_light"]
        led_intensity_before_auto_new = board_info_after["led_intensity"]

        assert(auto_mode_new == auto_mode_after)
        assert(led_intensity_before_auto_new == current_led_intensity)

        # ændre den til false, og tjek at det skete
        # tjek at led_intensity bliver lig med led_intensity_before_auto
    else:
        auto_mode_after = not auto_mode_before
        current_setpoint = board_info_before["setpoint"]
        current_led_intensity = board_info_before["led_intensity"]

        post(urls["toggleautolight"], body ={
        "board_id": board_id,
        "auto_adjust_light" : auto_mode_after,
        "setpoint" : current_setpoint
        })

        board_info_after = get(url).json()
        auto_mode_new = board_info_after["auto_adjust_light"]
        led_intensity_before_auto_new = board_info_after["led_intensity_before_auto"]

        assert(auto_mode_new == auto_mode_after)
        assert(led_intensity_before_auto_new == current_led_intensity)
        # ændre den til true, og tjek at det skete
        # tjek at led_intensity_before_auto bliver sat lig med led_intensity

    return None

#/autolightupdate
# <board_id(String)>
# <measured_light(Integer)>
# Returns String message
@given(measured_light = st.integers(max_value=10000, min_value=0))
def auto_light_update(board_ids, measured_light):
    #print("Auto Light Update")

    # if measured_light < setpoint THEN led_intensity decreases ELSE led_intensity increases
    rand_board_index = random.SystemRandom().randint(0, len(board_ids) - 1)
    board_id = board_ids[rand_board_index]
    url = urls["getboardinfo"] + "?board_id="+board_id
    board_info_before = get(url).json()

    initial_setpoint = board_info_before["setpoint"]
    initial_led_intensity = board_info_before["led_intensity"]
    post(urls["autolightupdate"], body ={
        "board_id": board_id,
        "measured_light" : measured_light
        })
    
    board_info_after = get(url).json()
    setpoint_after = board_info_after["setpoint"]
    led_intensity_after = board_info_after["led_intensity"]

    print("----")
    print("LED_INTENSITY_BEFORE: " + str(initial_led_intensity))
    print("MEASURED LIGHT: " + str(measured_light))
    print("LED_INTENSITY_AFTER: " + str(led_intensity_after))
    
    dist_to_setpoint = initial_setpoint - measured_light

    assert(led_intensity_after >= 0)
    if abs(dist_to_setpoint) < 10:
        assert(led_intensity_after == initial_led_intensity)
        print("HEJ")
    elif measured_light < initial_setpoint:
        if initial_led_intensity == 100:
            print("MED")
            assert(led_intensity_after == 100)
        else:
            print("SUR")
            assert(led_intensity_after > initial_led_intensity)
    elif measured_light > initial_setpoint:
        if initial_led_intensity == 0:
            print("DIG")
            assert(led_intensity_after == 0)
        else:
            print("KRYDSORD")
            assert(led_intensity_after < initial_led_intensity)

    print("----")
    return None

#/updatesetpoint
# <board_id(String)>
# <setpoint(Integer)>
# Returns String message
#@given()
def update_setpoint(board_ids):
    print("Update Setpoint")
    return None

#/submitlightdata
# <board_id(String)>
# <measured_light(Integer)>
# Appends the data to a .csv file
# Returns a String message
#@given()
def submit_light_data(board_ids):
    print("Submit Light Data")
    return None

#/boards
# <secret(String=QmGZADAipmhKsovsIhyQQcsTxgFkiy)>
# Returns a list of all registered boards
#@given()
def boards(board_ids):
    print("Boards")
    return None



commands = [\
    init, \
    submit_color, \
    get_updates, \
    get_current_color, \
    toggle_auto_light, \
    auto_light_update, \
    update_setpoint, \
    submit_color, \
    boards]


@st.composite
def command_lists(draw):
    command_list = []
    global commands
    command_list = draw(st.lists(commands_gen(), min_size=1, max_size=100))
    for i in range(1):
        command_list.insert(i, commands[0])
    # command_list.insert(0, commands[0])
    return command_list


@st.composite
def commands_gen(draw):
    global commands
    #TODO: Ask Jan about random generator
    i = draw(st.integers(min_value=0, max_value=len(commands) -1))
    return commands[i]


@given(command_list = command_lists(), name = st.text())
@settings(deadline = 100000,suppress_health_check=(HealthCheck.too_slow,))
def test_command_lists(command_list,name):
    board_ids = []
    print("_____________ NEW COMMANDS LIST _________________")
    func_names = [c.__name__ for c in command_list]
    print(func_names)
    for func in command_list:
        if func.__name__ == "init":
            board_id = func(name,board_ids)
            assert(len(board_id) == 10)
        else:
            func(board_ids)
    print("Tested with board ids: ", board_ids)
    print("\n\n__________________________________________________\n\n")


post(urls["reset"], body ={})
test_command_lists()
















