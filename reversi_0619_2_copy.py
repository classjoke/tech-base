import random
import copy

class Pos(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hyoukati = HYOUKATI[self.x][self.y]
    def add(self, p):
        return Pos(self.x + p.x, self.y + p.y)


HYOUKATI = [
            [-100, -100, -100, -100, -100, -100, -100, -100, -100, -100],
            [0, 10, -3, 5, 4, 4, 5, -3, 10, 0],
            [0, -3, -5, 4, 3, 3, 4, -5, -3, 0],
            [0, 5, 4, 5, 3, 3, 5, 4, 5, 0],
            [0, 4, 3, 3, 3, 3, 3, 3, 4, 0],
            [0, 4, 3, 3, 3, 3, 3, 3, 4, 0],
            [0, 5, 4, 5, 3, 3, 5, 4, 5, 0],
            [0, -3, -5, 4, 3, 3, 4, -5, -3, 0],
            [0, 10, -3, 5, 4, 4, 5, -3, 10, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]

path = "test_2.txt"
file_p = open(path, "w")

class Board(object):
    def __init__(self):
        self.cell = [["E" for _ in range(10)] for _ in range(10)]
        self.cell[4][4] = "W"
        self.cell[4][5] = "B"
        self.cell[5][4] = "B"
        self.cell[5][5] = "W"
        for i in range(10):
            for j in range(10):
                if i > 8 or j > 8:
                    self.cell[j][i] = "O"
                if i < 1 or j < 1:
                    self.cell[j][i] = "O"

    def ask(self, color, pos, board):
        if color == "B":
            o_color = "W"
        elif color == "W":
            o_color = "B"
        else: return False
        if board[pos.x][pos.y] == "E":
            for e in range(-1, 2):
                for f in range(-1, 2):
                    if e == 0 and f == 0: continue
                    if board[pos.x+e][pos.y+f] == o_color:
                        if self._can_reverse(color, pos, e, f, board):
                            return True

        return False

    def _ask(self, color, pos, board):
        if color == "B":
            o_color = "W"
        elif color == "W":
            o_color = "B"
        else:
            return False
        count = 0
        if board[pos.x][pos.y] == "E":
            for e in range(-1, 2):
                for f in range(-1, 2):
                    if e == 0 and f == 0: continue
                    if board[pos.x + e][pos.y + f] == o_color:
                        l = self._can_reverse(color, pos, e, f, board)
                        if l is not None:
                            count = 1
                            t, r, p, q = 0, 0, pos.x, pos.y
                            a = l[0] - pos.x
                            b = l[1] - pos.y
                            if abs(a) == abs(b):
                                buf = abs(a)
                            else: buf = abs(a)+abs(b)

                            if abs(a) != 0:
                                t = int(a / abs(a))
                            if abs(b) != 0:
                                r = int(b / abs(b))
                            for _ in range(buf-1):
                                p += t
                                q += r
                                board[p][q] = color



        if count == 1:
            board[pos.x][pos.y] = color
            return True
        else: return False

    def play(self, color, pos, board):
        return self._ask(color, pos, board)

    def _can_reverse(self, color, pos, e, f, board):
        if color == "B":
            o_color = "W"
        elif color == "W":
            o_color = "B"
        count = 1

        while board[pos.x+e*count][pos.y+f*count] == o_color:
            count += 1

            if board[pos.x+e*count][pos.y+f*count] == color:
                return pos.x+e*count, pos.y+f*count
        return None

    def showboard(self):
        for i in range(1, 9):
            for j in range(1, 9):
                print(self.cell[j][i], end="")
            print("")

    def genmove(self, color):
        if color == "B":
            o_color = "W"
        elif color == "W":
            o_color = "B"
        candidates = []
        max = Pos(0, 0)

        fww = -100
        for y in range(1, 9):
            for x in range(1, 9):
                pos = Pos(x, y)
                if self.ask(color, pos, self.cell):
                    candidates.append(pos)

        #            max = pos
        for i in candidates:
            self.board_copy = copy.deepcopy(self.cell)
            self.play(color, i, self.board_copy)
            file_p.write(color + str(i.x) + " " + str(i.y)+" "+ str(i.hyoukati) + "\n")

            max_o = Pos(0, 0)

            for y in range(1, 9):
                for x in range(1, 9):
                    o_pos = Pos(x, y)
                    if self.ask(o_color, o_pos, self.board_copy):

                        file_p.write(o_color+ " "+str(o_pos.x) +" " + str(o_pos.y) + " "+ str(o_pos.hyoukati)+ "\n")
                        if max_o.hyoukati < o_pos.hyoukati:
                            max_o = o_pos
                            file_p.write(str(max_o.hyoukati) + "\n")
            file_p.write(str(i.hyoukati - max_o.hyoukati) +" "+str(fww)+"\n")
            #file_p.write(str(max.x) + " " + str(max.y) + " " + str(fww) + "\n")
            if i.hyoukati - max_o.hyoukati >= fww:
                max = i
                fww = i.hyoukati - max_o.hyoukati
                file_p.write("現状最善手 "+str(max.x) + " " + str(max.y) + " " + str(fww) + "\n")

        if len(candidates) == 0:
            return "NG"
        self.play(color, max, self.cell)

        file_p.write(str(max.x) + " " + str(max.y) + " " + str(fww) + "\n")

        return str(max.x-1)+" "+str(max.y-1)

    def _genmove(self, color):
        candidates = []
        max = Pos(0, 0)
        for y in range(1, 9):
            for x in range(1, 9):
                pos = Pos(x, y)
                if self.ask(color, pos, self.cell):
                    candidates.append(pos)

        if len(candidates) == 0:
            return "NG"

        for i in candidates:
            if max.hyoukati < i.hyoukati:
                max = i
#        print(max.x - 1, max.y - 1, max.hyoukati)

        return str(max.x - 1) + " " + str(max.y - 1)

    def result(self):
        b_count = 0
        w_count = 0
        if self._genmove("B") == "NG" and self._genmove("W") == "NG":
            for i in range(10):
                for j in range(10):
                    if self.cell[j][i] == "B":
                        b_count += 1
                    elif self.cell[j][i] == "W":
                        w_count += 1
            if b_count > w_count:
                print("B")
            elif w_count > b_count:
                print("W")
            elif b_count == w_count:
                print("D")
            return True
        else:
            print("NG")
            return False

    def is_valid(self, pos):
        return 1 <= pos.x < 9 and 1 <= pos.y < 9
def main():
    board = Board()
    while True:
        cmd = input().split()
        #file_p.write(cmd[0]+" ")
        if cmd[0] == "quit":
            return
        elif cmd[0] == "name":
            print("test project")
        elif cmd[0] == "showboard":
            board.showboard()
        elif cmd[0] == "ask":
            if board.is_valid(Pos(int(cmd[2])+1, int(cmd[3])+1)):
                if board.ask(cmd[1], Pos(int(cmd[2])+1, int(cmd[3])+1), board.cell):
                    print("OK")
                else:
                    print("NG")
            else:
                print("NG")
        elif cmd[0] == "play":
            if board.is_valid(Pos(int(cmd[2]) + 1, int(cmd[3]) + 1)):
                if board.play(cmd[1], Pos(int(cmd[2])+1, int(cmd[3])+1), board.cell):
                    print("OK")
                else:
                    print("NG")
            else:
                print("NG")
        elif cmd[0] == "genmove":
            fas = board.genmove(cmd[1])
            print(fas)
        elif cmd[0] == "result":
            board.result()

if __name__ == '__main__':
    main()