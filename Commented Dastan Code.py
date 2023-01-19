#Skeleton Program code for the AQA A Level Paper 1 Summer 2023 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.9 programming environment

import random

# The main class, but you don't call the main class main like the main file and the main function because reasons
class Dastan:
    # Initialises objects when the class is called
    def __init__(self, R, C, NoOfPieces):
        # Creates an empty Board
        self._Board = []
        # Creates an empty list for the Players
        self._Players = []
        # Creates an empty list for the move offers
        self._MoveOptionOffer = []
        # Creates 2 players for the Players list, one with direction 1, the other with direction -1
        self._Players.append(Player("Player One", 1))
        self._Players.append(Player("Player Two", -1))
        # Creates the Options for Moving pieces
        self.__CreateMoveOptions()
        # Sets the board size
        self._NoOfRows = R
        self._NoOfColumns = C
        # Initialises the offered move to be in position 0
        self._MoveOptionOfferPosition = 0
        # Adds the five moves to the list of offer options
        self.__CreateMoveOptionOffer()
        # Initialises the Board to have the correct size
        # with P1's Kotla loft of middle, and P2's in the middle or right of middle
        self.__CreateBoard()
        # Places the Mirzas in the Kotlas, and the correct number of Standard pieces on the board
        self.__CreatePieces(NoOfPieces)
        # Sets Player One to go first
        self._CurrentPlayer = self._Players[0]

    # Displays the Board array in an easy to understand way
    def __DisplayBoard(self):
        # Prints an indent to align column numbers
        print("\n" + "   ", end="")
        # Prints the column numbers
        for Column in range(1, self._NoOfColumns + 1):
            print(str(Column) + "  ", end="")
        # Prints an indent to align the top edge of the board
        print("\n" + "  ", end="")
        # Prints the top edge of the board
        for Count in range(1, self._NoOfColumns + 1):
            print("---", end="")
        print("-")
        # Loops over the block of code, once for each row
        for Row in range(1, self._NoOfRows + 1):
            # Prints the Row number
            print(str(Row) + " ", end="")
            # Loops over the block of code, once for each column
            for Column in range(1, self._NoOfColumns + 1):
                # Assigns Index to the index of the square to be printed
                Index = self.__GetIndexOfSquare(Row * 10 + Column)
                # Prints a vBar followed by the symbol of the right square
                print("|" + self._Board[Index].GetSymbol(), end="")
                # Gets the peice in the current square
                PieceInSquare = self._Board[Index].GetPieceInSquare()
                # Prints the piece in the current square
                if PieceInSquare is None:
                    print(" ", end="")
                else:
                    print(PieceInSquare.GetSymbol(), end="")
            # Prints a final vBar for the right edge of the board
            print("|")
        # Prints an indent to align toe bottom edge and starts printing the lower edge
        print("  -", end="")
        # Finishes the lower edge
        for Column in range(1, self._NoOfColumns + 1):
            print("---", end="")
        # Prints two blank lines to separate the board from following text
        print()
        print()

    # Displays the current game state
    def __DisplayState(self):
        # Displays the board
        self.__DisplayBoard()
        # Displays the current offer
        print("Move option offer: " + self._MoveOptionOffer[self._MoveOptionOfferPosition])
        # Leaves a blank line for separation
        print()
        # Displays the score and move option queue
        print(self._CurrentPlayer.GetPlayerStateAsString())
        # Prints the name of the player who's turn it currently is
        print("Turn: " + self._CurrentPlayer.GetName())
        # Prints a blank line for separation
        print()

    # Converts a square's reference number to a list index of the board array
    def __GetIndexOfSquare(self, SquareReference):
        # Extracts the row number from the reference number
        Row = SquareReference // 10
        # Extracts the column number from the reference number
        Col = SquareReference % 10
        # Returns the index number for the board array
        return (Row - 1) * self._NoOfColumns + (Col - 1)

    # Checks a square's reference number if it is within the board
    def __CheckSquareInBounds(self, SquareReference):
        # Extracts the row number from the reference number
        Row = SquareReference // 10
        # Extracts the column number from the reference number
        Col = SquareReference % 10
        # If the row number is out of bounds, return false
        if Row < 1 or Row > self._NoOfRows:
            return False
        # If the column number is out of bounds, return false
        elif Col < 1 or Col > self._NoOfColumns:
            return False
        # Otherwise return true
        else:
            return True

    # Checks if the squares reference number is a valid choice
    def __CheckSquareIsValid(self, SquareReference, StartSquare):
        # returns false if the square is out of bounds
        if not self.__CheckSquareInBounds(SquareReference):
            return False
        # Gets the piece in the square of the reference number
        PieceInSquare = self._Board[self.__GetIndexOfSquare(SquareReference)].GetPieceInSquare()
        # If the starting square of a move is empty, return false
        if PieceInSquare is None:
            if StartSquare:
                return False
            else:
                return True
        # If the target square contains a piece belonging to the current player, return false
        elif self._CurrentPlayer.SameAs(PieceInSquare.GetBelongsTo()):
            if StartSquare:
                return True
            else:
                return False
        # If the piece in the start square doesn't belong to the current player, return false
        else:
            if StartSquare:
                return False
            else:
                return True

    # Checks if the game is over by checking for both player's Mirza's
    # and checks if either of them are in the opposing Kotla
    def __CheckIfGameOver(self):
        # Initialises a flag for each player that will be true if they have a Mirza
        Player1HasMirza = False
        Player2HasMirza = False
        # loops through every position in the board array
        for S in self._Board:
            # Assigns a variable to the piece in the current square
            PieceInSquare = S.GetPieceInSquare()
            # If the square is empty it skips all other checks and goes to the next square
            if PieceInSquare is not None:
                # If a Mirza is in the opposing Kotla, return true (i.e. the game has ended)
                if S.ContainsKotla() and PieceInSquare.GetTypeOfPiece() == "mirza" and not PieceInSquare.GetBelongsTo().SameAs(S.GetBelongsTo()):
                    return True
                # If the piece is P1's Mirza, set the relevant flag to true
                elif PieceInSquare.GetTypeOfPiece() == "mirza" and PieceInSquare.GetBelongsTo().SameAs(self._Players[0]):
                    Player1HasMirza = True
                # If the piece is P2's Mirza, set the relevant flag to true
                elif PieceInSquare.GetTypeOfPiece() == "mirza" and PieceInSquare.GetBelongsTo().SameAs(self._Players[1]):
                    Player2HasMirza = True
        # Return false if both Mirzas are still in play, else return false
        return not (Player1HasMirza and Player2HasMirza)

    # Gets a reference number for the square from the user and returns it
    def __GetSquareReference(self, Description):
        # Gets a reference number for the square from the user
        SelectedSquare = int(input("Enter the square " + Description + " (row number followed by column number): "))
        # and returns it
        return SelectedSquare

    # Replaces a move from a player's queue with the move offer
    def __UseMoveOptionOffer(self):
        # Asks the user which move they want to replace
        ReplaceChoice = int(input("Choose the move option from your queue to replace (1 to 5): "))
        # Updates the player's move queue with the new move
        self._CurrentPlayer.UpdateMoveOptionQueueWithOffer(ReplaceChoice - 1, self.__CreateMoveOption(self._MoveOptionOffer[self._MoveOptionOfferPosition], self._CurrentPlayer.GetDirection()))
        # Reduces the score by the required amount
        self._CurrentPlayer.ChangeScore(-(10 - (ReplaceChoice * 2)))
        # Creates a new move option
        self._MoveOptionOfferPosition = random.randint(0, 4)

    # Used to calculate the total points for the squares occupied by the current player
    def __GetPointsForOccupancyByPlayer(self, CurrentPlayer):
        # Initialises a variable to denote the change in score
        ScoreAdjustment = 0
        # Loops through every position on the board
        for S in self._Board:
            # Adjusts the score for the right value for each tile
            ScoreAdjustment += (S.GetPointsForOccupancy(CurrentPlayer))
        # Returns the final score adjustment
        return ScoreAdjustment

    # Updates the player's score after the events of a turn
    def __UpdatePlayerScore(self, PointsForPieceCapture):
        # Adds the points from occupancy and the points for piece capture to the current player's score
        self._CurrentPlayer.ChangeScore(self.__GetPointsForOccupancyByPlayer(self._CurrentPlayer) + PointsForPieceCapture)

    # Calculates the points gained for capture in one turn
    def __CalculatePieceCapturePoints(self, FinishSquareReference):
        # If the finish square for a move is occupied, return the points earned for capturing that piece
        if self._Board[self.__GetIndexOfSquare(FinishSquareReference)].GetPieceInSquare() is not None:
            return self._Board[self.__GetIndexOfSquare(FinishSquareReference)].GetPieceInSquare().GetPointsIfCaptured()
        # If it isn't occupied, return 0
        return 0

    # The main game loop for the game, only exitable if the GameOver flag is true
    def PlayGame(self):
        # Initialises the GameOver flag to false
        GameOver = False
        # Loops until the GameOver flag is true
        while not GameOver:
            # Displays the current game state
            self.__DisplayState()
            # Initialises the SquareIsValid flag, denoting if a player chooses a valid square, to false
            SquareIsValid = False
            # Initialises the player choice to the invalid choice of 0
            Choice = 0
            # Loops until a valid choice is chosen
            while Choice < 1 or Choice > 3:
                # Asks the user for a choice
                Choice = int(input("Choose move option to use from queue (1 to 3) or 9 to take the offer: "))
                # If the choice is 9, the user takes the offer
                if Choice == 9:
                    # Replaces a move from a player's queue with the move offer
                    self.__UseMoveOptionOffer()
                    # Displays the current game state
                    self.__DisplayState()
            # Loops until a valid square is chosen
            while not SquareIsValid:
                # Gets a reference number for the square containing the piece to move from the user
                StartSquareReference = self.__GetSquareReference("containing the piece to move")
                # Checks if the squares reference number is a valid choice for the square containing the piece to move
                SquareIsValid = self.__CheckSquareIsValid(StartSquareReference, True)
            # Resets the flag to false
            SquareIsValid = False
            # Loops until a valid square is chosen
            while not SquareIsValid:
                # Gets a reference number for the square to move to from the user
                FinishSquareReference = self.__GetSquareReference("to move to")
                # Checks if the squares reference number is a valid choice for the square to move to
                SquareIsValid = self.__CheckSquareIsValid(FinishSquareReference, False)
            # Checks if the chosen move is legal
            MoveLegal = self._CurrentPlayer.CheckPlayerMove(Choice, StartSquareReference, FinishSquareReference)
            # If the move is legal, enact the move
            if MoveLegal:
                # Calculates the points gained for capture in one turn
                PointsForPieceCapture = self.__CalculatePieceCapturePoints(FinishSquareReference)
                # Changes the points for the move selection
                self._CurrentPlayer.ChangeScore(-(Choice + (2 * (Choice - 1))))
                # Updates the move choice queue
                self._CurrentPlayer.UpdateQueueAfterMove(Choice)
                # Updates the board positions at the start point and finish point of the move
                self.__UpdateBoard(StartSquareReference, FinishSquareReference)
                # Updates the player's score after the events of a turn
                self.__UpdatePlayerScore(PointsForPieceCapture)
                # Prints the new score
                print("New score: " + str(self._CurrentPlayer.GetScore()) + "\n")
            # Switches which player's turn it is currently
            if self._CurrentPlayer.SameAs(self._Players[0]):
                self._CurrentPlayer = self._Players[1]
            else:
                self._CurrentPlayer = self._Players[0]
            # Checks if the game is over and assigns the result to the GameOver flag
            GameOver = self.__CheckIfGameOver()
        # Once the game is over, the current state and the final result are both displayed
        self.__DisplayState()
        self.__DisplayFinalResult()

    # Updates the board positions at the start point and finish point of the move
    def __UpdateBoard(self, StartSquareReference, FinishSquareReference):
        self._Board[self.__GetIndexOfSquare(FinishSquareReference)].SetPiece(self._Board[self.__GetIndexOfSquare(StartSquareReference)].RemovePiece())

    # Displays the final result of the game
    def __DisplayFinalResult(self):
        # If the scores are equal, it is a draw
        if self._Players[0].GetScore() == self._Players[1].GetScore():
            print("Draw!")
        # If Player 1 has more points, their name is declared the winner
        elif self._Players[0].GetScore() > self._Players[1].GetScore():
            print(self._Players[0].GetName() + " is the winner!")
        # If Player 2 has more points, their name is declared the winner
        else:
            print(self._Players[1].GetName() + " is the winner!")

    # Creates the initial board state, without pieces
    def __CreateBoard(self):
        # Loops for the number of rows
        for Row in range(1, self._NoOfRows + 1):
            # Loops for the number of columns
            for Column in range(1, self._NoOfColumns + 1):
                # If the current square being set up is in row 1 and is left of centre or central, place Player 1's Kotla
                if Row == 1 and Column == self._NoOfColumns // 2:
                    S = Kotla(self._Players[0], "K")
                # If the current square being set up is in the last row and is reight of centre, place Player 2's Kotla
                elif Row == self._NoOfRows and Column == self._NoOfColumns // 2 + 1:
                    S = Kotla(self._Players[1], "k")
                # Otherwise, place a normal square
                else:
                    S = Square()
                # Add the square to the board
                self._Board.append(S)

    # Sets up the initial pieces in the right places
    def __CreatePieces(self, NoOfPieces):
        # Loops through the number of normal pieces needed to be placed for  P1 on the board
        for Count in range(1, NoOfPieces + 1):
            # Assigns an instance of a new piece for P1 to the CurrentPiece variable
            CurrentPiece = Piece("piece", self._Players[0], 1, "!")
            # Places the CurrentPiece on to the board in the right position
            self._Board[self.__GetIndexOfSquare(2 * 10 + Count + 1)].SetPiece(CurrentPiece)
        # Assigns an instance of a new Mirza for P1 to the CurrentPiece variable
        CurrentPiece = Piece("mirza", self._Players[0], 5, "1")
        # Places the CurrentPiece on to the board in the right position
        self._Board[self.__GetIndexOfSquare(10 + self._NoOfColumns // 2)].SetPiece(CurrentPiece)
        # Loops through the number of normal pieces needed to be placed for  P2 on the board
        for Count in range(1, NoOfPieces + 1):
            # Assigns an instance of a new piece for P2 to the CurrentPiece variable
            CurrentPiece = Piece("piece", self._Players[1], 1, '"')
            # Places the CurrentPiece on to the board in the right position
            self._Board[self.__GetIndexOfSquare((self._NoOfRows - 1) * 10 + Count + 1)].SetPiece(CurrentPiece)
        # Assigns an instance of a new Mirza for P2 to the CurrentPiece variable
        CurrentPiece = Piece("mirza", self._Players[1], 5, "2")
        # Places the CurrentPiece on to the board in the right position
        self._Board[self.__GetIndexOfSquare(self._NoOfRows * 10 + (self._NoOfColumns // 2 + 1))].SetPiece(CurrentPiece)

    # Creates a list of all of the different moves that can be offered
    def __CreateMoveOptionOffer(self):
        # RANT ADDED
        # If you have a bit in your NEA that looks like this, don't
        # It should look like this:
        # self._MoveOptionOffer = ["jazair", "chowkidar", "cuirassier", "ryott", "faujdar"]
        # And frankly, it doesn't need to be a separate function
        # RANT END
        self._MoveOptionOffer.append("jazair")
        self._MoveOptionOffer.append("chowkidar")
        self._MoveOptionOffer.append("cuirassier")
        self._MoveOptionOffer.append("ryott")
        self._MoveOptionOffer.append("faujdar")

    # Creates the 'ryott' (riot) move
    def __CreateRyottMoveOption(self, Direction):
        # Instantiates an instance of a MoveOption called 'ryott'
        NewMoveOption = MoveOption("ryott")
        # Creates a set of new moves and adds them to the possible 'ryott' moves
        NewMove = Move(0, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        # Returns the 'ryott' move
        return NewMoveOption

    # Creates the 'faujdar'(fudgecake) move
    def __CreateFaujdarMoveOption(self, Direction):
        # Instantiates an instance of a MoveOption called 'faujdar'
        NewMoveOption = MoveOption("faujdar")
        # Creates a set of new moves and adds them to the possible 'faujdar' moves
        NewMove = Move(0, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        # Returns the 'faujdar' move
        return NewMoveOption

    # Creates the 'jazair' (jesus) move
    def __CreateJazairMoveOption(self, Direction):
        # Instantiates an instance of a MoveOption called 'jazair'
        NewMoveOption = MoveOption("jazair")
        # Creates a set of new moves and adds them to the possible 'jazair' moves
        NewMove = Move(2 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(2 * Direction, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(2 * Direction, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        # Returns the 'jazair' move
        return NewMoveOption

    # Creates the 'cuirassier' (curious) move
    def __CreateCuirassierMoveOption(self, Direction):
        # Instantiates an instance of a MoveOption called 'cuirassier'
        NewMoveOption = MoveOption("cuirassier")
        # Creates a set of new moves and adds them to the possible 'cuirassier' moves
        NewMove = Move(1 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(2 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        # Returns the 'cuirassier' move
        return NewMoveOption

    # Creates the 'chowkidar' (eat kid pirate) move
    def __CreateChowkidarMoveOption(self, Direction):
        # Instantiates an instance of a MoveOption called 'chowkidar'
        NewMoveOption = MoveOption("chowkidar")
        # Creates a set of new moves and adds them to the possible 'chowkidar' moves
        NewMove = Move(1 * Direction, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        # Returns the 'chowkidar' move
        return NewMoveOption

    # Creates a move option according to the name inputted
    def __CreateMoveOption(self, Name, Direction):
        # If the name is 'chowkidar' return the 'chowkidar' move
        if Name == "chowkidar":
            return self.__CreateChowkidarMoveOption(Direction)
        # If the name is 'ryott' return the 'ryott' move
        elif Name == "ryott":
            return self.__CreateRyottMoveOption(Direction)
        # If the name is 'faujdar' return the 'faujdar' move
        elif Name == "faujdar":
            return self.__CreateFaujdarMoveOption(Direction)
        # If the name is 'jazair' return the 'jazair' move
        elif Name == "jazair":
            return self.__CreateJazairMoveOption(Direction)
        # Else return the 'cuirassier' move
        else:
            return self.__CreateCuirassierMoveOption(Direction)

    # Adds the different move options to the players' move queues
    def __CreateMoveOptions(self):
        # RANT ADDED
        # WHY IS THE EXAM BOARD MAKING AN EXAMPLE WITH SUCH HORIFFIC CODE
        # A 3 YEAR OLD COULD PROBABLY MAKE MORE LOGICAL SENSE
        # USING A KNIFE MADE OUT OF AN ORANGE AND CHEERIOS SOAKED IN WATER
        # END RANT
        # I don't think these need indiviually explaining
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("ryott", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("chowkidar", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("cuirassier", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("faujdar", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("jazair", 1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("ryott", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("chowkidar", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("jazair", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("faujdar", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("cuirassier", -1))

# Defines a class for the pieces
class Piece:
    # Initialises a piece object when the class is called
    def __init__(self, T, B, P, S):
        # Denotes the type of piece
        self._TypeOfPiece = T
        # Denotes who the piece belongs to
        self._BelongsTo = B
        # Denotes the points awarded if captured
        self._PointsIfCaptured = P
        # Denotes the symbol
        self._Symbol = S

    # Returns the symbol
    def GetSymbol(self):
        return self._Symbol

    # Returns the type of piece
    def GetTypeOfPiece(self):
        return self._TypeOfPiece

    # Returns who the piece belongs to
    def GetBelongsTo(self):
        return self._BelongsTo

    # Returns the points awarded if captured
    def GetPointsIfCaptured(self):
        return self._PointsIfCaptured

# Defines a class for the Squares
class Square:
    # Initialises a Square object when the class is called
    def __init__(self):
        # Denotes the piece in the square
        self._PieceInSquare = None
        # Denotes who the occupying piece belongs to
        self._BelongsTo = None
        # Denotes the symbol of the square
        self._Symbol = " "

    # Sets the piece in the square
    def SetPiece(self, P):
        self._PieceInSquare = P

    # Removes the piece in the square and returns the removed pieace
    def RemovePiece(self):
        # Sets the piece to return as the one currently occupying the square
        PieceToReturn = self._PieceInSquare
        # Sets the piece in the square to None (this is basically an empty value, a placeholder)
        self._PieceInSquare = None
        # Returns the removed piece
        return PieceToReturn

    # Returns the piece in the square
    def GetPieceInSquare(self):
        return self._PieceInSquare

    # returns the Symbol of the piece in the square
    def GetSymbol(self):
        return self._Symbol

    # Returns the points for occupying this square, defaulted to 0, but can be overwritten by children
    def GetPointsForOccupancy(self, CurrentPlayer):
        return 0

    # Returns who the occupying piece belongs to
    def GetBelongsTo(self):
        return self._BelongsTo

    # Returns whether the square is a Kotla or not
    def ContainsKotla(self):
        if self._Symbol == "K" or self._Symbol == "k":
            return True
        else:
            return False

# Defines a child class for Kotlas that inherits from the Square class
class Kotla(Square):
    # Initialises a Kotla object when the class is called
    def __init__(self, P, S):
        # Inherits the attributes initialised in the parent Square class
        super(Kotla, self).__init__()
        # Denotes who the Kotla belongs to
        self._BelongsTo = P
        # Denotes which Symbol represents the Kotla
        self._Symbol = S

    # Returns the points receieved for occupying the Kotla this turn
    def GetPointsForOccupancy(self, CurrentPlayer):
        # If there is nothing in the Kotla, return 0
        if self._PieceInSquare is None:
            return 0
        # If the owner of the Kotla is taking their turn, execute the following code
        elif self._BelongsTo.SameAs(CurrentPlayer):
            # If the current player is the same as the owner of the piece in the Kotla
            # and the piece in the Kotla is either a normal piece or a Mirza return 5, else return 0
            if CurrentPlayer.SameAs(self._PieceInSquare.GetBelongsTo()) and (self._PieceInSquare.GetTypeOfPiece() == "piece" or self._PieceInSquare.GetTypeOfPiece() == "mirza"):
                return 5
            else:
                return 0
        # If the owner of the Kotla is not taking their turn, execute the following code
        else:
            # If the current player is the same as the owner of the piece in the Kotla
            # and the piece in the Kotla is either a normal piece or a Mirza return 1, else return 0
            if CurrentPlayer.SameAs(self._PieceInSquare.GetBelongsTo()) and (self._PieceInSquare.GetTypeOfPiece() == "piece" or self._PieceInSquare.GetTypeOfPiece() == "mirza"):
                return 1
            else:
                return 0

# Defines a class for Move types
class MoveOption:
    # Initialiases a MoveOption object with a name, but an empty possible moves list
    def __init__(self, N):
        # Denotes the name of a move
        self._Name = N
        # Denotes the set of possible moves under this move type
        self._PossibleMoves = []

    # Adds possible moves to the PossibleMoves list
    def AddToPossibleMoves(self, M):
        self._PossibleMoves.append(M)

    # Returns the name of the move type
    def GetName(self):
        return self._Name

    # Checks if the move given is a valid move under this move type
    def CheckIfThereIsAMoveToSquare(self, StartSquareReference, FinishSquareReference):
        # Converts the Start position and Finish position to a square reference number
        StartRow = StartSquareReference // 10
        StartColumn = StartSquareReference % 10
        FinishRow = FinishSquareReference // 10
        FinishColumn = FinishSquareReference % 10
        # Loops through all of the possible moves under this move type
        for M in self._PossibleMoves:
            # If the move gets a piece from the start position to the finish position, return True
            if StartRow + M.GetRowChange() == FinishRow and StartColumn + M.GetColumnChange() == FinishColumn:
                return True
        # Return false if no moves under this move type get a piece from the start position to the finish position
        return False

# Define a class for individual moves
class Move:
    # Initialises a Move object
    def __init__(self, R, C):
        # Denotes how the row changes with this move
        self._RowChange = R
        # Denotes how the column changes with this move
        self._ColumnChange = C

    # Returns how the row changes with this move
    def GetRowChange(self):
        return self._RowChange

    # Returns how the column changes with this move
    def GetColumnChange(self):
        return self._ColumnChange

# Defines a class for the move option queue
class MoveOptionQueue:
    # Initialises a MoveOptionQueue object
    def __init__(self):
        # Denotes the contents of the queue
        self.__Queue = []

    # Returns the queue as a string
    def GetQueueAsString(self):
        # Initialises a string to hold the queue
        QueueAsString = ""
        # Initialises a count for which position in the queue the loop is currently at
        # NOTE ADDED
        # There is a built-in called enumerate() that would make this better
        # END NOTE
        Count = 1
        # Loops through the queue
        for M in self.__Queue:
            # Adds to the end of the string, the position in the queue, a '. ', the name of the move and a space
            # May look like this: '4. ryott   '
            QueueAsString += str(Count) + ". " + M.GetName() + "   "
            # Increments the count
            Count += 1
        # Returns the string
        return QueueAsString

    # Adds a new move option to the queue
    def Add(self, NewMoveOption):
        self.__Queue.append(NewMoveOption)

    # Replace a position in the queue with a new move option
    def Replace(self, Position, NewMoveOption):
        self.__Queue[Position] = NewMoveOption

    # Moves an item in the queue to the back
    def MoveItemToBack(self, Position):
        Temp = self.__Queue[Position]
        self.__Queue.pop(Position)
        self.__Queue.append(Temp)

    # Returns the move option in a given position
    def GetMoveOptionInPosition(self, Pos):
        return self.__Queue[Pos]

# Defines the Player class
class Player:
    # Initialises a Player object
    def __init__(self, N, D):
        # Denotes the current score of the Player
        self.__Score = 100
        # Denotes the name of the Player
        self.__Name = N
        # Denotes which way the Player is facing in terms of the board
        self.__Direction = D
        # Holds the Queue for the Player's move options
        self.__Queue = MoveOptionQueue()

    # Returns if a Player is the same as the Player
    def SameAs(self, APlayer):
        # If the Player given is Non-existant, return false
        if APlayer is None:
            return False
        # If the name of the given Player is the same as the name of the Player, return True
        elif APlayer.GetName() == self.__Name:
            return True
        else:
            return False

    # Returns the Name, Score and Move Queue as a string
    # May look like this:
    # 'John'
    # 'Score: 100'
    # 'Move option queue: 1. ryott   2. chowkidar   3. cuirassier   4. faujdar   5. jazair'
    def GetPlayerStateAsString(self):
        return self.__Name + "\n" + "Score: " + str(self.__Score) + "\n" + "Move option queue: " + self.__Queue.GetQueueAsString() + "\n"

    # Adds a new move to the Player's Move Queue
    def AddToMoveOptionQueue(self, NewMoveOption):
        self.__Queue.Add(NewMoveOption)

    # Moves an item in the Move Queue to the back after a move has been taken
    def UpdateQueueAfterMove(self, Position):
        self.__Queue.MoveItemToBack(Position - 1)

    # Replaces an item in the Move Queue with a taken offer
    def UpdateMoveOptionQueueWithOffer(self, Position, NewMoveOption):
        self.__Queue.Replace(Position, NewMoveOption)

    # Returns the Player's Score
    def GetScore(self):
        return self.__Score

    # Returns the Player's Name
    def GetName(self):
        return self.__Name

    # Return's the Player's Direction
    def GetDirection(self):
        return self.__Direction

    # Changes the Score by a given amount, positive or negative
    def ChangeScore(self, Amount):
        self.__Score += Amount

    # Checks if the Player's move is valid
    def CheckPlayerMove(self, Pos, StartSquareReference, FinishSquareReference):
        # Assigns the Move option in the given position to a temporary variable
        Temp = self.__Queue.GetMoveOptionInPosition(Pos - 1)
        # Checks if the move given is a valid move under the given Move option
        return Temp.CheckIfThereIsAMoveToSquare(StartSquareReference, FinishSquareReference)

# Is the main function
def Main():
    # Creates an instance of Dastan with 6 rows, 6 columns and 4 standard pieces given to each player
    ThisGame = Dastan(6, 6, 4)
    # Runs the main game loop of the Dastan instance, only exiting the loop when the game is over
    ThisGame.PlayGame()
    # Outputs the word goodbye with an exclamation mark on the end
    # May look like this:
    # 'Goodbye!'
    print("Goodbye!")
    # Leaves the game on an input, allowing the game to be rerun if the user wishes
    input()

# If the programme is the one being run, rather than imported, run the main function
if __name__ == "__main__":
    Main()
