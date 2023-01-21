class Tile():
    def __init__(self):
        self.correct_place = False
        self.in_word = False
        self.char = ''
        self.index = None
    
    def set_correct_place(self, bool):
        self.correct_place = bool

    def set_in_word(self, bool):
        self.in_word = bool
    
    def set_char(self, char):
        self.char = char

    def get_correct_place(self):
        return self.correct_place

    def get_in_word(self):
        return self.in_word
    
    def get_char(self):
        return self.char

