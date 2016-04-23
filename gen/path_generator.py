# -*- coding: utf-8 -*-
###############################################################################
from pprint import pprint
############################################################################

def show(input_uni):
    for x in input_uni:
        for bod in x:
            print(bod, end="")
        print()
    return input_uni
 
def find_players(maze): 
    enemy_position = None
    my_position = None    
    for row in range(0, len(maze)):
        for cell in range(0, len(maze[row])):
            if len(maze[row][cell]) > 1:
               if "your_bot" in maze[row][cell]:
                   my_position = (row, cell)
               else:
                   enemy_position = (row, cell)
            if enemy_position == True and my_position == True:
               break
    return dict(my_bot=my_position, enemy_bot=enemy_position)

def find_end(lab):
    for a, s in enumerate(lab):
        if 1 in s:
            return (a, s.index(1))

def objecttomap(maze):
    new_maze=[]
    one_row=[]
    start_position=(0,0)
    enemy_position=(0,0)
    orientation=0
    for row in range(0,len(maze)):
        for cell in range(0, len(maze[row])):
            if maze[row][cell].get("field") == 1:
                one_row.append(maze[row][cell].get("field"))
            elif len(maze[row][cell])>1:
                one_row.append(maze[row][cell].get("field"))
                print(maze[row][cell])
                if "your_bot" in maze[row][cell]:
                    start_position = (row, cell)
                    orientation=maze[row][cell].get("orientation")
                else:
                    enemy_position = (row, cell)
            else:
                one_row.append(maze[row][cell].get("field"))
        new_maze.append(one_row)
        one_row = []
    return new_maze, start_position, enemy_position, orientation,
   
def labtograph(labyrint, my_bot): #prevod nahodneho bludiste do grafu
    height=len(labyrint)
    width=len(labyrint[0]) if height else 0 #zapis v pythonu 3 - delka je rovno len.. pokud height ma nejakou hodnotu ktera se vrati jako True
    graph={ (i, j): [] for i in range(0, width) for j in range(0, height)
            if labyrint[i][j] != 3
          } 
    
    for row, col in graph.keys(): # zjisteni sousedu kolem jednotlivych vrcholu grafu (nahrazeni hran v grafu)
        if row < (height - 1) and (labyrint[row + 1][col] == 0 or labyrint[row + 1][col] == 1 or (row + 1, col) == (my_bot[0],my_bot[-1]) ): #dokud bude platit
           graph[(row, col)].append(("S",(row + 1,col))) #ptam se vyskove - prohledam jih
           graph[(row + 1, col)].append(("N",(row, col))) #davam jiznimu sousedu predchozi vrchol od kteryho ptam
        if col < (width - 1) and (labyrint[row][col + 1] == 0 or labyrint[row][col + 1] == 1 or (row, col + 1) == (my_bot[0],my_bot[-1])):
           graph[(row, col)].append(("E",(row, col + 1))) #ptam se sirkove - doprava - prohledavam vychod
           graph[(row, col + 1)].append(("W",(row, col))) #to same ale sirkove
    return graph
    

def moves(labyrint,location, start):
    goal = find_end(labyrint)
    queue = [("",start)]
    graph = labtograph(labyrint, my_bot=start )
    visited = set()
    print(start)
    print(goal)
    while queue:
        path, current = queue.pop(0)
        if current == goal:
            print(path)
            return action(path,location)
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            queue.append((path + direction,neighbour))
    return False
    
def action(path,location):
    loc={0:"N",1:"E",2:"S",3:"W"}
    ori=loc.get(location)
    moves=[]
    path=list(path)
    for p in path:
        if p == ori:
            moves.append("step")
        else:
            if ori == "N": #divam se nahoru
                if p == "W":
                    ori="W"
                    moves.append("turn_left")
                elif p == "E":
                    ori="E"
                    moves.append("turn_right")
                elif p == "S":
                    ori="S"
                    moves.append("turn_left")
                    moves.append("turn_left")
                    
            elif ori == "E": #divam se doprava 
                if p == "W":
                    ori="W"
                    moves.append("turn_right")
                    moves.append("turn_right")
                elif p == "N":
                    ori="N"
                    moves.append("turn_left")
                elif p == "S":
                    ori="S"
                    moves.append("turn_right")
                    
                    
            elif ori == "S": #divam se dolu
                if p == "W":
                    ori="W"
                    moves.append("turn_right")
                elif p == "E":
                    ori="E"
                    moves.append("turn_left")
                elif p == "N":
                    ori="N"
                    moves.append("turn_left")
                    moves.append("turn_left")
                    
            elif ori == "W": #divam se doleva
                if p == "N":
                    ori="N"
                    moves.append("turn_right")
                elif p == "E":
                    ori="E"
                    moves.append("turn_right")
                    moves.append("turn_right")
                elif p == "S":
                    ori="S"
                    moves.append("turn_left")
                    
            moves.append("step")
    return moves
