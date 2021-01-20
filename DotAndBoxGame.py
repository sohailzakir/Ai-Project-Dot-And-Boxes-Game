import random
import copy
import math
import time


class dotsboxes(object):
    ''' Dictates the game: has 2 real major functions: render a game, and make
    a play. It keeps track of score and can check for scores given a game board
    '''
    def __init__(self, rows, columns):
        '''
        Main game components:
            play dictionary -- self.play_dict: has all of the possible moves 
            that can be played. a "0" indicates an open spot, and a "1" 
            one that is filled.
            
            score dictionary -- self.score_dict: has all the possible score
            "boxes" that can be 1. An "A" or "B" represents a player score,
            while a "0" indicate an open score.
            
            column and row counts keep track of the game board size
            While a_score and b_score are integers that represent A's score
            and B's scores respectively.
        '''
        #Creates the possible horizontal plays
        self.play_dict = {}
        for i in range((rows)):
            for j in range(columns-1):
                self.play_dict[((j+(i*columns)), j+(i*columns)+1)] = 0
        
        #creates the possible vertical plays
        for i in range(rows-1):
            for j in range (columns):
                self.play_dict[(j+(i*columns), j+columns+(i*columns))] = 0
        self.score_dict = {}
        
        for i in range((rows-1)): #Rows 
            for j in range(columns-1): #columns
            #The code bellow then generates each possible square, represented
            #as a set of tuples using the same description method as specified
            #for the play dictionary
                box = [(j + i*columns, j+i*columns +1)]
                box.append((box[0][0], box[0][1] + columns - 1))
                box.append((box[0][0] + 1, box[0][1] + columns))
                box.append((box[0][0] + columns, box[2][1]))
                self.score_dict[tuple(box)] = 0
        
        #row and column counts
        self.row_count = rows
        self.column_count = columns
        
        #scorekeeping
        self.a_score = 0
        self.b_score = 0
        
    def render_row(self, i):
        ''' Helper function to render. It renders the rows that have numbers.
        '''
        #keeps track of the leftmost and rightmost number
        left = (i * self.column_count)
        right = left + 1
        for j in range(self.column_count - 1):
            if self.play_dict[(left, right)] == 0:
                #if not, it just prints the text
                print("{:^3d}".format(left), end = "   ") 
            else: #if true, it adds a dash to show the line has been played
                print("{:^3d} -".format(left), end = " ")
            left = right
            right = left + 1
        print("{:^3d}".format(left))
        
    def render_vertical(self, upper_left, upper_right):
        '''helper function to render_middle_row. represents all moves that
        are vertical. '''
        if self.play_dict[(upper_left, upper_right)] == 0:
            print("  ", end = " ")
        else:
            print(" |", end = " ")
    
    def render_middle_row(self, i):
        '''
        Helper function to render. Represents all the rows that do not have
        numbers themselves, but have vertical plays.'''
        
        #renders one square at time the following directions
        upper_left = (i * self.column_count)
        upper_right = upper_left + 1
        bottom_left = upper_left + self.column_count
        bottom_right = bottom_left + 1
        
        for j in range(self.column_count - 1):
            #renders the sides
            self.render_vertical(upper_left, bottom_left)
            
            #represents whether or not there are scores in the box
            top = (upper_left, upper_right)
            left = (upper_left, bottom_left)
            right = (upper_right, bottom_right)
            bottom = (bottom_left, bottom_right)
            score = self.score_dict[(top, left, right, bottom)]
            
            if score == 0:
                print("  ", end = " ")
            else: 
                print(" " + score, end = " ")
            
            #shifts one to the right to render the next box
            upper_left, bottom_left = upper_right, bottom_right
            upper_right += 1
            bottom_right += 1
        self.render_vertical(upper_left, bottom_left)
        print()
        
    
    def render(self):
        '''
        prints out a representation of the game as it currently is, including
        the board, the made moves, and the scores.
        '''
        #The iteration of i goes through the rows of the grid
        for i in range(self.row_count - 1):
        #While the iteration of j goes through the columns of the grid
        #The block of code below goes through the horizontal plays
            self.render_row(i)
            self.render_middle_row(i)
            
        self.render_row(self.row_count - 1)
        print("\nPlayer A: {} Player B: {}".format(self.a_score, self.b_score))
        
    def check_for_scores(self, player_a):
        ''' checks if a score had been awarded. Takes as input if it's player
        a or not player a. Adds scores if necessary.'''
        player = "A" if player_a else "B"
        
        #checks all moves that have been made and the possible scoring plays
        taken_set = {i for i in self.play_dict if self.play_dict[i] == 1}
        open_scores = [i for i in self.score_dict if self.score_dict[i] == 0]
        
        #sets the score counter to 0
        score_counter = 0
        
        
        for box in open_scores:
            #if a new score is found:
            if set(box).issubset(taken_set):
                score_counter += 1
                #keeps track of the score in the dict:
                self.score_dict[box] = player
        return(score_counter) #returns the score
                
    
    def make_play(self, start_point, end_point, player_a):
        ''' Takes as input a start point and an end point, along with if 
        the player is player a or not. Adds the play to the play dictionary
        and then checks for scores. If an invalid entry is given, it returns
        false. '''
        try:
            #makes sure that the play isn't already played
            if self.play_dict[(start_point, end_point)] == 1:
                return(False)
        except KeyError: #in case that the move doesn't exist
            return(False)
        
        #marks down the play
        self.play_dict[(start_point, end_point)] = 1
        #checks if a scoring move has been played
        score = self.check_for_scores(player_a)
        if player_a:
            self.a_score += score
        else:
            self.b_score += score
        return(True)
            
    def get_open_plays(self):
        ''' Returns a list of available plays'''
        return([i for i in self.play_dict if self.play_dict[i] == 0])
        
    def isover(self):
        '''returns whether or not if the game is over as bool'''
        return(self.a_score + self.b_score == len(self.score_dict))
        
