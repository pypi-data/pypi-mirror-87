import turtle


class visualize_team_selection_442:
    def __init__(self, list_of_goalies, list_of_defenders, list_of_midfielders, list_of_strikers, cash_left):
        self.list_of_goalies = list_of_goalies
        self.list_of_defenders = list_of_defenders
        self.list_of_midfielders = list_of_midfielders
        self.list_of_strikers = list_of_strikers
        self.cash_left = cash_left

    def draw_pitch(self):
        '''
        Uses turtle graphics to visualize a soccer field 
        '''
        GREEN="#149118"
        screen = turtle.Screen()
        screen.tracer(0)
        screen.bgcolor(GREEN)
    
        myBrush = turtle.Turtle()
        myBrush.width(1)
        myBrush.hideturtle()
    
        myBrush.speed(0)
        myBrush.color("#FFFFFF")
    
        #Outer lines
        myBrush.penup()
        myBrush.goto(-250,280)
        myBrush.pendown()
        myBrush.goto(250,280)
        myBrush.goto(250,-220)
        myBrush.goto(-250,-220)
        myBrush.goto(-250,280)
    
        #Penalty Box - Top
        myBrush.penup()
        myBrush.goto(0,190)
        myBrush.pendown()
        myBrush.circle(40)
        myBrush.penup()
        myBrush.goto(-100,280)
        myBrush.pendown()
        myBrush.fillcolor(GREEN)
        myBrush.begin_fill()
        myBrush.goto(100,280)
        myBrush.goto(100,215)
        myBrush.goto(-100,215)
        myBrush.goto(-100,280)  
        myBrush.end_fill()
    
        #Penalty Box - Bottom 
        myBrush.penup()
        myBrush.goto(0,-210)
        myBrush.pendown()
        myBrush.circle(40)
        myBrush.penup()
        myBrush.goto(-100,-220)
        myBrush.pendown()
        myBrush.fillcolor(GREEN)
        myBrush.begin_fill()
        myBrush.goto(100,-220)
        myBrush.goto(100,-155)
        myBrush.goto(-100,-155)
        myBrush.goto(-100,-220)  
        myBrush.end_fill()

        # Goal Box - Bottom
        myBrush.penup()
        myBrush.goto(40,-220)
        myBrush.pendown()
        myBrush.goto(40,-195)
        myBrush.goto(-40,-195)
        myBrush.goto(-40,-220)  

        # Goal Box - Top
        myBrush.penup()
        myBrush.goto(40,280)
        myBrush.pendown()
        myBrush.goto(40,255)
        myBrush.goto(-40,255)
        myBrush.goto(-40,280)     
    
        #Halfway Line
        myBrush.penup()
        myBrush.goto(-250,30)
        myBrush.pendown()
        myBrush.goto(250,30)
    
        #Central Circle
        myBrush.penup()
        myBrush.goto(0,-10)
        myBrush.pendown()
        myBrush.circle(40)
    
        screen.tracer(1)  

    def draw_player(self, color, x, y, label):
        screen = turtle.Screen()
        screen.tracer(0)
        myPen = turtle.Turtle()
        myPen.hideturtle()
        myPen.penup()
        myPen.goto(x,y)
        myPen.fillcolor(color)
        myPen.begin_fill()
        myPen.circle(10)
        myPen.end_fill()
        screen.tracer(1)  
        myPen.penup()
        x_offset = (len(label)/2) * 5
        myPen.goto(x-x_offset,y-20)
        myPen.write(label[4:])

    def draw_bench(self):
        #Will have 1 defenders, 1 midfielder, 1 striker, 1 goalie on bench
        self.draw_player("red", -260, -270, self.list_of_goalies[1]) 
        self.draw_player("red", -140, -270, self.list_of_defenders[4]) 
        self.draw_player("red", -20, -270, self.list_of_midfielders[4]) 
        self.draw_player("red", 100, -270, self.list_of_strikers[2]) 
        #Add Cash Remaining:
        cash_left_label = "Cash Remaining: " + str(self.cash_left)
        self.draw_player("white", 300, -270, cash_left_label)

    def draw_starting_eleven(self):
        #Draw Gk
        self.draw_player("blue", -0, -190, self.list_of_goalies[0]) 

        #Draw 4 defenders
        self.draw_player("yellow", 175, -120, self.list_of_defenders[0]) 
        self.draw_player("yellow", -60, -120, self.list_of_defenders[1]) 
        self.draw_player("yellow", 60, -120, self.list_of_defenders[2]) 
        self.draw_player("yellow", -175, -120, self.list_of_defenders[3]) 

        #Draw 4 Midfielders
        self.draw_player("yellow", 225, 20, self.list_of_midfielders[0]) 
        self.draw_player("yellow", -75, 20, self.list_of_midfielders[1]) 
        self.draw_player("yellow", 75, 20, self.list_of_midfielders[2]) 
        self.draw_player("yellow", -225, 20, self.list_of_midfielders[3]) 

        #Draw 2 Strikers
        self.draw_player("yellow", -60, 150, self.list_of_strikers[0]) 
        self.draw_player("yellow", 60, 150, self.list_of_strikers[1]) 

    def run_visualization(self):
        self.draw_pitch()
        self.draw_starting_eleven()
        self.draw_bench()
        turtle.mainloop()


