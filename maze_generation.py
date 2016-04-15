# -*- coding: utf-8 -*-
"""
Task: A Maze Generator 
"""
###############################################################################
from random import randint as r
###############################################################################

#func - text form of maze
def show(input_uni): 
    for x in input_uni:
        for y in x:
            print(y, end=" ")
        print()
    return input_uni

#func - generator starting position
def start(maze):
    index_one=r(1,(len(maze)-2))
    index_two=r(1,(len(maze)-2))
    while True:    
        if maze[index_one][index_two]==1 or maze[index_one][index_two]==4:
            index_one=r(1,(len(maze)-2))
            index_two=r(1,(len(maze)-2))
            continue
        else:
            maze[index_one][index_two]=3
            break

#func - end position     
def end(maze):    
    maze[-2][-2]=4  
    
   
#main func - maze generator
def generation(row, length, wall_length):

    #sub func - inner walls of maze
    def choice_of_direction(pos_2, maze, wall_length):
        choice_2 = pos_2[r(0,(len(pos_2)-1))]
        current = (choice_2[0],choice_2[-1])
        direction = r(0,3)
        pos_2.remove(current)
        while True:
            
            for _ in range(0,wall_length):
                if direction == 0:
                        maze[current[0]][current[-1]] = 1
                        current = ((current[0]-1),current[-1])
                        if current in pos_2:
                            pos_2.remove(current)
                        if maze[current[0]][current[-1]] == 1:
                            break
                        
                elif direction == 1:
                        maze[current[0]][current[-1]] = 1
                        current = (current[0],(current[-1]+1))
                        if current in pos_2:
                            pos_2.remove(current)
                        if maze[current[0]][current[-1]] == 1:
                            break
                        
                elif direction == 2:
                        maze[current[0]][current[-1]] = 1
                        current = ((current[0]+1),current[-1])
                        if current in pos_2:
                            pos_2.remove(current)
                        if maze[current[0]][current[-1]] == 1:
                            break
                        
                elif direction == 3:
                        maze[current[0]][current[-1]] = 1
                        current = (current[0],(current[-1]-1))
                        if current in pos_2:
                            pos_2.remove(current)
                        if maze[current[0]][current[-1]] == 1:
                            break

            if len(pos_2) == 0:
                break
            direction = r(0,3)
            choice_2 = pos_2[r(0,(len(pos_2)-1))]
            current = (choice_2[0],choice_2[-1])
            pos_2.remove(current)
    
    #sub func - replacing remaining 2 cells to 0    
    def del_2(maze):
        for row in range(0,len(maze)-1):
            for point in range(0,len(maze)-1):
                if maze[row][point] == 2:
                    maze[row][point] = 0
        return maze
    
    pos_2 = []        
    maze = [[0 for _ in range(length)] for _ in range(row)] #main part
    for i in range(len(maze)): #outer walls
            if i == 0 or i == (len(maze)-1):
                maze[i] = [1 for _ in range(len(maze[i]))] 
            maze[i][0]=1
            maze[i][-1]=1
            
    for line in range(len(maze)): #marking free cells for inner walls
        for cell in range(len(maze)):
             if 0 <= (line+1) < len(maze): 
                if 0 <= (cell+1) <len(maze[line]):
                   pole = (maze[line+1][cell-1]+maze[line+1][cell]+
                           maze[line+1][cell+1]+maze[line][cell-1]+
                           maze[line][cell+1]+maze[line-1][cell-1]+
                           maze[line-1][cell]+maze[line-1][cell+1]
                          )          
                if pole > 0:
                    continue
                elif pole == 0:
                    maze[line][cell] = 2
                    pos_2.append((line,cell))

    choice_of_direction(pos_2, maze, wall_length)
    del_2(maze)
    start(maze)
    end(maze)
    return maze