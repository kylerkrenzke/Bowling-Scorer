class BowlingGame:
    def __init__(self, names):
        self.names = names
        self.nplayers = len(names)
        self.scores = [[(None, None) for j in range(10)] for i in range(self.nplayers)]
        self.totals = [[None for j in range(10)] for i in range(self.nplayers)]
        
    def setFrameScore(self, player, frame, score):
        self.scores[player][frame] = score
        
    def isTerminal(self):
        for player in self.scores:
            for frame in player:
                if frame[0:1] == (None, None):
                    return False
        return True
        
def formatFrame(frame):
    if frame[0] == frame[1] == None:
        return "|   |"
    elif isinstance(frame[0], int) and frame[1] == None:
        return "|  X|" if frame[0] == 10 else "|{}  |".format(frame[0])
    else:
        return "|{0} {1}|".format(frame[0], '/' if frame[0]+frame[1]==10 else frame[1])
        
def formatFrameList(frame_lst):
    ret = ""
    for lst in frame_lst:
        ret = ret + formatFrame(lst)
    return ret
    
def formatPlayerList(player_lst, names):
    ret = ""
    for i in range(5*10 + 12):
        ret += '-'
    ret += '\n'
    for i in range(len(player_lst)):
        ret += "|{0}|".format(names[i].ljust(10))
        ret += formatFrameList(player_lst[i]) + '\n'
    for i in range(5*10 + 12):
        ret += '-'
    return ret
        
def formatGame(game):
    return "Scoreboard:\n{0}".format(formatPlayerList(game.scores, game.names))
        
def getPlayers():
    print("Enter player names 1 at a time (between 2-4). Enter 'done' when finished\n")
    name = ""
    names = []
    while name != "done" and len(names) != 4:
        name = input(">> ")
        if len(name) > 10:
            name = name[0:10]
        if name != "done":
            names.append(name)
    return names

print("----- Bowling Scorer -----\n\nAuthor: Kyler Krenzke\n")
    
names = getPlayers()
game = BowlingGame(names)
game.setFrameScore(0, 0, (10, None))
game.setFrameScore(0, 1, (9, None))
game.setFrameScore(0, 2, (8, 2))
game.setFrameScore(0, 3, (7, 2))

print(formatGame(game))