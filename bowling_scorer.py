class BowlingGame:
    def __init__(self, nplayers):
        self.nplayers = nplayers
        self.scores = [[(None, None) for j in range(10)] for i in range(nplayers)]
        
    def setFrameScore(self, player, frame, score):
        self.scores[player][frame] = score
        
def formatFrame(frame):
    if frame == (None, None):
        return "|   |"
    elif frame == (10, None):
        return "|  X|"
    else:
        return "|{0} {1}|".format(frame[0], '/' if frame[0]+frame[1]==10 else frame[1])
        
def formatFrameList(frame_lst):
    ret = ""
    for lst in frame_lst:
        ret = ret + formatFrame(lst)
    return ret
    
def formatPlayerList(player_lst):
    ret = ""
    for i in range(5 * 10):
        ret += '-'
    ret += '\n'
    for lst in player_lst:
        ret = ret + formatFrameList(lst) + '\n'
    for i in range(5 * 10):
        ret += '-'
    return ret
        
def printGame(game):
    for player in range(game.nplayers):
        for i in range(10):
            if game.scores[player][i] == (None, None):
                print(' ')
            elif game.scores[player][i] == (10,None):
                print('X')
            elif game.scores[player][i][0] + game.scores[player][i][1] == 10:
                print(game.scores[player][i][0],'/')
            else:
                print(game.scores[player][i][0],game.scores[player][i][1])
        
print("----- Bowling Scorer -----\n\nAuthor: Kyler Krenzke\n")
nplayers = int(input("How many players? "))
while nplayers < 2 or nplayers > 4:
    nplayers = int(input("Please enter a number between 2 and 4. How many players? "))
    
game = BowlingGame(nplayers)
game.setFrameScore(0, 0, (10, None))
print(formatPlayerList(game.scores))