class visualize_team_selection_343(visualize_team_selection_442):

    def draw_bench(self):
       #Will have 2 defenders, 1 midfielder, 1 goalie on bench
        self.draw_player("red", -260, -270, self.list_of_goalies[1]) 
        self.draw_player("red", -140, -270, self.list_of_defenders[3]) 
        self.draw_player("red", -20, -270, self.list_of_defenders[4]) 
        self.draw_player("red", 100, -270, self.list_of_midfielders[4]) 
        #Add Cash Remaining:
        cash_left_label = "Cash Remaining: " + str(self.cash_left)
        self.draw_player("white", 300, -270, cash_left_label)

    def draw_starting_eleven(self):
        #Draw Gk
        self.draw_player("blue", -0, -190, self.list_of_goalies[0]) 

        #Draw 3 defenders
        self.draw_player("yellow", -150, -130, self.list_of_defenders[0]) 
        self.draw_player("yellow", 0, -130, self.list_of_defenders[1]) 
        self.draw_player("yellow", 150, -130, self.list_of_defenders[2]) 

        #Draw 4 Midfielders
        self.draw_player("yellow", 225, 20, self.list_of_midfielders[0]) 
        self.draw_player("yellow", -75, 20, self.list_of_midfielders[1]) 
        self.draw_player("yellow", 75, 20, self.list_of_midfielders[2]) 
        self.draw_player("yellow", -225, 20, self.list_of_midfielders[3]) 

        #Draw 3 Strikers
        self.draw_player("yellow", -150, 150, self.list_of_strikers[0]) 
        self.draw_player("yellow", 0, 150, self.list_of_strikers[1]) 
        self.draw_player("yellow", 150, 150, self.list_of_strikers[2]) 


class visualize_team_selection_352(visualize_team_selection_442):

    def draw_bench(self):
        #Will have 2 defenders 1 striker, 1 goalie on bench
        self.draw_player("red", -260, -270, self.list_of_goalies[1]) 
        self.draw_player("red", -140, -270, self.list_of_defenders[3]) 
        self.draw_player("red", -20, -270, self.list_of_defenders[4]) 
        self.draw_player("red", 100, -270, self.list_of_strikers[2]) 
        #Add Cash Remaining:
        cash_left_label = "Cash Remaining: " + str(self.cash_left)
        self.draw_player("white", 300, -270, cash_left_label)

    def draw_starting_eleven(self):
        #Draw Gk
        self.draw_player("blue", -0, -190, self.list_of_goalies[0]) 

        #Draw 3 defenders
        self.draw_player("yellow", -150, -130, self.list_of_defenders[0]) 
        self.draw_player("yellow", 0, -130, self.list_of_defenders[1]) 
        self.draw_player("yellow", 150, -130, self.list_of_defenders[2]) 

        #Draw 5 Midfielders
        self.draw_player("yellow", 220, 20, self.list_of_midfielders[0]) 
        self.draw_player("yellow", 110, -5, self.list_of_midfielders[1]) 
        self.draw_player("yellow", 0, 20, self.list_of_midfielders[2]) 
        self.draw_player("yellow", -110, -5, self.list_of_midfielders[3]) 
        self.draw_player("yellow", -220, 20, self.list_of_midfielders[4]) 

        #Draw 2 Strikers
        self.draw_player("yellow", -75, 150, self.list_of_strikers[0]) 
        self.draw_player("yellow", 75, 150, self.list_of_strikers[1])  


class visualize_team_selection_433(visualize_team_selection_442):

    def draw_bench(self):
       #Will have 2 defenders, 1 midfielder, 1 goalie on bench
        self.draw_player("red", -260, -270, self.list_of_goalies[1]) 
        self.draw_player("red", -140, -270, self.list_of_defenders[4]) 
        self.draw_player("red", -20, -270, self.list_of_midfielders[3]) 
        self.draw_player("red", 100, -270, self.list_of_midfielders[4]) 
        #Add Cash Remaining:
        cash_left_label = "Cash Remaining: " + str(self.cash_left)
        self.draw_player("white", 300, -270, cash_left_label)

    def draw_starting_eleven(self):
        #Draw Gk
        self.draw_player("blue", -0, -190, self.list_of_goalies[0]) 

        #Draw 4 defenders
        self.draw_player("yellow", 225, -130, self.list_of_defenders[0]) 
        self.draw_player("yellow", -75, -130, self.list_of_defenders[1]) 
        self.draw_player("yellow", 75, -130, self.list_of_defenders[2])
        self.draw_player("yellow", -225, -130, self.list_of_defenders[3]) 
 
        #Draw 3 Midfielders
        self.draw_player("yellow", -150, 20, self.list_of_midfielders[0]) 
        self.draw_player("yellow", 0, 20, self.list_of_midfielders[1]) 
        self.draw_player("yellow", 150, 20, self.list_of_midfielders[2]) 
        
        #Draw 3 Strikers
        self.draw_player("yellow", -150, 150, self.list_of_strikers[0]) 
        self.draw_player("yellow", 0, 150, self.list_of_strikers[1]) 
        self.draw_player("yellow", 150, 150, self.list_of_strikers[2]) 
        