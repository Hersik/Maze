# -*- coding: utf-8 -*-
"""
Task: Graphic part
"""
###############################################################################
from gen.maze_generator import (generation,)
from random import randint as r
from tkinter import (Tk, Label, Frame, messagebox, Canvas, SUNKEN, Menu, 
                     simpledialog, ALL)              
###############################################################################

class print_maze(Frame):
    def __init__(self, mainWin):
        super().__init__(mainWin)
        self.mainWin=mainWin
        self.mainWin.wm_title(u"Bludiště")
        self.mainWin.wm_geometry("{0}x{1}+"
                                 "{2}+{3}".format(self.mainWin.winfo_screenwidth()-15,
                                                  self.mainWin.winfo_screenheight()-95,
                                                  0,0))
        
        #variables
        self.maze_width=11
        self.maze_height=11
        self.box_width=0
        self.box_height=0
        self.start_pos=None
        self.goal_pos=None
        self.current=None
        self.player_coords=None
        self.counter=0
        
        #generation part
        self.maze=generation(row=self.maze_height, length=self.maze_width, 
                             wall_length=r(0,5))
        self.find_starting_position()
        
        #creating menu
        self.MainMenu=Menu(self.mainWin)
        self.main = Menu(self.MainMenu, tearoff=0)
        self.main.add_command(label=u"Ukončit", command=self.close_app)
        self.MainMenu.add_cascade(label=u"Hlavní", menu=self.main)
        self.MainMenu.add_command(label=u"Nova hra", command=self.new_game)
         
        #win one
        self.map=Canvas(self.mainWin, width=650, height=650, bg="white")
        self.counterlbl=Label(self.mainWin, 
                              text=u"Počet kroků: {0:d} | "
                                   u"Pozice-X: {1:d} | "
                                   u"Pozice-Y: {2:d}".format(self.counter,
                                                             self.start_pos[0],
                                                             self.start_pos[-1]),
                              relief=SUNKEN, borderwidth=1, width=85)                        
        self.map.pack()
        self.counterlbl.pack()
    
        #add menu
        self.mainWin.config(menu=self.MainMenu)    
    
        #bind - func, methods, protocols
        self.mainWin.bind("<F1>", self.show_maze)
        self.mainWin.bind("<F2>", self.new_game)
        self.mainWin.bind("<Left>", self.left_movement)
        self.mainWin.bind("<Right>", self.right_movement)
        self.mainWin.bind("<Up>", self.up_movement)
        self.mainWin.bind("<Down>", self.down_movement)
        self.mainWin.bind("<F3>", self.count)
        self.mainWin.protocol("WM_DELETE_WINDOW", self.close_app)        
        self.mainWin.bind("<Escape>", self.close_app)
        self.new_game()
        
        
    def find_starting_position(self, *args):
        """
            Method for find / check positions of player and goal
        """
        for i, row in enumerate(self.maze):
            if 3 in row:
                self.start_pos=(i, row.index(3))
                self.current=self.start_pos
                break
        for i_2, row_2 in enumerate(self.maze):
            if 4 in row_2:
                self.goal_pos=(i_2, row_2.index(4))
                break
     
    def new_game(self, *args):
        """
            Method for new game
        """
        self.maze_width=simpledialog.askinteger(u"Rozměry bludište",
                                                u"Zvolte nové rozměry bludiště",
                                                initialvalue=self.maze_width)
        if  self.maze_width:
            self.maze_height=self.maze_width
            self.generate_maze()
            self.find_starting_position()
            self.show_maze()
            self.counter=0
            self.mainWin.focus()
        else:
            pass
       
    def generate_maze(self, *args):
        """
            Method of generating maze
        """
        self.maze=generation(row=self.maze_height, length=self.maze_width, 
                             wall_length=r(0,5))
                             
    def show_player(self, *args):
        """
            Method for render player in maze
        """
        self.map.delete("player")
        self.map.create_rectangle(self.player_coords[0],
                                  self.player_coords[1],
                                  self.player_coords[2],
                                  self.player_coords[-1],
                                  fill="#ff3300", outline="white", width=0,
                                  tag="player")
        
    def show_maze(self, *args):
        """
            Method graphics rendering of maze
        """
        self.map.delete(ALL)
        self.box_height=(int(self.map.cget("height"))/self.maze_height)
        self.box_width=(int(self.map.cget("width"))/self.maze_width)
        print(self.box_height, self.box_width) #widt, height one square
        self.x1=0
        self.y1=0
        self.x2=self.box_width
        self.y2=self.box_height
        for row in range(0,(len(self.maze))):
            for cell, value in enumerate(self.maze[row]):
                if value == 0:
                    self.map.create_rectangle(self.x1, self.y1, 
                                  self.x2, self.y2, fill="#cccccc",
                                  outline="white", width=0)
                elif value == 1:
                    self.map.create_rectangle(self.x1, self.y1, 
                                  self.x2, self.y2, fill="black",
                                  outline="white", width=0)
        
                elif value == 3:
                    self.map.create_rectangle(self.x1, self.y1, 
                                  self.x2, self.y2, fill="#cccccc",
                                  outline="white", width=0, 
                                  tag="star_pos_player")
                
                elif value == 4:
                    self.map.create_rectangle(self.x1, self.y1, 
                                  self.x2, self.y2, fill="#ffff00",
                                  outline="white", width=0)
                self.x1=self.x1+self.box_width
                self.x2=self.x2+self.box_width
            
            self.x1=0
            self.x2=self.box_width
            self.y1=self.y1+self.box_height
            self.y2=self.y2+self.box_height
        
        self.player_coords=self.map.coords("star_pos_player")
        self.map.create_rectangle(self.player_coords[0],
                                  self.player_coords[1],
                                  self.player_coords[2],
                                  self.player_coords[-1],
                                  fill="#ff3300", outline="white", width=0,
                                  tag="player")
    
    def left_movement(self, *args):
        """
            Method to move left
        """
        if self.maze[self.current[0]][self.current[-1]-1] == 1:
            pass
        else:
            self.new_pos=(self.current[0],self.current[-1]-1)
            self.maze[self.current[0]][self.current[-1]]=0
            self.maze[self.new_pos[0]][self.new_pos[-1]]=3
            self.current=self.new_pos
            self.counter=self.counter+1
            self.counterlbl.config(text=u"Počet kroků: {0:d} | "
                                   u"Pozice-X: {1:d} | "
                                   u"Pozice-Y: {2:d}".format(self.counter,
                                                             self.current[0],
                                                             self.current[-1])
                                  )
            self.player_coords=self.map.coords('player')
            self.player_coords=[(self.player_coords[0]-self.box_width),
                                self.player_coords[1],
                                (self.player_coords[2]-self.box_width),
                                self.player_coords[-1],]
            self.show_player()                      
            #self.show_maze()
            if self.current == self.goal_pos:
                messagebox.showinfo(u"Výhra",u"Došel jste k cíli.")
                self.new_game()
            else:
                pass
    
    def right_movement(self, *args):
        """
            Method to move right
        """
        if self.maze[self.current[0]][self.current[-1]+1] == 1:
            pass
        else:
            self.new_pos=(self.current[0],self.current[-1]+1)
            self.maze[self.current[0]][self.current[-1]]=0
            self.maze[self.new_pos[0]][self.new_pos[-1]]=3
            self.current=self.new_pos
            self.counter=self.counter+1
            self.counterlbl.config(text=u"Počet kroků: {0:d} | "
                                   u"Pozice-X: {1:d} | "
                                   u"Pozice-Y: {2:d}".format(self.counter,
                                                             self.current[0],
                                                             self.current[-1])
                                  )
            self.player_coords=self.map.coords('player')
            self.player_coords=[(self.player_coords[0]+self.box_width),
                                self.player_coords[1],
                                (self.player_coords[2]+self.box_width),
                                self.player_coords[-1],]
            self.show_player()
            if self.current == self.goal_pos:
                messagebox.showinfo(u"Výhra",u"Došel jste k cíli.")
                self.new_game()
            else:
                pass
    
    def up_movement(self, *args):
        """
            Method to move up
        """
        if self.maze[self.current[0]-1][self.current[-1]] == 1:
            pass
        else:
            self.new_pos=(self.current[0]-1,self.current[-1])
            self.maze[self.current[0]][self.current[-1]]=0
            self.maze[self.new_pos[0]][self.new_pos[-1]]=3
            self.current=self.new_pos
            self.counter=self.counter+1
            self.counterlbl.config(text=u"Počet kroků: {0:d} | "
                                   u"Pozice-X: {1:d} | "
                                   u"Pozice-Y: {2:d}".format(self.counter,
                                                             self.current[0],
                                                             self.current[-1])
                                  )
            self.player_coords=self.map.coords('player')
            self.player_coords=[self.player_coords[0],
                                (self.player_coords[1]-self.box_height),
                                self.player_coords[2],
                                (self.player_coords[-1]-self.box_height)]
            self.show_player()
            #self.show_maze()
            if self.current == self.goal_pos:
                messagebox.showinfo(u"Výhra",u"Došel jste k cíli.")
                self.new_game()
            else:
                pass
    
    def down_movement(self, *args):
        """
            Method to move down
        """
        if self.maze[self.current[0]+1][self.current[-1]] == 1:
            pass
        else:
            self.new_pos=(self.current[0]+1,self.current[-1])
            self.maze[self.current[0]][self.current[-1]]=0
            self.maze[self.new_pos[0]][self.new_pos[-1]]=3
            self.current=self.new_pos
            self.counter=self.counter+1
            self.counterlbl.config(text=u"Počet kroků: {0:d} | "
                                   u"Pozice-X: {1:d} | "
                                   u"Pozice-Y: {2:d}".format(self.counter,
                                                             self.current[0],
                                                             self.current[-1])
                                  )
            self.player_coords=self.map.coords('player')
            self.player_coords=[self.player_coords[0],
                                (self.player_coords[1]+self.box_height),
                                self.player_coords[2],
                                (self.player_coords[-1]+self.box_height)]
            self.show_player()                                  
            #self.show_maze()
            if self.current == self.goal_pos:
                messagebox.showinfo(u"Výhra",u"Došel jste k cíli.")
                self.new_game()
            else:
                pass
    
    def count(self, *args):
        """
            Method for counting steps
        """
        self.counter=self.counter+1
        
    
    def close_app(self, *args):
        """
            Method of closing app
        """
        if messagebox.askyesno(u"Ukončení programu",
                               u"Opravdu chcete ukončit aplikaci?"):
            self.mainWin.destroy()
        else:
            pass
        
###############################################################################

root=Tk()
app=print_maze(root)
app.mainloop()
