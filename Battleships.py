import os


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


    def __init__(self, length, orientation, board = "", location = ""): #up, down, left, right
        self.length = length
        self.orientation = orientation
        self.board = board
        self.location = location
        self.alive = True


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
    
    
    @staticmethod
    def neighbors(ship_span_indexes):
        """
        Returns a list of tuples containing the indexes of the neighbors of a ship\n
        list -> list
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
                neighbors.extend([(row_index, column_index - 1), (row_index, column_index + 1), (row_index + 1, column_index + 1), (row_index + 1, column_index - 1), (row_index + 1, column_index)])
            elif column_index == 9:
                neighbors.extend([(row_index - 1, column_index-1), (row_index - 1, column_index), (row_index, column_index - 1), (row_index + 1, column_index - 1), (row_index + 1, column_index)])
            elif row_index == 9:
                neighbors.extend([(row_index - 1, column_index-1), (row_index - 1, column_index), (row_index - 1, column_index + 1), (row_index, column_index - 1), (row_index, column_index + 1)])
            else:
                neighbors.extend([(row_index - 1, column_index-1), (row_index - 1, column_index), (row_index - 1, column_index + 1), (row_index, column_index - 1), (row_index, column_index + 1), (row_index + 1, column_index - 1), (row_index + 1, column_index), (row_index + 1, column_index + 1)])
        return neighbors


    def shipSpanRetrieve(self, location = None, orientation = None):
        """
        Returns a list of tuples containing the indexes of the board that a ship occupies\n
        None -> List
        """   
        if isinstance(location, str):
            row_index, column_index = Ship.locationSwitch(location)
        else:
            row_index, column_index = Ship.locationSwitch(self.location)
        ship_span_indexes = []
        if orientation is None: 
            if self.orientation == "up": #the tail points up
                ship_span_indexes += [(row_index - row, column_index) for row in range(self.length)]
            elif self.orientation == "down":
                ship_span_indexes += [(row_index + row, column_index) for row in range(self.length)]
            elif self.orientation == "left":
                ship_span_indexes += [(row_index, column_index - column) for column in range(self.length)]
            elif self.orientation == "right":
                ship_span_indexes += [(row_index, column_index + column) for column in range(self.length)]
        else: 
            if orientation == "up": #the tail points up
                ship_span_indexes += [(row_index - row, column_index) for row in range(self.length)]
            elif orientation == "down":
                ship_span_indexes += [(row_index + row, column_index) for row in range(self.length)]
            elif orientation == "left":
                ship_span_indexes += [(row_index, column_index - column) for column in range(self.length)]
            elif orientation == "right":
                ship_span_indexes += [(row_index, column_index + column) for column in range(self.length)]     
        return ship_span_indexes


    def checkLocation(self, location): 
        """
        Accepts patch to check if that new location can hold that ship\n
        String -> Boolean
        """
        if location == "BACK":
            return False
        ship_span = []
        ship_span_indexes = self.shipSpanRetrieve(location = location)
        neighbors = Ship.neighbors(ship_span_indexes) 
        deadzone = list(filter(lambda a : a != self, ship_span_indexes)) + neighbors
        for row, column in deadzone:
            if row < 0 or column < 0:
                return False
            try:
                ship_span.append(self.board.board[row][column])
            except IndexError:
                return False
        return True not in [isinstance(patch.shipHere, Ship) for patch in ship_span]


    def removeShip(self, rotate = False):
        """
        Sets all the patches that the ship occupies to not be occupied anymore. Goes before move and rotate.\n
        None -> None
        """
        if self.location == "":
            return 
        row_index, column_index = Ship.locationSwitch(self.location)
        self.board.board[row_index][column_index].headShipHere = False
        ship_span_indexes = self.shipSpanRetrieve(location = self.location)
        for row, column in ship_span_indexes:
            self.board.board[row][column].shipHere = False
        if not rotate:
            self.location = ""


    def moveShip(self, location): #runs after computer checks if the location is available
        """
        After a location is validated for a ship, this function sets the shipHere for all the \n
        patches the ship will occupy to the ship obect and sets the headShipHere value for the head ship \n
        to be the ship object
        String -> None
        """
        self.location = location
        row_index, column_index = Ship.locationSwitch(location)
        self.board.board[row_index][column_index].headShipHere = self 
        ship_span_indexes = self.shipSpanRetrieve(location = location)
        for row, column in ship_span_indexes:
            self.board.board[row][column].shipHere = self


    def checkRotate(self, orientation):
        """
        Checks if the hypothetical patches a ship will occupy if it is rotated is valid \n
        String -> Boolean
        """
        if orientation == self.orientation:
            return True
        ship_span = []
        ship_span_indexes = self.shipSpanRetrieve(orientation = orientation)
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
        ship_span_indexes = self.shipSpanRetrieve(orientation = orientation)
        for row, column in ship_span_indexes:
            self.board.board[row][column].shipHere = self


class Board:


    def __init__(self):
        self.mode = "setup" # hidden, setup, playing
        self.board = [[Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()], 
                [Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()], 
                [Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()], 
                [Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()], 
                [Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()], 
                [Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()], 
                [Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()], 
                [Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()], 
                [Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()], 
                [Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch(), Patch()]]
        self.ships = (Ship(1, "up"), 
                Ship(1, "up"), 
                Ship(1, "up"), 
                Ship(1, "up"), 
                Ship(2, "up"), 
                Ship(2, "up"), 
                Ship(2, "up"), 
                Ship(3, "up"), 
                Ship(3, "up"), 
                Ship(4, "up"))
        self.placed = {}


    def isSunken(self, location):
        """
        Returns if all a ship's patches have been marked\n
        String -> Boolean
        """
        row_index, column_index = Ship.locationSwitch(location)
        ship = self.board[row_index][column_index].shipHere
        return False not in [self.board[row][index].deadShip for row, index in ship.shipSpanRetrieve()]


    def showNotPlaced(self):
        """
        Prints out the ships that the user has not placed yet\n
        None -> None
        """
        print("Ships not placed:")
        not_placed = [ship for ship in self.ships if ship not in self.placed]
        ship_string = ""
        for ship in not_placed:
            ship_string += f"ID: {self.ships.index(ship)} Length: {ship.length} Orientation: {ship.orientation}\n"
        print(ship_string)


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
        String -> Bool
        """
        row_index, column_index = Ship.locationSwitch(location)
        target = self.board[row_index][column_index]
        if not target.marked:
            target.marked = True
            if target.shipHere:
                target.deadShip = True
            return True
        else:
            return False
        

    def markNeighbors(self, location):
        """
        Marks all the ships around a ship\n
        String -> None
        """
        row_index, column_index = Ship.locationSwitch(location)
        ship = self.board[row_index][column_index].shipHere
        ship_span_indexes = ship.shipSpanRetrieve()
        neighbors = Ship.neighbors(ship_span_indexes)
        alphabet = "ABCDEFGHIJ"
        neighbors_locations = []
        for row, column in neighbors:
            neighbors_locations.append(alphabet[column] + str(row + 1))
        for location in neighbors_locations:
            self.markPatch(location)
            
                    
    def setup(self):
        """
        Guides user setup for board \n
        None -> None
        """
        while True:
            print("Board setup: ")
            back = False
            self.display()
            self.showNotPlaced()
            ship_id = input("Enter the ID of the ship you want to edit or enter 'exit' to finish: ")
            self.placed = set(self.placed)
            self.placed = list(self.placed) 
            if ship_id == "exit" and len(self.placed) == 10: 
                break
            elif ship_id == "exit" and len(self.placed) != 10:
                print("Cannot finish, not all ships have been placed yet. ")
                continue
            while ship_id not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', "exit"]:
                ship_id = input("Please enter a valid ship ID or 'exit' to finish: ")
                if ship_id == "exit" and len(self.placed) == 10:
                    self.display()
                    back = True
                    break
                elif ship_id == "exit" and not len(self.placed) == 10:
                    print("Cannot finish, not all ships have been placed yet. ")                
            if back:
                break
            ship = self.ships[int(ship_id)]
            while True:
                self.display()
                action = input("Enter 'm' to move or place, 'r' to rotate a ship, 'back' to go back: ")
                self.display()
                while action not in ['m', 'r', 'back']:
                    action = input("Please enter a valid option ('m', 'r', 'back'): ")
                if action == "back":
                    back = True
                    break
                elif action == 'm':
                    location = input("Which location do you want to move the ship to, or 'back' to go back: ").upper()
                    if location == "BACK":
                        continue
                    if ship.location != "":
                        ship.removeShip()
                    while not isinstance(Ship.locationSwitch(location), tuple) or not ship.checkLocation(location=location):
                        location = input("Invalid location or can't be placed here. Please enter a valid location or 'back' to go back: ").upper()
                        if location == "BACK":
                            back = True
                            break
                    if back:
                        continue
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
                    while ship.location != "" and not ship.checkRotate(orientation):
                        orientation = input("Cannot turn ship this way. Try to turn the ship a different way or 'back': ")
                        while orientation not in ['left', 'right', 'up', 'down', 'back']:
                            orientation = input("Please enter 'left', 'right', 'up', 'down', or 'back': ")
                        if orientation == "back":
                            back = True
                            break
                    if back:
                        break
                    if ship.location == "":
                        ship.orientation = orientation
                    else: 
                        ship.removeShip(rotate = True)
                        ship.rotate(orientation)
                    break
                self.display()
                if back:
                    continue
            if back:
                continue
            os.system('cls')


    def countDead(self):
        """
        Returns the number of dead ships in the board. \n
        None -> int 
        """         
        count = 0 
        for row in self.board:
            count += len(list(filter(lambda a : a.deadShip, row)))
        return count


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


    def setupManager(self):
        """
        Initiates ship setup\n
        None -> None
        """
        print("Player one setup: ")
        self.p1.setup()
        os.system('cls')
        print("Player two setup: ")
        self.p2.setup()
        os.system('cls')


    def play(self):
        """
        Plays the game\n
        None -> None
        """
        self.setupManager()
        while self.p1.countDead() != 20 and self.p2.countDead() != 20:
            confirm_1 = input("Player 1 ready (enter anything): ")
            self.p2.mode = "hidden"
            self.p1.mode = "playing"
            self.p2.display()
            print()
            self.p1.display()
            print()
            location = input("Location to attack: ").upper()
            while Ship.locationSwitch(location) == False or (isinstance(Ship.locationSwitch(location), tuple) and not self.p2.markPatch(location)):
                location = input("Invalid location or location already marked, choose another location: ").upper()
            self.p2.markPatch(location)
            self.p2.display()
            print()
            self.p1.display()
            print()
            row, column = Ship.locationSwitch(location)
            while self.p2.board[row][column].shipHere and self.p2.countDead() != 20: 
                os.system('cls')
                if self.p2.isSunken(location): 
                    self.p2.markNeighbors(location)
                self.p2.display()
                print()
                self.p1.display()
                print()
                location = input("Location to attack: ").upper()
                while Ship.locationSwitch(location) == False or (isinstance(Ship.locationSwitch(location), tuple) and not self.p2.markPatch(location)):
                    location = input("Invalid location or location already marked, choose another location: ").upper()
                self.p2.markPatch(location)
                self.p2.display()
                print()
                self.p1.display()
                print()
                row, column = Ship.locationSwitch(location)
            if self.p2.countDead() != 20:
                done = input("Player 1 done (enter anything): ")
            os.system('cls')
            if self.p2.countDead() != 20:
                confirm_2 = input("Player 2 ready (enter anything): ")
                self.p1.mode = "hidden"
                self.p2.mode = "playing"
                self.p1.display()
                print()
                self.p2.display()
                print()
                location = input("Location to attack: ").upper()
                while Ship.locationSwitch(location) == False or (isinstance(Ship.locationSwitch(location), tuple) and not self.p1.markPatch(location)):
                    location = input("Invalid location or location already marked, choose another location: ").upper()
                os.system('cls')
                self.p1.markPatch(location)
                self.p1.display()
                print()
                self.p2.display()
                print()
                row, column = Ship.locationSwitch(location)
                while self.p1.board[row][column].shipHere and self.p1.countDead() != 20:     
                    os.system('cls')
                    if self.p1.isSunken(location): 
                        self.p1.markNeighbors(location)
                    self.p1.display()
                    print()
                    self.p2.display()
                    print()
                    location = input("Location to attack: ").upper()
                    while Ship.locationSwitch(location) == False or (isinstance(Ship.locationSwitch(location), tuple) and not self.p1.markPatch(location)):
                        location = input("Invalid location or location already marked, choose another location: ").upper()
                    os.system('cls')
                    self.p1.markPatch(location)
                    self.p1.display()
                    print()
                    self.p2.display()
                    print()
                    row, column = Ship.locationSwitch(location)
                if self.p1.countDead() != 20:
                    done = input("Player 2 done (enter anything): ")
                os.system('cls')
        if self.p1.countDead() == 20:
            print("Player two wins!")
        else:
            print("Player one wins!")
            

g1 = Game()
g1.play()



