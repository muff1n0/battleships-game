class Patch:


    shipHere = False
    headShipHere = False
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


class Ship:
    

    alive = True


    def __init__(self, length, orientation, board, location = ""): #up, down, left, right
        self.length = length
        self.orientation = orientation
        self.board = board
        self.location = location

    @staticmethod
    def locationSwitch(location):
        """
        Accepts location in Letter-Number (Column, Row) format and converts it into Number-Number (Row, Column) format \n
        String -> String
        """
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return int(location[1]) - 1, alphabet.index(location[0])
    

    def checkLocation(self, location): 
        """
        Accepts patch to check if that new location can hold that ship or if that new location exists \n
        Patch Object -> Boolean
        """
        row_index, column_index = Ship.locationSwitch(location)
        ship_span = []
        if self.orientation == "up": #the tail points up
            ship_span_indexes = [(row_index - row, column_index) for row in range(self.length)]
        elif self.orientation == "down":
            ship_span_indexes = [(row_index + row, column_index) for row in range(self.length)]
        elif self.orientation == "left":
            ship_span_indexes = [(row_index, column_index - column) for column in range(self.length)]
        elif self.orientation == "right":
            ship_span_indexes = [(row_index, column_index + column) for column in range(self.length)]
        print(ship_span_indexes)
        for row, column in ship_span_indexes:
            if row < 0 or column < 0:
                return False
            try:
                ship_span.append(self.board.board[row][column])
            except IndexError:
                return False
        return False in [patch.shipHere for patch in ship_span]


    def removeShip(self):
        """
        Sets all the patches that the ship occupies to not be occupied anymore 
        None -> None
        """
        if self.location == "":
            return 
        row_index, column_index = Ship.locationSwitch(self.location)
        self.board.board[row_index][column_index].headShipHere = False
        if self.orientation == "up": 
            ship_span_indexes = [(row_index - row, column_index) for row in range(self.length)]
        elif self.orientation == "down":
            ship_span_indexes = [(row_index + row, column_index) for row in range(self.length)]
        elif self.orientation == "left":
            ship_span_indexes = [(row_index, column_index - column) for column in range(self.length)]
        elif self.orientation == "right":
            ship_span_indexes = [(row_index, column_index + column) for column in range(self.length)]
        for row, column in ship_span_indexes:
            self.board.board[row][column].shipHere = False


    def moveShip(self, location): #runs after computer checks if the location is available
        """
        After a location is validated for a ship, this function sets the shipHere for all the 
        patches the ship will occupy to True and sets the headShipHere value for the head ship 
        to be True
        String -> None
        """
        self.location = location
        row_index, column_index = Ship.locationSwitch(location)
        self.board.board[row_index][column_index].headShipHere = True 
        if self.orientation == "up": 
            ship_span_indexes = [(row_index - row, column_index) for row in range(self.length)]
        elif self.orientation == "down":
            ship_span_indexes = [(row_index + row, column_index) for row in range(self.length)]
        elif self.orientation == "left":
            ship_span_indexes = [(row_index, column_index - column) for column in range(self.length)]
        elif self.orientation == "right":
            ship_span_indexes = [(row_index, column_index + column) for column in range(self.length)]
        for row, column in ship_span_indexes:
            self.board.board[row][column].shipHere = True


    def checkRotate(self, orientation):
        """
        Checks if the hypothetical patches a ship will occupy if it is rotated is valid \n
        String -> Boolean
        """
        if orientation == self.orientation:
            return True
        row_index, column_index = Ship.locationSwitch(self.location)
        ship_span = []
        if orientation == "up": 
            ship_span_indexes = [(row_index - row, column_index) for row in range(self.length)]
        elif orientation == "down":
            ship_span_indexes = [(row_index + row, column_index) for row in range(self.length)]
        elif orientation == "left":
            ship_span_indexes = [(row_index, column_index - column) for column in range(self.length)]
        elif orientation == "right":
            ship_span_indexes = [(row_index, column_index + column) for column in range(self.length)]
        for row, column in ship_span_indexes:
            if row < 0 or column < 0:
                return False
            try:
                ship_span.append(self.board.board[row][column])
            except IndexError:
                return False
        return False in [patch.shipHere for patch in ship_span]


class Game:


    p1 = Board()
    p2 = Board()

