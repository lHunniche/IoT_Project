class Board:
    def __init__(self, board_id=None, name=None):
        self.board_id = board_id
        self.color = {"red": 255, "green": 255, "blue": 255}
        self.led_intensity = 50
        self.name = name
        self.has_update = True
        self.auto_adjust_light = False
        self.setpoint = None
        self.blue_light_filter = False


    def __str__(self):
        return str(self.__dict__)

    
    def board_hash(self):
        return \
            self.color["red"]*17 + \
            self.color["green"]*31 + \
            self.color["blue"]*43 + \
            self.led_intensity*59


    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Board):
            return self.board == other.board_id
        return False


    '''
    def to_dict(self):
        md = dict()
        
        md["board_id"] = self.board_id
        md["color"] = self.color
        md["led_intensity"] = self.led_intensity
        md["name"] = self.name
        md["has_update"]
    '''
