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
    "getboardinfo": base_url + "/getboardinfo"
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
    print("Initting: ", name)
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
    print(len(board_ids))
    board_id = board_ids[rand_board_index]
    print(rand_board_index)
    print(board_id, " chosen from ")
    print(board_ids)
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
    return None

#/getcurrentcolor
# <board_id(String)>
# Returns the board (with adjusted light intensity and blue light filter)
#@given()
def get_current_color(board_ids):
    print("Get Current Color")
    return None

#/toggleautolight
# <board_id(String)>
# <setpoint(Integer)>
# Returns String message
#@given()
def toggle_auto_light(board_ids):
    print("Toggle Auto Light")
    return None

#/autolightupdate
# <board_id(String)>
# <measured_light(Integer)>
# Returns String message
#@given()
def auto_light_update(board_ids):
    print("Auto Light Update")
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
    for i in range(0,10):
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



test_command_lists()
















