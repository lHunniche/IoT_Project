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
    

    def and_intensity_of(self, brightness):
        self.led_brightness = brightness
        return self
    

    def measured(self, light_measured):
        self.light_level = light_measured
        return self

    def board_with_id(self, board_id):
        self.board_id = board_id
        return self


class Actuator:
    def __init__(self):
        self.setpoint = None
        self.readings = list()
        self.led_intensity = None


    def submit_reading(self, light_measured, board):
        # see how far reading deviates from setpoint
        # determine course of action (increase, decrease, or do nothing)

        # construct Reading object and set attributes
        reading = Reading()\
                        .board_with_id(board.board_id)\
                        .measured(light_measured)\
                        .with_setpoint(self.setpoint)\
                        .and_intensity_of(self.led_brightness)
        readings.append(reading)

        dist_to_setpoint = self.setpoint - reading.light_level
        updated_board = act_on_reading(dist_to_setpoint, board)

        return updated_board


    def act_on_reading(self, dist_to_setpoint, board):
        # if very close to set point, ignore and carry on
        if abs(dist_to_setpoint) < 10:
            return board
        
        # take the square root of the distance, interpret as percentage, and 
        act_value = int(math.sqrt(abs(dist_to_setpoint)))/100
        current_pwm = board.color["pwm_duty_cycle"]
        new_pwm = 0
        
        if dist_to_setpoint > 0:
            new_pwm = current_pwm + current_pwm*act_value
        else:
            new_pwm = current_pwm - current_pwm*act_value

        board.color["pwm_duty_cycle"] = new_pwm
        return board
        
            
        
        