class random_player(object):
    ''' Random player that makes a random move based on the plays available
    alone. '''
    def __init__(self, player_a):
        #knows if it's player a or b
        self.player = player_a
        
    def make_play(self, game):
        '''retrives the list of available plays, chooses 1 randomly, and uses
        it as its move'''
        list_of_plays = game.get_open_plays()
        play = random.choice(list_of_plays)
        game.make_play(*play, self.player)
        player = "A" if self.player else "B"
        print("Player {}'s move: {} {}".format(player, *play))

class human_player(object):
    '''interface between game and human player takes inputs and enters them
    into the game baord. '''
    def __init__(self, player_a):
        #keeps track of playername as both bool and string
        self.player_a = player_a
        self.playername = "A" if player_a else "B"
    
    def make_play(self, game):
        '''Allows the player to enter in a play as input. Loops until a valid
        input is given. '''
        while True:
            move = input("Player {}, make your move (start point end point):"\
                         .format(self.playername))
            move = move.split()
            try:
                move[0], move[1] = int(move[0]), int(move[1])
                if len(move) != 2: #too long entry
                    print("Error. Input must be of form start point, endpoint")
            
            except NameError: 
                print("Error. Input must be of form start point, endpoint")
                continue
            except IndexError: #too short of an entry
                print("Error. Input must be of form start point, endpoint")
                continue
            except ValueError: #enters non integer entry
                print("Error. Input must be of form start point, endpoint")
                continue
            move.sort() #makes sure it's not too long
            valid_move = game.make_play(*move, self.player_a)
            if valid_move:
                return()
            print("Error. That move does not exist. Try again")
        
        
class alphabeta_player(object):
    '''player that uses the minimax algorithm to play: that is, it assumes
    the opponent is trying to  maximize their own score, which means the
    algorthm does a depth first search finding the best score given that
    constraint. Note that with alpha beta pruning, it will never go down 
    a branch that's going to guarentee a lesser score. More on the minimax
    algorithm with alphabeta pruning can be found here:
        https://en.wikipedia.org/wiki/Minimax
        https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning'''
    def __init__(self, player_a):
        self.player = player_a
        
    def alphabeta(self, game, play, depth, alpha, beta, player_a):
        '''recursive algorthm that tries to maximize the player's score'''
        if (game.isover()) or depth == 0:
            #returns score if at end of tree
            return((game.a_score - game.b_score, play))
        if player_a: #maximizing player
            value = -math.inf 
            for move in game.get_open_plays():
                #the folowing creates a new game with a given move
                new_game = copy.deepcopy(game)
                old_score = new_game.a_score
                new_game.make_play(*move, True)
                new_score = new_game.a_score
                
                '''The following is the recursvie step. Note, that the game
                allows for a scoring player to go again.'''
                if new_score == old_score:
                    new_play_results = self.alphabeta(new_game, move, \
                                            depth - 1, alpha, beta, False)
                else:
                    new_play_results = self.alphabeta(new_game, move, \
                                            depth - 1, alpha, beta, True)
                    
                #keeps the best outcome
                if value >= new_play_results[0]:
                    play = move
                    value = new_play_results[0]
                
                #prunes branches that will not bring out the best score
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return(value, play)
        
        else:
            #the same as above, but assuming the player is trying to minimize
            value = math.inf
            for move in game.get_open_plays():
                
                new_game = copy.deepcopy(game)
                old_score = new_game.b_score
                new_game.make_play(*move, False)
                new_score = new_game.b_score
                
                if new_score == old_score:
                    move_results = self.alphabeta(new_game, move, depth-1, \
                                                  alpha, beta, True)
                else:
                    move_results = self.alphabeta(new_game, move, depth-1, \
                                                  alpha, beta, False)
                
                if value <= move_results[0]:
                    play = move
                    value = move_results[0]
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return(value, play)
    
    def make_play(self, game):
        '''Makes a play on the board using the alpha beta algorithm'''
        start_time = time.time()
        
        #calculates the rough amount of time it will take to make a decision
        play_space_size = len(game.get_open_plays())
        if play_space_size == 1:
            play = random.choice(game.get_open_plays())
            game.make_play(*play, self.player)
            return()
        #depth that guarentees a maximum of 5 minutes of thinking
        depth = math.floor(math.log(19000, play_space_size))
        
        #first step in the recursive algorithm
        play = self.alphabeta(game, (0, 0), depth, -math.inf, math.inf, \
                              self.player)[1]
        elapsed = time.time() - start_time
        
        #plays randomly if the algorithm finds nothing exceptional
        if play == (0, 0): 
            play = random.choice(game.get_open_plays())
        game.make_play(*play, self.player) #actually playing the game
        
        #prints how they played
        player = "A" if self.player else "B"
        print("Player {}'s move: {} {}".format(player, *play))
        print("Time elapsed to make move: {}".format(elapsed))
        

