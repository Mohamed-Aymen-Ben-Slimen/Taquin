from graphics import *
import queue
import pprint
import time
import sys

pp = pprint.PrettyPrinter(indent=4)

end_puzzle = [[0, 2, 1, 3],[4, 6, 5, 7], [8, 9, 10, 11],[12, 13, 14, 15]]

open_q = queue.Queue()
closed_q = queue.Queue()

def puzz_astar(start, end):
    """
    A* algorithm
    """
    start = str(start)
    end = str(end)
    heuristic_function = heuristic_1
    if sys.argv == 'h2':
        heuristic_function = heuristic_2
    front = [[heuristic_function(start), start]]
    expanded = []
    expanded_nodes=0
    while front:
        i = 0
        for j in range(1, len(front)):
            if front[i][0] > front[j][0]:
                i = j
        path = front[i]
        front = front[:i] + front[i+1:]
        endnode = path[-1]
        if endnode == end:
            break
        if endnode in expanded: continue
        for k in moves(endnode):
            if k in expanded: continue
            newpath = [path[0] + heuristic_2(k) - heuristic_2(endnode)] + path[1:] + [k]
            front.append(newpath)
            expanded.append(endnode)
        expanded_nodes += 1
        if (expanded_nodes > 3000):
            return 0
    print("Expanded nodes:", expanded_nodes)
    pp.pprint(path)
    return path


def heuristic_1(puzz):
    """
    Calcule le nombre des cases mal placées
    """
    misplaced = 0
    compare = 0
    m = eval(puzz)
    for i in range(4):
        for j in range(4):
            if m[i][j] != compare:
                misplaced += 1
            compare += 1
    return misplaced

def heuristic_2(puzz):
    """
    Manhattan
    """
    distance = 0
    m = eval(puzz)
    for i in range(4):
        for j in range(4):
            if m[i][j] == 0: continue
            distance += abs(i - (m[i][j]/4)) + abs(j -  (m[i][j]%4))
    return distance



def initialize_board(filename):
    infile = open(filename, "r")
    board = []
    for i in range(4):
        board.append([])
    for row in range(4):
        for col in range(4):
            columnvalue = eval(infile.readline())
            board[row].append(columnvalue)
    return board

def display_numbers(window, board):
    for row in range(4):
        for col in range(4):
            square = Rectangle(Point(col * 100, row * 100), Point((col + 1) * 100, (row + 1) * 100))
            square.setFill("white")
            square.draw(window)
            if board[row][col] != 0:
                center = Point(col * 100 + 50, row * 100 + 50)
                number = Text(center, board[row][col])
                number.setSize(24)
                number.setTextColor("purple")
                number.draw(window)


def moves(mat):
    """
    Returns a list of all possible moves
    """
    output = []

    m = eval(mat)
    i = 0
    while 0 not in m[i]: i += 1
    j = m[i].index(0)  # blank space (zero)

    if i > 0:
        m[i][j], m[i - 1][j] = m[i - 1][j], m[i][j];  # move up
        output.append(str(m))
        m[i][j], m[i - 1][j] = m[i - 1][j], m[i][j];

    if i < 3:
        m[i][j], m[i + 1][j] = m[i + 1][j], m[i][j]  # move down
        output.append(str(m))
        m[i][j], m[i + 1][j] = m[i + 1][j], m[i][j]

    if j > 0:
        m[i][j], m[i][j - 1] = m[i][j - 1], m[i][j]  # move left
        output.append(str(m))
        m[i][j], m[i][j - 1] = m[i][j - 1], m[i][j]

    if j < 3:
        m[i][j], m[i][j + 1] = m[i][j + 1], m[i][j]  # move right
        output.append(str(m))
        m[i][j], m[i][j + 1] = m[i][j + 1], m[i][j]

    return output

def main():
    filename = ("taquin.txt")
    window = GraphWin("Jeux de Taquin", 400, 400)
    board = initialize_board(filename)
    display_numbers(window, board)
    path = puzz_astar(board, end_puzzle)
    if path == 0:
        message = Text(Point(200, 200), "NO POSSIBLE SOLUTION")
        message.setSize(24)
        message.setTextColor("orange")
        message.draw(window)
    else:
        for pa in path[1:]:
            display_numbers(window, eval(pa))
            time.sleep(0.3)
        message = Text(Point(200, 200), "SOLUTION FOUND")
        message.setSize(24)
        message.setTextColor("orange")
        message.draw(window)

    print("Press <ENTER> to quit.")
    input()
    window.close()


main()