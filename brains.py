_BASESIZE = 8
_ROWCOUNT = 13
_MAX_COMPUTATIONAL_TIME = 60

from copy import deepcopy
from time import clock

def createEmptyBoard():
    board = []
    for i in range(13):
        board.append(['X' for _ in range(_BASESIZE - 1 + min(i, 6))])
    return board

def updateBoard(board, tileType, coords):
    board[coords[0]][coords[1]] = tileType

def initState(board):
    # to pad board with empty spaces for easier computation

    # board.insert(0, ['X' for _ in range(_BASESIZE)])
    # for i in range(1, 6):
    #     board[i] = ['X'] + board[i] + ['X']
    # board[6] = ['X'] + board[6] + ['X']
    # for i in range(7, 12):
    #     board[i] = ['X'] + ['X']*(i-6) + board[i] + ['X']
    # board.append(['X' for _ in range(_ROWCOUNT)])

    freeAtoms = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if cellIsEmpty(board, row, col):
                continue
            elif checkFree(board, row, col):
                freeAtoms.append((board[row][col], (row, col)))

    countDict = {'?': 4, 'A': 8, 'B': 8, 'C': 8, 'D': 8,
                 'M': 4, 'V': 4, 'Q': 5,
                 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}
    return board, freeAtoms, sum(countDict.values()), 1

def cellIsEmpty(board, row, col):
    return board[row][col] == 'X'

def checkFree(board, row, col):
    #  C C X
    #  C ? C
    #  X C C
    neighbourList = []
    neighbourCheck = ((row-1, col-1), (row-1, col), (row, col+1), (row+1, col+1), (row+1, col), (row, col-1))
    for i in neighbourCheck:
        neighbourList.append(cellIsEmpty(board, *i))
    neighbourList = neighbourList + neighbourList[:2]
    # print(row, col, neighbourList)
    neighbourList = [neighbourList[i:i+3] == [True, True, True] for i in range(6)]
    return any(neighbourList)

# sampleBoard = [['C', 'X', 'X', 'X', 'X', 'D'],
#                ['D', 'C',  2 , 'Q', 'B', 'C', 'X'],
#                [ 3 , 'B', 'C', 'X', 'X', 'A', 'X', 'A'],
#                ['A',  5 , 'B', 'M', 'X', 'X', 'M', '?', 'D'],
#                ['X', 'X',  4 , 'X', 'B', 'X', 'X', 'A', 'A', 'V'],
#                ['Q', '?', '?', 'X', 'X',  6 , 'B', 'Q', '?', 'V', 'M'],
#                ['X', 'C', 'X', 'X', 'D', 'X', 'X', 'X', 'M', 'X'],
#                ['X', 'V', 'X', 'B', 'X', 'X', 'X',  1 , 'X'],
#                ['X', 'B', 'D', 'A', 'B', 'Q', 'A', 'X'],
#                ['X', 'D', 'C', 'D', 'X', 'C', 'X'],
#                ['Q', 'V', 'C', 'D', 'X', 'A']]

def printBoard(board):
    for i, row in enumerate(board):
        if i == 0 or i == len(board)-1:
            continue
        else:
            for charIndex in range(len(row[1:-1])):
                if charIndex<i-6:
                    print('', end = '\t')
                    continue
                print(row[1+charIndex], end = '\t')
            print()

# sampleState = initState(sampleBoard)
# printBoard(sampleState[0])
# print()
# print(sampleState[1])

def solvePair(state, coord1, coord2):
    board, freeAtoms, atomCount, metalCleared = state
    board = deepcopy(board)
    freeAtoms = freeAtoms.copy()


    row1, col1 = coord1
    neighbourCheck1 = ((row1-1, col1-1), (row1-1, col1), (row1, col1+1), (row1+1, col1+1), (row1+1, col1), (row1, col1-1))
    row2, col2 = coord2
    neighbourCheck2 = ((row2-1, col2-1), (row2-1, col2), (row2, col2+1), (row2+1, col2+1), (row2+1, col2), (row2, col2-1))

    if board[row1][col1] == 6:
        atomCount += 1
    if board[row1][col1] == metalCleared or board[row2][col2] == metalCleared:
        metalCleared += 1
    board[row1][col1] = 'X'
    board[row2][col2] = 'X'
    atomCount -= 2
    freeAtoms = [i for i in freeAtoms if (i[1] != coord1 and i[1] != coord2)]

    totalNeighbourCheck = set(neighbourCheck1) | set(neighbourCheck2)
    for i in totalNeighbourCheck:
        if board[i[0]][i[1]] != 'X' and checkFree(board, *i) == True and (board[i[0]][i[1]], i) not in freeAtoms:
            freeAtoms.append((board[i[0]][i[1]], i))
    return board, freeAtoms, atomCount, metalCleared

# newState = solvePair(sampleState, (3, 8), (4, 1))
# printBoard(newState[0])
# print()
# print(newState[1])

def getSolutions(freeAtoms, metalCleared):
    wildSaltSet = []
    saltSets = [[], [], [], []]
    quicksilverSet = set()
    metalSet = set()
    vitaeSet = set()
    morsSet = set()

    refer = {'?': wildSaltSet.append,
             'A': saltSets[0].append,
             'B': saltSets[1].append,
             'C': saltSets[2].append,
             'D': saltSets[3].append,
             'Q': quicksilverSet.add,
             metalCleared: metalSet.add,
             'V': vitaeSet.add,
             'M': morsSet.add}

    for i in freeAtoms:
        try:
            refer[i[0]](i)
        except:
            continue

    if len(metalSet) > 0:
        for metal in metalSet:
            if metal[0] == 6:
                yield metal[1], metal[1]
            else:
                for quickSilver in quicksilverSet:
                    yield metal[1], quickSilver[1]


    if len(vitaeSet) > 0 and len(morsSet) > 0:
        for vitae in vitaeSet:
            for mors in morsSet:
                yield vitae[1], mors[1]

    for saltList in saltSets:
        for i in range(len(saltList)):
            for wild in wildSaltSet:
                yield saltList[i][1], wild[1]
            for j in range(i+1, len(saltList)):
                yield saltList[i][1], saltList[j][1]


def solve(state, elapsedTime):
    # print('Current elapsedTime:', elapsedTime)
    start = clock()
    board, freeAtoms, atomCount, metalCleared = state
    if atomCount == 0:
        return True, elapsedTime
    for solutionCoords in getSolutions(freeAtoms, metalCleared):
        newState, stepSolveTime = solve(solvePair(state, *solutionCoords), elapsedTime + clock() - start)
        if newState:
            return [solutionCoords] + ([] if newState == True else newState), elapsedTime
        elapsedTime = stepSolveTime
        if elapsedTime > _MAX_COMPUTATIONAL_TIME:
            return False, elapsedTime
    return False, elapsedTime

def validBoard(board):
    atomCount = {}
    for row in board:
        for element in row:
            if element == 'X':
                continue
            try:
                atomCount[element] += 1
            except KeyError:
                atomCount[element] = 1

    totalCount = 0
    for v in atomCount.values():
        totalCount += v
    if totalCount != 55 or atomCount['A'] != 8 or atomCount['B'] != 8 or atomCount['C'] != 8 or atomCount['D'] != 8:
        return False
    else:
        return True


# solution = solve(sampleState)
# for i in solution:
#     print(*i)

# for i in getSolutions(sampleState[1], sampleState[3]):
#     print (*i)