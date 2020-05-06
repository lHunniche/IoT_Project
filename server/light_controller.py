import math

class Reading:
    def __init__(self):
        self.setpoint_at_time = None
        self.light_level = None
        self.led_intensity = None
        self.board_id = None


    def with_setpoint(self, setpoint):
        self.setpoint = setpoint
        return self
    

    def and_intensity_of(self, led_intensity):
        self.led_intensity = led_intensity
        return self
    

    def measured(self, light_measured):
        self.light_level = light_measured
        return self

    def board_with_id(self, board_id):
        self.board_id = board_id
        return self


class light_actuator:
    def __init__(self):
        self.readings = list()


    def submit_reading(self, board, light_measured, setpoint):
        # see how far reading deviates from setpoint
        # determine course of action (increase, decrease, or do nothing)

        # construct Reading object and set attributes
        reading = Reading()\
                        .board_with_id(board.board_id)\
                        .measured(light_measured)\
                        .with_setpoint(setpoint)\
                        .and_intensity_of(board.led_intensity)
        readings.append(reading)

        dist_to_setpoint = setpoint - reading.light_level
        updated_board = act_on_reading(dist_to_setpoint, board)

        return updated_board


    def act_on_reading(self, dist_to_setpoint, board):
        # if very close to set point, ignore and carry on
        if abs(dist_to_setpoint) < 10:
            return board
        
        # take the square root of the distance, interpret as percentage, and subtract/add that from current intensity
        act_value = int(math.sqrt(abs(dist_to_setpoint)))/100
        led_intensity = board.color["led_intensity"]
        new_led_intensity = 0
        
        if dist_to_setpoint > 0:
            new_led_intensity = led_intensity + led_intensity*act_value
        else:
            new_led_intensity = led_intensity - led_intensity*act_value

        board.color["led_intensity"] = new_led_intensity
        return board
        
            
        
        
