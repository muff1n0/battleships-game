class Ship:
    

    alive = True


    def __init__(self, length, orientation):
        self.length = length
        self.orientation = orientation


    def locationSwitch(location):
        """
        Accepts location in Letter-Number (Column, Row) format and converts it into Number-Number (Row, Column) format
        String -> String
        """
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return str(location[1] - 1) + alphabet.index(location[0])


class Patch:


    displayIcons = ("-", "x", "o")


class Board:


    mode = "hidden" # hidden, setup, playing
    board = [[Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()], 
             [Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()], 
             [Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()], 
             [Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()], 
             [Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()], 
             [Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()], 
             [Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()], 
             [Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()], 
             [Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()], 
             [Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()]]


class Game:


    p1 = Board()
    p2 = Board()
