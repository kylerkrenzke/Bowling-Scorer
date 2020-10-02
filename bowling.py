class BowlingGame:
    def __init__(self, names):
        self.names = names
        self.curframe = 0
        self.curplayer = 0
        self.curthrow = 0
        
        self.scores = [[[] for j in range(10)] for i in range(len(names))]
        self.bonus_ctr = [[] for i in range(len(names))]
        self.bonuses = [[[] for j in range(10)] for i in range(len(names))]
        
    def cur_frame_score(self):
        return sum(self.scores[self.curplayer][self.curframe])
        
    def scoreThrow(self, no_pins):
        # score current throw
        self.scores[self.curplayer][self.curframe].append(no_pins)
        
        # add any strike/spare bonuses to the queue
        n_bonus_ctr = []
        while self.bonus_ctr[self.curplayer] != []:
            bonus = self.bonus_ctr[self.curplayer][0]
            recip_frame = bonus[0]
            bonus_no = bonus[1]
            self.bonuses[self.curplayer][recip_frame].append((self.curframe, self.curthrow))
            if bonus_no == 2:
                n_bonus_ctr.append((recip_frame, 1))
            self.bonus_ctr[self.curplayer].pop(0)
        self.bonus_ctr[self.curplayer] = n_bonus_ctr
        
        # update potential bonuses
        if self.curframe < 9:
            if self.cur_frame_score() == 10:
                if self.curthrow == 0:
                    self.bonus_ctr[self.curplayer].append((self.curframe, 2))
                elif self.curthrow == 1:
                    self.bonus_ctr[self.curplayer].append((self.curframe, 1))
                
        self.advance()
        
    def frame_total(self, player, frame):
        score = 0
        for f in range(len(self.scores[player][0:frame]) + 1):
            if len(self.scores[player][f]) == 0:
                return None
            elif len(self.scores[player][f]) == 1 and self.scores[player][f][0] != 10:
                return None
            
            for poss_bonus in self.bonus_ctr[player]:
                if poss_bonus[0] == f:
                    return None

            score += sum(self.scores[player][f])
            for elem in self.bonuses[player][f]:
                bonus_frame = elem[0]
                bonus_throw = elem[1]
                score += self.scores[player][bonus_frame][bonus_throw]
        return score
        
    def getPlayerTotals(self, player):
        return [self.frame_total(player, frame) for frame in range(len(self.scores[player]))]
        
    def getAllTotals(self):
        return [self.getPlayerTotals(player) for player in range(len(self.names))]
    
    def advance(self):
        self.curthrow += 1
        if self.curframe < 9:
            if self.curthrow == 2 or self.cur_frame_score() == 10:
                self.curthrow = 0
                self.curplayer += 1
                if self.curplayer == len(self.names):
                    self.curplayer = 0
                    self.curframe += 1
        else:
            if self.curthrow == 3 or (self.curthrow == 2 and self.cur_frame_score() < 10):
                self.curthrow = 0
                self.curplayer += 1
                if self.curplayer == len(self.names):
                    self.curframe += 1                
                
    def is_terminal(self):
        if self.curframe > 9:
            return True
        else:
            return False


class BowlingDriver:
    def __init__(self):
        self.game = None
        self.names = None
        
    def formatFrame(self, frame, is_tenth = False):
        if is_tenth:
            if len(frame) == 0:
                return "|     |"
            elif len(frame) == 1:
                return "|{0}    |".format('X' if frame[0] == 10 else frame[0])
            elif len(frame) == 2 and sum(frame) < 10:
                return "|{0} {1}  |".format(frame[0], frame[1])
            elif len(frame) == 2 and sum(frame) >= 10:
                return "|{0} {1}  |".format('X' if frame[0] == 10 else frame[0],
                                            '/' if sum(frame) == 10  and frame[0] != frame[1] != 0 else frame[1])
            elif len(frame) == 3:
                arg1 = 'X' if frame[0] == 10 else frame[0]
                if frame[1] == 10 and frame[0] == 10:
                    arg2 = 'X'
                elif sum(frame) == 10 and frame[1] != 0:
                    arg2 = '/'
                else:
                    arg2 = frame[1]
                arg3 = 'X' if frame[2] == 10 else frame[2]
                return "|{0} {1} {2}|".format(arg1, arg2, arg3)
    
        if len(frame) == 0:
            return "|   |"
        elif len(frame) == 1:
            return "|  X|" if frame[0] == 10 else "|{}  |".format(frame[0])
        else:
            return "|{0} {1}|".format(frame[0], '/' if frame[0]+frame[1]==10 else frame[1])
            
    def formatTotal(self, total, is_tenth=False):
        if is_tenth:
            return "| {0:3} |".format(total) if total is not None else "|     |"
        else:
            return "|{0:3}|".format(total) if total is not None else "|   |"
        
    def formatFrameList(self, frame_lst):
        ret = ""
        for lst in frame_lst[0: len(frame_lst)-1]:
            ret = ret + self.formatFrame(lst)
        ret += self.formatFrame(frame_lst[len(frame_lst)-1], is_tenth=True)
        return ret
        
    def formatTotalList(self, total_lst):
        ret = ""
        for total in total_lst[0: len(total_lst)-1]:
            ret += self.formatTotal(total)
        ret += self.formatTotal(total_lst[len(total_lst)-1], is_tenth=True)
        return ret
        
    def formatPlayerList(self, player_lst, names):
        totals = self.game.getAllTotals()
        
        ret = ""
        for i in range(5*9 + 7*1 + 12):
            ret += '-'
        ret += '\n'
        for i in range(len(player_lst)):
            ret += "|{0}|".format(names[i].ljust(10))
            ret += self.formatFrameList(player_lst[i]) + '\n'
            ret += "|          |"
            ret += self.formatTotalList(totals[i]) + '\n'
            
        for i in range(5*9 + 7*1 + 12):
            ret += '-'
        return ret
        
    def formatGame(self, game):
        return "Scoreboard:\n{0}".format(self.formatPlayerList(game.scores, game.names))
        
    def getPlayers(self):
        print("Enter player names 1 at a time (between 2-4). Enter 'done' when finished (case-sensitive)\n")
        name = ""
        self.names = []
        while len(self.names) < 4:
            name = input(">> ")
            if len(name) > 10:
                name = name[0:10]
            if name == "done":
                if len(self.names) < 2:
                    print("Please enter at least two (2) names. You have ({0}) so far.".format(len(self.names)))
                else:
                    break
            else:
                self.names.append(name)
    
    def play(self):
        self.getPlayers()
        self.game = BowlingGame(self.names)
        while not self.game.is_terminal():
            for i in range(500):
                print('\n')
            print(self.formatGame(self.game))
            print("Enter either the number of pins knocked down or 'quit' to exit")
            inp = input("{0} >> ".format(self.game.names[self.game.curplayer]))
            if inp == "quit":
                return
            else:
                score = int(inp)
                self.game.scoreThrow(score)
        print(self.formatGame(self.game))
                
driver = BowlingDriver()
driver.play()
