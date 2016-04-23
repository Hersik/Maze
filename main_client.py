# -*- coding: utf-8 -*-
"""
Quest:Maze
"""
###############################################################################
from pybots_client import (Bot, )
from gen.path_generator import moves, objecttomap, show, find_players
from random import randint as r
from tkinter import (Tk, Label, Frame, messagebox, Canvas, SUNKEN, Menu, 
                     simpledialog, ALL) 
from time import sleep
###############################################################################

class Maze_printer(Frame):
    def __init__(self, mainWin):
        super().__init__(mainWin)
        self.mainWin = mainWin
        self.mainWin.wm_title(u"Bludiště")
        self.mainWin.wm_geometry("{0}x{1}+"
                                 "{2}+{3}".format(self.mainWin.winfo_screenwidth()-15,
                                                  self.mainWin.winfo_screenheight()-95,
                                                  0,0))
        #variables
        self.maze_width = 0
        self.maze_height = 0
        self.box_width = 0
        self.box_height = 0
        self.mybot_position = None
        self.enemy_position = None
        self.goal_position = None
        self.current = None
        self.player_coords = None
        self.enemy_coords = None
        self.counter = 0
        self.MyBot = None
        self.data = ""
        self.bot_path = ""
        self.bots_position = None
        self.player_x=StringVar()
        self.player_y=StringVar()
        
        #creating menu
        self.MainMenu = Menu(self.mainWin)
        self.main = Menu(self.MainMenu, tearoff=0)
        self.main.add_command(label=u"Ukončit", command=self.close_app)
        self.MainMenu.add_cascade(label=u"Hlavní", menu=self.main)
        self.MainMenu.add_command(label=u"Nova hra", command=self.new_game)
         
        #win one
        self.map=Canvas(self.mainWin, width=650, height=650, bg="white")
        self.counterlbl=Label(self.mainWin, 
                              text=u"Počet kroků: {0:d} | "
                                   u"Pozice-X: {1:s} | "
                                   u"Pozice-Y: {2:s}".format(self.counter,
                                                             self.player_x.get(), 
                                                             self.player_y.get()),
                              relief=SUNKEN, borderwidth=1, width=85)                        
        self.map.pack()
        self.counterlbl.pack()
    
        #add menu
        self.mainWin.config(menu=self.MainMenu)    
    
        #bind - func, methods, protocols
        self.mainWin.bind("<F1>", self.show_maze)
        self.mainWin.bind("<F2>", self.step)
        self.mainWin.bind("<F3>", self.game)
        self.mainWin.bind("<F5>", self.new_game)
        self.mainWin.bind("<Escape>", self.close_app)
        self.mainWin.protocol("WM_DELETE_WINDOW", self.close_app)        
        
    def new_game(self, *args):
        """
            Method for new game
        """
        if messagebox.askyesno(u"Nova hra",u"Chcete založit novou hru?"):
           self.MyBot = Bot('hroch.spseol.cz')
           self.data = self.MyBot.getdata()
           informations = self.MyBot.getmap()
           self.bots_position = find_players(informations)
           informations = objecttomap(informations)
           self.bot_path = moves(labyrint=informations[0],location=informations[-1], 
                                 start=informations[1])
           print(self.bots_position)
           self.maze = informations[0]
           self.maze_height = len(self.maze)
           self.maze_width = len(self.maze[0])
           self.mybot_position = self.bots_position.get("my_bot")
           self.enemy_position = self.bots_position.get("enemy_bot")
           self.player_x.set(self.mybot_position[0])
           self.player_y.set(self.mybot_position[-1])
           self.counterlbl.config(text=u"Počet kroků: {0:d} | "
                                  u"Pozice-X: {1:s} | "
                                  u"Pozice-Y: {2:s}".format(self.counter,
                                                            self.player_x.get(), 
                                                            self.player_y.get())
                                 )
           self.show_maze()
           self.show_players()
        else:
            pass   
               
    def show_players(self, *args):
        """
            Method for render player in maze
        """
        #x1, y1, x2, y2
        self.player_coords = [self.mybot_position[-1]*self.box_width,
                              self.mybot_position[0]*self.box_height,
                             (self.mybot_position[-1]*self.box_width)+
                              self.box_width,
                             (self.mybot_position[0]*self.box_height)+
                             self.box_height]
        self.enemy_coords = [self.enemy_position[-1]*self.box_width,
                            self.enemy_position[0]*self.box_height,
                            (self.enemy_position[-1]*self.box_width)+
                            self.box_width,
                            (self.enemy_position[0]*self.box_height)+
                            self.box_height]        
        
        self.map.create_rectangle(self.player_coords[0],
                                  self.player_coords[1],
                                  self.player_coords[2],
                                  self.player_coords[-1],
                                  fill="#00ff00", outline="white", width=0,
                                  tag="bot_my")
                                  
        self.map.create_rectangle(self.enemy_coords[0],
                                  self.enemy_coords[1],
                                  self.enemy_coords[2],
                                  self.enemy_coords[-1],
                                  fill="#ff3300", outline="white", width=0,
                                  tag="bot_enemy")
        
    def show_maze(self, *args):
        """
            Method graphics rendering of maze
        """
        #self.box_height, self.box_width - width, height one square
        self.map.delete(ALL)
        self.box_height = (int(self.map.cget("height"))/self.maze_height)
        self.box_width = (int(self.map.cget("width"))/self.maze_width)
        self.x1 = 0
        self.y1 = 0
        self.x2 = self.box_width
        self.y2 = self.box_height
        for row in self.maze:
            for value in row:
                if value == 0:
                    self.pain_block(color="#cccccc")
                    
                elif value == 1:
                    self.pain_block(color="yellow")                    
        
                elif value == 3:
                    self.pain_block(color="black")
                
                elif value == 2 or value == 4:
                    self.pain_block(color="#cccccc")
                    
                self.x1 = self.x1+self.box_width
                self.x2 = self.x2+self.box_width
            
            self.x1 = 0
            self.x2 = self.box_width
            self.y1 = self.y1+self.box_height
            self.y2 = self.y2+self.box_height
    
    
    def game(self, *args):
        """
            Method of automatic controlling the motion of the robot
        """
        responce=self.MyBot.post('/action', bot_id=self.MyBot.bot_id, 
                                action=self.bot_path[self.counter])
        if responce["state"] == "game_won":
            print(responce["state"])
            messagebox.showinfo(u"Stav hry",u"Vyhrál jsi!")
            self.mainWin.after_cancel()
            self.new_game()
        elif responce["state"] == "game_lost":
            print(responce["state"])
            messagebox.showinfo(u"Stav hry",u"Bohužel jsi prohrál :(")
            self.mainWin.after_cancel()
            self.new_game()
        elif responce["state"] == "movement_error":
            self.map.delete("bot_my")
            self.map.delete("bot_enemy")
            
            informations = objecttomap(responce["game"]["map"])
            self.bot_path = moves(labyrint=informations[0],
                                  location=informations[-1], 
                                  start=informations[1])
            self.bots_position=find_players(responce["game"]["map"])
            self.mybot_position=self.bots_position.get("my_bot")
            self.enemy_position=self.bots_position.get("enemy_bot")                                  
            self.player_x.set(self.mybot_position[0])
            self.player_y.set(self.mybot_position[-1])
            self.show_players()
            self.counterlbl.config(text=u"Počet kroků: {0:d} | "
                                  u"Pozice-X: {1:s} | "
                                  u"Pozice-Y: {2:s}".format(self.counter,
                                                            self.player_x.get(), 
                                                            self.player_y.get()))
            self.counter=0
            
        else: 
            self.map.delete("bot_my")
            self.map.delete("bot_enemy")
            self.bots_position=find_players(responce["game"]["map"])
            self.mybot_position=self.bots_position.get("my_bot")
            self.enemy_position=self.bots_position.get("enemy_bot")
            self.player_x.set(self.mybot_position[0])
            self.player_y.set(self.mybot_position[-1])
            self.show_players()
            self.counterlbl.config(text=u"Počet kroků: {0:d} | "
                                  u"Pozice-X: {1:s} | "
                                  u"Pozice-Y: {2:s}".format(self.counter,
                                                            self.player_x.get(), 
                                                            self.player_y.get()))   
            self.counter=self.counter+1
        self.mainWin.after(600, self.game)
               
    def step(self, *args):
        """
            Method of manually controlling the motion of the robot
        """
        responce = self.MyBot.post('/action', bot_id=self.MyBot.bot_id, 
                                   action=self.bot_path[self.counter])
        self.map.delete("bot_my")
        self.map.delete("bot_enemy")
        if responce["state"] == "game_won":
            messagebox.showinfo(u"Stav hry",u"Vyhrál jsi!")
            self.MyBot.end_connection()
            self.new_game()
            
        self.bots_position = find_players(responce["game"]["map"])
        self.mybot_position=self.bots_position.get("my_bot")
        self.enemy_position=self.bots_position.get("enemy_bot")
        self.player_x.set(self.mybot_position[0])
        self.player_y.set(self.mybot_position[-1])
        print(responce["state"])
        self.show_players()
        self.counterlbl.config(text=u"Počet kroků: {0:d} | "
                               u"Pozice-X: {1:s} | "
                               u"Pozice-Y: {2:s}".format(self.counter,
                                                         self.player_x.get(), 
                                                         self.player_y.get()))
        self.counter=self.counter+1
    
    
    def pain_block(self, color, *args):
        """
            Method for create one cell of maze in canvas
        """
        self.map.create_rectangle(self.x1, self.y1, 
                                  self.x2, self.y2, fill=color, width=0)    
    
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
if __name__ == "__main__":
    root = Tk()
    app = Maze_printer(root)
    app.mainloop()
