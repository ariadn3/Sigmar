from brains import *

puzzle = []
print('Reading puzzlein.txt...')
with open('puzzlein.txt', 'r') as input:
    for line in input.readlines():
        line = line.strip()
        l = []
        for char in line:
            if 49 <= ord(char) <= 54:
                l.append(int(char))
            else:
                l.append(char)
        puzzle.append(l)
print('Read complete! Solving board...')

solution = solve(initState(puzzle))

with open('puzzleout.txt', 'w') as output:
    for i in solution:
        for j in i:
            output.write(str(j) + '\t')
        output.write('\n')

print('Board solved! Check puzzleout.txt for solutions...')