class game(object):
    ''' Contains the players and the gameplay itself. Uses the previously
    defined dotsboxes and player classes. '''
    
    def __init__(self, player_a_type = "random" , player_b_type = "random", \
                 rows = 5, columns = 5):
        '''Contains:
        rows count
        columns count
        a player a class
        a player b class
        and a dotboxes game'''
        
        self.rows = rows
        self.columns = columns
        
        #initializing player A:
        if player_a_type == "random":
            self.player_a = random_player(True)
        elif player_a_type == "alphabeta":
            self.player_a = alphabeta_player(True)
        else:
            self.player_a = human_player(True)
            
        #initializing player B:
        if player_b_type == "random":
            self.player_b = random_player(False)
        elif player_b_type == "alphabeta":
            self.player_b = alphabeta_player(False)
        else:
            self.player_b = human_player(False)
        
    def play_game(self):
        ''' Flips a coin to determines who goes first. Then alternates players
        until the game is over.'''
        
        #instantiates dotboxes class
        game = dotsboxes(self.rows, self.columns)
        
        print()
        game.render()
        print()
        
        #tosses a coin. 1 = heads, 2 = tails
        coin_toss = random.randint(1, 2)
        print("The coin landed on {}".\
              format("heads" if coin_toss == 1 else "tails"))
        print("Player {} goes first".format("A" if coin_toss == 1 else "B"))
        print()
            
        #loops until the game is over
        while not(game.isover()):
            
            #loops until the player doesn't score a point
            while not(game.isover()):
                #player B goes first if it lands on tails.
                if coin_toss == 2:
                    coin_toss = 3
                    break
                old_score = game.a_score
                self.player_a.make_play(game)
                game.render()
                if old_score == game.a_score:
                    break
            
            #same as above but for player b.
            while not(game.isover()):
                old_score = game.b_score
                self.player_b.make_play(game)
                game.render()
                if old_score == game.b_score:
                    break
        
        #returns the results
        if game.a_score == game.b_score:
            print("It's a tie!")
        elif game.a_score >= game.b_score:
            print("A wins!")
        else:
            print("B wins!")
                
def main():
    print("Welcome to dots and boxes!")
    print("Rules about the game can be found here:"\
          "https://en.wikipedia.org/wiki/Dots_and_Boxes")
    
    #main driving loop. allows replay
    loop = "y"
    while loop == "y":
        
        #choose between random player and intelligent player.
        playtype = input("Press r to play against a random player. "\
                         "Press i for a more intelligent one.(Intelligent "\
                         "takes player ~5-10 seconds to think): ").lower()
        
        #error message
        if (playtype != "r") and (playtype != "i"):
            print("Invalid game type. Please try again")
            continue
        
        #assigns computer player type
        player_b = "alphabeta" if playtype == "i" else "random"
        
        #loops until game is properly set up.
        while True:
            #max 1000 nodes. 5000 is the minimum for that
            rows = input("How many rows should the grid have? "\
                         "(limit 500): ")
            #error -- too many rows
            try:
                rows = int(rows)
                if rows > 500:
                    print("Too many rows! Please try again (limit 500)")
                    continue
            except ValueError:
                print("Not an integer. Please try again.")
                continue
            break
        while True:
            #makes sure maximum row count isn't met
            limit = math.floor(min(16, 9999/rows))
            columns = input("How many columns should the grid have?" \
                            "(limit {}): ".format(limit))
            try:
                columns = int(columns)
                if columns > limit:
                    print("Too many columns! Try again (limit {})"\
                          .format(limit))
                    continue
            except ValueError:
                print("That is not an integer value! try again")
                continue
            break
        
        gameplay = game("Human", player_b, rows, columns)
        gameplay.play_game()
        
        loop = input("Play again?(y/n): ")
        
    print("Thank you for playing! c:")
    

if __name__ == "__main__":
    main()