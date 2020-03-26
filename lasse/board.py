class Board:
    def __init__(self, board_id):
        self.board_id = board_id
        self.color = {"red": 255, "green": 255, "blue": 255}


    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Board):
            return self.board == other.board_id
        return False