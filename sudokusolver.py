# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 09:06:03 2022

@author: JAndreg

The aim of this code is to solve sudokus
"""

#The sudoku values will be stored in the below matrix
sud = [[" " for i in range(9)] for j in range(9)]


#We need to display the sudoku in the console
def display(sud):
    print("+---+---+---+---+---+---+---+---+---+")
    for i in range(9):
        print("| {} ¦ {} ¦ {} | {} ¦ {} ¦ {} | {} ¦ {} ¦ {} |".format(*sud[i]))
        if i%3 == 2:
            print("+---+---+---+---+---+---+---+---+---+")
        else:
            print("+- -+- -+- -+- -+- -+- -+- -+- -+- -+")

#User inputs
print("Please fill the sudoku:")
for i in range(9):
    for j in range(9):
        sud[i][j] = "x"
        display(sud)
        ans = input("Please enter the value of x or leave empty: ")
        if ans:
            sud[i][j] = int(ans)
        #note: here the conversion to integer is not mandatory as no 
        #operations shall be performed on the values
        #However it is more convenient to manipulate integers than strings
        else:
            sud[i][j] = " "

display(sud)
print("Thank you\n")

#trival cases if any...

#check function, works like a firewall with default rule allow
def check(sud):
    #only one value between 1 and 9 per row
    for row in sud:
        #if the line is full
        if " " not in row:
            for val in range(1,10):
                if val not in row: return False
                
        #if the line is not full, we can check doubles
        else:
            for val in range(1,10):
                if row.count(val) > 1: return False
            
    #same for columns
    for j in range(9):
        col = [sud[i][j] for i in range(9)]
        #full columns
        if " " not in col:
            for val in range(1,10):
                if val not in col: return False
        #uncomplete column, doubles check
        else:
            for val in range(1,10):
                if col.count(val) > 1: return False
    
    #now checking the 3x3 squares 
    for k in range(3):
        for l in range(3):
            square = []
            for i in range(3 * k, 3 * (k + 1)):
                for j in range(3 * l, 3 * (l + 1)):
                    square.append(sud[i][j])
            
            #for a full square
            if " " not in square:
                for val in range(1,10):
                    if val not in square: return False
            #for an uncomplete square, check for doubles
            else:
                for val in range(1,10):
                    if square.count(val) > 1: return False

    return True

#test solved sudoku
solved = [[8, 2, 7, 1, 5, 4, 3, 9, 6],
 [9, 6, 5, 3, 2, 7, 1, 4, 8],
 [3, 4, 1, 6, 8, 9, 7, 5, 2],
 [5, 9, 3, 4, 6, 8, 2, 7, 1],
 [4, 7, 2, 5, 1, 3, 6, 8, 9],
 [6, 1, 8, 9, 7, 2, 4, 3, 5],
 [7, 8, 6, 2, 3, 5, 9, 1, 4],
 [1, 5, 4, 7, 9, 6, 8, 2, 3],
 [2, 3, 9, 8, 4, 1, 5, 6, 7]]

test = [[8, 2, 7, 1, 5, 4, 3, 9, 6],
 [" "," "," "," "," "," "," "," "," "],
 [" "," "," "," "," "," "," "," "," "],
 [" "," "," "," "," "," "," "," "," "],
 [" "," "," "," "," "," "," "," "," "],
 [" "," "," "," "," "," "," "," "," "],
 [7, 8, 6, 2, 3, 5, 9, 1, 4],
 [1, 5, 4, 7, 9, 6, 8, 2, 3],
 [2, 3, 9, 8, 4, 1, 5, 6, 7]]


# sud = test

#display(sud)
#
#print("check(sud) =",check(sud),"\n")

#initialization

# We need to flag the values as good (thos given) that won't be changed
# and we need also to be able to stop on a specific cell when a proposed value
# break the rules or  when all possible values have been tried.
# In the first case the algorithm has to propose a new value, in the second
# it needs to go backwad.


#our good matrix g, initially no values are trusted
good = [[0 for i in range(9)] for j in range(9)]

for i in range(9):
    for j in range(9):
        if sud[i][j] != " ": good[i][j] = 1
            

#our stop matrix, initially we don't need to stop
stop = [[0 for i in range(9)] for j in range(9)]

#functions to browse the sudoku grid
def next_cell(i,j):
    return (i,j+1) if j < 8 else (i+1,0)

def prev_cell(i,j):
    return (i,j-1) if j > 0 else (i-1,8)


iteration = 0
i,j = 0,0
while (i,j) < (9,0):

# OPTIONAL
#.............................................    
    completed = True
    for k in range(9):
        if " " in sud[k]: completed = False
        
    if completed and check(sud): break
#.............................................  

    #if cell is empty, let's propose 1
    if sud[i][j] == " ": sud[i][j] = 1
    
    if check(sud) and not stop[i][j]:
        i,j = next_cell(i,j)
    
    else:
        if good[i][j]:
            if stop[i][j]: stop[i][j] = 0
            i,j = prev_cell(i,j)
            stop[i][j] = 1
        else:
            if sud[i][j] < 9:
                sud[i][j] = sud[i][j] + 1
                if stop[i][j]: stop[i][j] = 0
            else:
                sud[i][j] = " "
                if stop[i][j]: stop[i][j] = 0
                i,j = prev_cell(i,j)
                stop[i][j] = 1
    
    iteration = iteration +1


print("And the solution is...\n")                
display(sud)
print("\n#iteration =", iteration)                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        