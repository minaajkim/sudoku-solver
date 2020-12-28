#Mina Kim
import numpy as np
import copy

#checks the row, column, and subsquare of a particular square for duplicates of the attempted number
#returns False if the number does not work, returns True if it works
def check_number(puzzle, num, n, r, c):
    x = np.array(list(puzzle))
    grid = np.reshape(x, (9, 9))
    num = str(num)

    #Checks availability of given square
    if grid[r][c] != "0":
        return False

    #Checks availability of each row and column
    for i in range(0, n):
        if grid[r][i] == num:
            return False
        if grid[i][c] == num:
            return False

    #Gets the coordinates of the top left square in the specific subsquare
    #Using these, checks availability of subsquare
    if c == 1 or c == 2:
        topLeftCol = 0
    elif c == 4 or c == 5:
        topLeftCol = 3
    elif c == 7 or c == 8:
        topLeftCol = 6
    else:
        topLeftCol = c
    if r == 1 or r == 2:
        topLeftRow = 0
    elif r == 4 or r==5:
        topLeftRow = 3
    elif r == 7 or r == 8:
        topLeftRow = 6
    else:
        topLeftRow = r

    for i in range(topLeftRow, topLeftRow+3):
        for j in range(topLeftCol, topLeftCol+3):
                if grid[i][j] == num:
                    #print("problem box")
                    return False
    return True

#Finds the row of the index of string
def findRow(index, n):
    return index//n

#Finds the column of the index of string
def findCol(index, n):
    return index%n

#Workaround for returning final puzzle after recursion complete
def export(puzzle):
    global puz
    puz = puzzle
    return

#Solves the sudoku puzzle using backtracking/recursion
def solve(puzzle, n, markup):

    #update the markup (aka get rid of singletons, etc.) at the beginning
    puzzle, markup = update_singleton(puzzle, markup)

    #Base case: puzzle is already solved
    if puzzle.find('0') < 0:
        print("solved")
        return puzzle

    index = findPos(puzzle, markup)

    for num in markup[index]:
        #if check_number(puzzle, num, n, index//9, index%9) == True:
        newPzl = puzzle[:index] + num + puzzle[index+1:]
        newMark = remove_from_markups(puzzle, markup, num, index)
        res = solve(newPzl, n, newMark)
        if res != "":
            return res
    return ""

#returns the index of the smallest list of candidates (for speed-up)
def findPos(puzzle, markup):
    index = 0
    min = 999999
    for entry in markup:
        #print(len(markup[entry]))
        if len(markup[entry]) != 0 and puzzle[entry] == '0' and len(markup[entry]) < min:
            index = entry
            min = len(markup[entry])
        if min == 2:
            return index
    return index

#This function ensures that when a value is assigned to the cell, the markups are updated for the cell and
#the number is excluded as a candidate for the rest of the row/col/box
def remove_from_markups(puzzle, markup, val, index): #if you assign a value, it must be excluded as a candidate for the rest of the row/col/box
    #Remove from row markups
    temp = markup.copy()
    for i in range(0,81):
        if i//9 == index//9 and i != index:
            if i in markup:
                if val in markup[i]:
                    l = markup[i].copy()
                    l.remove(val)
                    temp[i] = l
        if i%9 == index%9 and i != index:
            if i in markup:
                if val in markup[i]:
                    t = markup[i].copy()
                    t.remove(val)
                    temp[i] = t
    #Remove from box markups
    for k in range(index//9-(index//9)//3,3+index//9-(index//9)//3):
        for l in range(index%9-(index%9)%3,3+index%9-(index%9)%3):
            box_ind = 9*k + l
            if box_ind != index and box_ind in markup.keys():
                if val in markup[box_ind]:
                    q = markup[box_ind].copy()
                    q.remove(val)
                    temp[box_ind] = q
    return temp

#Returns updated puzzle and markup after a size-one list of candidates is assigned to a cell (for speed-up)
def update_singleton(puzzle, markup):
    temp = markup.copy()
    for x in markup.keys(): #for each unfilled square in the puzzle bc markup only holds unfilled squares
        if len(markup[x]) == 1: #if there's only one candidate in markup
            val = list(markup[x])[0]
            puzzle = puzzle[:x] + str(val) + puzzle[x+1:] #just append that one possibility to the puzzle at that index
            for i in range(0,81):
                if i//9 == x//9:
                    if i in markup:
                        if val in markup[i]:
                            l = markup[i].copy()
                            l.remove(val)
                            temp[i]=l
                if i%9 == x%9:
                    if i in markup:
                        if val in markup[i]:
                            t = markup[i].copy()
                            t.remove(val)
                            temp[i]=t
            for k in range(x//9-(x//9)//3, 3+x//9-(x//9)//3): #Removes number from all markups of squares in the box
                for h in range(x%9-(x%9)%3, 3+x%9-(x%9)%3):
                    ind3 = 9*k + h
                    if ind3 in markup.keys():
                        if val in markup[ind3]:
                            m = markup[ind3].copy()
                            m.remove(val)
                            temp[ind3]=m
    return puzzle, temp

#Reads the file into a list of lists
def read_into_lists():
    filename = "nine.txt"
    #input("What filename?")
    f = open(filename, 'r')
    l = []
    l = [line.split() for line in f]
    return l #where l is list of lists, each sublist is a row in input file

#Handles reformatting strings into grid output
def display(l, n):
    new_list = list(l)
    new_list = np.reshape(new_list, (n, n))
    for x in new_list:
        print(' '.join(x))

def main():
    list_of_lists = read_into_lists()
    num = 9
    #Turns list of lists into list of puzzles (represented by strings)
    for x in list_of_lists:
        list_of_lists = [''.join(x) for x in list_of_lists]
    #Solves and outputs
    for y in list_of_lists:
        print("Original: ")
        display(y, num)
        y = y.replace(".", "0") #y is a string representation of each puzzle
        markup = dict()
        for x in range(0, 81):
            if y[x] == '0':
                markup[x] = list()
                for i in range(1, 10):
                    if check_number(y, i, 9, x // 9, x % 9) == True:
                        markup[x].append(str(i))
        print("Solved:")
        result = solve(y, num, markup)
        if result != "":
            print(result)
            display(result,num)
        #display(puz, num)

main()