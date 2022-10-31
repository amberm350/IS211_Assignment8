import argparse
import random
import datetime


def throw_the_die(sides=6):
   
    return random.randint(1, sides)


class Player:
    def __init__(self, name):
        self.name = name
        self.total = 0

    def show(self):
        print(f"{self}")

    def __str__(self):
        
        return f"{self.name}'s Total = {self.total}"

    def turn(self):
        turn_total = 0
        roll_hold = 'r'
        while roll_hold != "h":
            die = throw_the_die()
            if die == 1:
                print ("You rolled a 1, next players turn")
                break

            turn_total += die
            print (f"The turn total is {turn_total}")
            print (f"The possible total if you hold is {self.total + turn_total}")
            print (f"The real total is {die}")
            
            roll_hold = input("Roll(r) or Hold(h)? ").lower()

        if roll_hold == 'h':
            
            self.total += turn_total

        self.show()


class ComputerPlayer(Player):

    def __init__(self, name):
        super().__init__(name)

    def turn(self):
        turn_total = 0
        scratch = False
        while turn_total <= min(25, 100 - self.total):
            die = throw_the_die()
            if die == 1:
                print (f"{self.name} player rolled a 1, next players turn")
                scratch = True
                break

            turn_total += die
            print (f"The turn total is {turn_total}")
            print (f"The possible total if you hold is {self.total + turn_total}")
            print (f"The real total is {self.total}")

        if not scratch:
            self.total += turn_total

        self.show()


class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_player= self.players[0]
        self.winner = None

    def check_winner(self):
        
        for player in self.players:
            if player.total >= 100:
                self.winner = player
                return True
        return False

    def change_player(self):
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]    

    def play_game(self):
        self.current_player = self.players[0]
        while not self.check_winner():
            print (f"------ {self.current_player} Turn ----------")
            self.current_player.turn()
            self.change_player()
        self.winner.show()       


class TimedGame(Game):

    def __init__(self, player1, player2, time_limit):
        super().__init__(player1, player2)
        self.current_player= self.players[0]
        self.start_time = datetime.datetime.now()
        self.time_limit = time_limit

    def check_time(self, time_now):
        
        return (time_now - self.start_time).total_seconds() > self.time_limit

    def change_player(self):

        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]

    def play_game(self):
        self.current_player = self.players[0]
        time_flag = False
        while not self.check_winner() or not time_flag:
            print (f"------ {self.current_player} Turn ----------")
            self.current_player.turn()
            self.change_player()
            print (self.current_player)
            time_flag = self.check_time(datetime.datetime.now())

        self.winner.show()
        


def make_player(player_type, player_name):
    
    if player_type.upper() == 'C':
        return ComputerPlayer(player_name)
    elif player_type.upper() == 'H':
        return Player(player_name)
    else:
        raise ValueError("I don't know what to build!!!!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pig Game")
    parser.add_argument("--player1", type=str, help="human/computer", required=True)
    parser.add_argument("--player2", type=str, help="human/computer", required=True)
    parser.add_argument("--timed", help="timed game")
    args = parser.parse_args()

    p1 = make_player(args.player1.lower()[0], "John")
    p2 = make_player(args.player2.lower()[0], "Jane")
    
    pig_game = Game(p1, p2)
    pig_game.play_game()