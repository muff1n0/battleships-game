class Patch:


    shipHere = False
    headShipHere = False
    deadShip = False
    marked = False

    
    def display(self, mode):
        """Represents a patch object when displayed in a humanreadable version \n
        String -> String 
        """
        if mode == "setup":
            if isinstance(self.headShipHere, Ship):
                return str(self.headShipHere.board.ships.index(self.headShipHere))
            elif self.shipHere:
                return "o"
            return "-"
        elif mode == "playing":
            if self.deadShip:
                return "x"
            elif self.shipHere:
                return "o"
            elif self.marked:
                return "+"
            return "-"
        elif mode == "hidden":
            if self.deadShip:
                return "x"
            elif self.marked: 
                return "+"
            return "-"


class Ship:
    

    alive = True


    def __init__(self, length, orientation, board = "", location = ""): #up, down, left, right
        self.length = length
        self.orientation = orientation
        self.board = board
        self.location = location


    @staticmethod
    def locationSwitch(location):
        """
        Accepts location in Letter-Number (Column, Row) format and converts it into Number-Number (Row, Column) format \n
        Returns False if location is not valid \n
        String -> String/Boolean
        """
        alphabet = "ABCDEFGHIJ"
        try: 
            return int(location[1:]) - 1, alphabet.index(location[0])
        except:
            return False
    

    def shipSpanRetrieve(self, location = None):
        """
        Returns a generator of tuples containing the indexes of the board that a ship occupies\n
        None -> Tuple
        """   
        if isinstance(location, str):
            row_index, column_index = Ship.locationSwitch(location)
        else:
            row_index, column_index = Ship.locationSwitch(self.location)
        if self.orientation == "up": #the tail points up
            ship_span_indexes = ((row_index - row, column_index) for row in range(self.length))
        elif self.orientation == "down":
            ship_span_indexes = ((row_index + row, column_index) for row in range(self.length))
        elif self.orientation == "left":
            ship_span_indexes = ((row_index, column_index - column) for column in range(self.length))
        elif self.orientation == "right":
            ship_span_indexes = ((row_index, column_index + column) for column in range(self.length))
        return ship_span_indexes


    @staticmethod
    def neighbors(ship_span_indexes):
        """
        Returns a list of tuples containing the indexes of the neighbors of a ship\n
        String -> list
        """
        neighbors = []
        for row_index, column_index in ship_span_indexes:
            if row_index == 0 and column_index == 0:
                neighbors.extend([(0, 1), (1, 0), (1, 1)])
            elif row_index == 9 and column_index == 0:
                neighbors.extend([(8, 0), (8, 1), (9, 1)])
            elif row_index == 0 and column_index == 9:
                neighbors.extend([(0, 8), (1, 8), (1, 9)])
            elif row_index == 9 and column_index == 9:
                neighbors.extend([(8, 9), (8, 8), (9, 8)])
            elif column_index == 0:
                neighbors.extend([(row_index - 1, column_index), (row_index - 1, column_index + 1), (row_index, column_index + 1), (row_index + 1, column_index), (row_index + 1, column_index + 1)])    
            elif row_index == 0:
                neighbors.extend([(row_index, column_index - 1), (row_index, column_index - 1), (row_index, column_index), (row_index, column_index + 1), (row_index - 1, column_index + 1)])
            elif column_index == 9:
                neighbors.extend([(row_index - 1, column_index-1), (row_index - 1, column_index), (row_index, column_index - 1), (row_index + 1, column_index - 1), (row_index + 1, column_index)])
            elif row_index == 9:
                neighbors.extend([(row_index - 1, column_index-1), (row_index - 1, column_index), (row_index - 1, column_index + 1), (row_index, column_index - 1), (row_index, column_index + 1)])
            else:
                neighbors.extend([(row_index - 1, column_index-1), (row_index - 1, column_index), (row_index - 1, column_index + 1), (row_index, column_index - 1), (row_index, column_index + 1), (row_index + 1, column_index - 1), (row_index + 1, column_index), (row_index + 1, column_index + 1)])
        return neighbors


    def checkLocation(self, location): 
        """
        Accepts patch to check if that new location can hold that ship\n
        Patch Object -> Boolean
        """
        if location == "BACK":
            return False
        ship_span = []
        ship_span_indexes = self.shipSpanRetrieve()
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
        Sets all the patches that the ship occupies to not be occupied anymore. Goes before move and rotate.\n
        None -> None
        """
        if self.location == "":
            return 
        row_index, column_index = Ship.locationSwitch(self.location)
        self.board.board[row_index][column_index].headShipHere = False
        ship_span_indexes = self.shipSpanRetrieve()
        for row, column in ship_span_indexes:
            self.board.board[row][column].shipHere = False


    def moveShip(self, location): #runs after computer checks if the location is available
        """
        After a location is validated for a ship, this function sets the shipHere for all the \n
        patches the ship will occupy to True and sets the headShipHere value for the head ship \n
        to be True
        String -> None
        """
        self.location = location
        row_index, column_index = Ship.locationSwitch(location)
        self.board.board[row_index][column_index].headShipHere = self 
        ship_span_indexes = self.shipSpanRetrieve(location)
        for row, column in ship_span_indexes:
            self.board.board[row][column].shipHere = True


    def checkRotate(self, orientation):
        """
        Checks if the hypothetical patches a ship will occupy if it is rotated is valid \n
        String -> Boolean
        """
        if orientation == self.orientation:
            return True
        ship_span = []
        ship_span_indexes = self.shipSpanRetrieve()
        for row, column in ship_span_indexes:
            if row < 0 or column < 0:
                return False
            try:
                ship_span.append(self.board.board[row][column])
            except IndexError:
                return False
        return False in [patch.shipHere for patch in ship_span]
            

    def rotate(self, orientation):
        """
        Rotates a ship\n
        String -> None
        """
        row_index, column_index = Ship.locationSwitch(self.location)
        self.board.board[row_index][column_index].headShipHere = self 
        self.orientation = orientation
        ship_span_indexes = self.shipSpanRetrieve()
        for row, column in ship_span_indexes:
            self.board.board[row][column].shipHere = True


class Board:


    mode = "setup" # hidden, setup, playing
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
    ships = (Ship(1, "up"), 
            Ship(1, "up"), 
            Ship(1, "up"), 
            Ship(1, "up"), 
            Ship(2, "up"), 
            Ship(2, "up"), 
            Ship(2, "up"), 
            Ship(3, "up"), 
            Ship(3, "up"), 
            Ship(4, "up"))
    placed = []


    def display(self):
        """Displays the entire board in a readable form \n
        None -> None
        """
        print("    A  B  C  D  E  F  G  H  I  J")
        for row_index, row in enumerate(self.board):
            if row_index + 1 == 10:
                print("", 10, "  ".join([patch.display(self.mode) for patch in row]))
                break
            print("", row_index + 1, "", "  ".join([patch.display(self.mode) for patch in row]))


    def markPatch(self, location):
        """
        Marks a patch on the board. Returns False if the user chose a marked location \n 
        String -> None/False
        """
        row_index, column_index = Ship.locationSwitch(location)
        target = self.board[row_index][column_index]
        if not target.marked:
            target.marked = True
            if target.shipHere:
                target.deadShip = True
        else:
            return False


    def setup(self):
        """
        Guides user setup for board \n
        None -> None
        """
        print("Board setup: ")
        while True:
            back = False
            ship_id = input("Enter the ID of the ship you want to edit or enter 'exit' to finish: ")
            if ship_id == "exit" and len(self.placed) == 10: 
                break
            elif ship_id == "exit" and len(self.placed) != 10:
                print("Cannot finish, not all ships have been placed yet. ")
                continue
            while ship_id not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', "exit"]:
                ship_id = input("Please enter a valid ship ID or 'exit' to finish: ")
                if ship_id == "exit" and len(self.placed) == 10:
                    back = True
                    break
                elif ship_id == "exit" and not len(self.placed) == 10:
                    print("Cannot finish, not all ships have been placed yet. ")                
            if back:
                break
            ship = self.ships[int(ship_id)]
            while True:
                action = input("Enter 'm' to move or place, 'r' to rotate a ship, 'back' to go back: ")
                while action not in ['m', 'r', 'back']:
                    action = input("Please enter a valid option ('m', 'r', 'back'): ")
                if action == "back":
                    back = True
                    break
                elif action == 'm':
                    location = input("Which location do you want to move the ship to, or 'back' to go back: ").upper()
                    if location == "BACK":
                        continue
                    while not isinstance(Ship.locationSwitch(location), tuple) or not ship.checkLocation(location):
                        location = input("Invalid location or can't be placed here. Please enter a valid location or 'back' to go back: ").upper()
                        if location == "BACK":
                            back = True
                            break
                    if back:
                        continue
                    else:
                        ship.removeShip()
                        ship.moveShip(location)
                        self.placed.append(ship)
                        break        
                elif action == 'r':
                    orientation = input("Which direction do you want the ship to point ('left', 'right', 'up', 'down'), or 'back' to go back: ")
                    while orientation not in ['left', 'right', 'up', 'down', 'back']:
                        orientation = input("Please enter 'left', 'right', 'up', 'down', or 'back': ")
                    if orientation == "back":
                        back = True
                        continue
                    while ship.location == "" and not ship.checkRotate(orientation):
                        orientation = input("Cannot turn ship this way. Try to turn the ship a different way or 'back': ")
                        while orientation not in ['left', 'right', 'up', 'down', 'back']:
                            orientation = input("Please enter 'left', 'right', 'up', 'down', or 'back': ")
                        if orientation == "back":
                            back = True
                            break
                    if ship.location == "":
                        ship.orientation = orientation
                    else: 
                        ship.removeShip()
                        ship.rotate(orientation)
                    continue
                if back:
                    continue
            if back:
                continue             


class Game:


    p1 = Board()
    p2 = Board()


    def __init__(self):
        """
        Assigns the appropriate boards to the ships of each board
        """
        for ship in self.p1.ships:
            ship.board = self.p1
        for ship in self.p2.ships:
            ship.board = self.p2


g1 = Game()
g1.p1.setup()
g1.p1.display()