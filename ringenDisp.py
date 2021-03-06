# Compile this and other python files to improve start time
# python3 -m py_compile myscript.py

import tkinter as tk

######################################################################
# CONSTANTS
STATUS_ROW_HEIGHT = 30
HORISONTAL_SEGMENTS = 9
VERTICAL_SEGMENTS = 6
LINE_WIDTH = 30


######################################################################
class StatusLbl (tk.Label) :
    def __init__(self, *args, grpName, **kwargs):
        tk.Label.__init__(self, *args, **kwargs)
        self.grpName = grpName
        self.configure(height = 2)
        self.setProblem()

    def setOk(self) :
        t = self.grpName + " OK"
        self.configure(text=t)
        self.configure(background='green')

    def setProblem(self) :
        t = self.grpName + " off-line"
        self.configure(text=t)
        self.configure(background='red')


######################################################################
class TurnoutCnv (tk.Canvas) :
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.width = kwargs["width"]
        self.height = kwargs["height"]
        self.configure(background='dark green')
    
    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

######################################################################
class Route:
    def __init__(self, canvas,  points):
        self.canvas = canvas
        self.canvasId = self.canvas.create_line(points)
        self.canvas.itemconfig(self.canvasId, joinstyle = tk.ROUND, capstyle=tk.BUTT, fill='gray42', width=LINE_WIDTH)

    def setBlocked(self):
        self.canvas.itemconfig(self.canvasId, fill='red')
        self.canvas.tag_lower(self.canvasId)

    def setFree(self):
        self.canvas.itemconfig(self.canvasId, fill='lawn green')
        self.canvas.tag_raise(self.canvasId)

    def setUnknown(self):
        self.canvas.itemconfig(self.canvasId, fill='gray42')
        self.canvas.tag_lower(self.canvasId)

######################################################################
class RingenRoutes:
    def __init__(self, canvas):
        self.canvas = canvas
        # Need to initialise the two dimensional array first. First index is group, second index is route
        self.routes = [[object] * 6 for i in range(5)] 

    def draw(self):
        HS = HORISONTAL_SEGMENTS
        VS = VERTICAL_SEGMENTS
        ZERO = LINE_WIDTH // 2
        X = (self.canvas.getWidth() // HS)
        Y = (self.canvas.getHeight() // VS)
        
        #VxlGrp1
        points = [(ZERO,Y+ZERO), (ZERO,Y),(X,ZERO), (2*X,ZERO), (3*X, ZERO), (4*X, ZERO)]
        self.routes[1][1] = Route(self.canvas, points)

        points = [(X,Y+ZERO), (X,Y),(2*X,ZERO), (3*X, ZERO), (4*X, ZERO)]
        self.routes[1][2] = Route(self.canvas, points)

        points = [(2*X,Y+ZERO), (2*X,Y), (3*X, ZERO), (4*X, ZERO)]
        self.routes[1][3] = Route(self.canvas, points)

        points = [(3*X,2*Y),(3*X,Y), (4*X, ZERO)]
        self.routes[1][4] = Route(self.canvas, points)

        #VxlGrp2
        points = [(2*X,(VS*Y - ZERO)),(3*X,(VS*Y - ZERO)), (4*X,(VS*Y - ZERO))]
        self.routes[2][1] = Route(self.canvas, points)

        points = [(2*X,(VS-1)*Y),(3*X,(VS-1)*Y), \
                  (4*X,(VS*Y - ZERO)), (4*X+ZERO,(VS*Y - ZERO))]
        self.routes[2][2] = Route(self.canvas, points)

        points = [(2*X,(VS-1)*Y),(3*X,(VS-1)*Y), (4*X,(VS-1)*Y),(5*X,(VS-1)*Y)]
        self.routes[2][3] = Route(self.canvas, points)

        points = [(2*X,(VS-3)*Y-ZERO), (2*X,(VS-3)*Y),(3*X,(VS-2)*Y), \
                  (4*X,(VS-1)*Y),(5*X,(VS-1)*Y)]
        self.routes[2][4] = Route(self.canvas, points)

        points = [(2*X,(VS-3)*Y-ZERO), (2*X,(VS-3)*Y),(3*X,(VS-2)*Y), \
                  (4*X,(VS-2)*Y),(5*X,(VS-3)*Y)]
        self.routes[2][5] = Route(self.canvas, points)

        #VxlGrp3
        points = [((HS-2)*X+ZERO,(VS*Y - ZERO)), ((HS-3)*X,(VS*Y - ZERO))]
        self.routes[3][1] = Route(self.canvas, points)

        points = [((HS-2)*X+ZERO,(VS*Y - ZERO)), ((HS-2)*X,(VS*Y - ZERO)), \
                  ((HS-3)*X,(VS-1)*Y), ((HS-3)*X-ZERO,(VS-1)*Y)]
        self.routes[3][2] = Route(self.canvas, points)

        points = [((HS-1)*X,(VS-2)*Y-ZERO), ((HS-1)*X,(VS-2)*Y), ((HS-2)*X,(VS-1)*Y), \
                  ((HS-3)*X-ZERO,(VS-1)*Y)]
        self.routes[3][3] = Route(self.canvas, points)

        points = [((HS-3)*X-ZERO,(VS-1)*Y), ((HS-4)*X-ZERO,(VS-1)*Y)]
        self.routes[3][4] = Route(self.canvas, points)

        points = [((HS-4)*X-ZERO,(VS-1)*Y), ((HS-4)*X,(VS-1)*Y), ((HS-3)*X,(VS-2)*Y)]
        self.routes[3][5] = Route(self.canvas, points)

        #VxlGrp4
        points = [((HS*X-ZERO),Y+ZERO),((HS*X-ZERO),Y),((HS-1)*X,ZERO), \
                  ((HS-2)*X-ZERO,ZERO)]
        self.routes[4][1] = Route(self.canvas, points)

        points = [((HS-1)*X,Y+ZERO), ((HS-1)*X,Y), ((HS-2)*X,ZERO), \
                  ((HS-2)*X-ZERO,ZERO)]
        self.routes[4][2] = Route(self.canvas, points)

        #Intermediate tracks
        tmp = []

        points= [(4*X, ZERO), (5*X, ZERO)]
        tmp.append(self.canvas.create_line(points))

        points= [((HS-4)*X,ZERO), ((HS-2)*X,ZERO)]
        tmp.append(self.canvas.create_line(points))

        points= [(ZERO,Y+ZERO), (ZERO,(VS-1)*Y), (X,(VS*Y - ZERO)), (2*X,(VS*Y - ZERO))]
        tmp.append(self.canvas.create_line(points))

        points= [(X,Y+ZERO), (X,(VS-2)*Y), (2*X,(VS-1)*Y)]
        tmp.append(self.canvas.create_line(points))

        points= [(2*X,Y+ZERO), (2*X,(VS-3)*Y-ZERO)]
        tmp.append(self.canvas.create_line(points))

        points= [(4*X, (VS*Y - ZERO)), (5*X, (VS*Y - ZERO))]
        tmp.append(self.canvas.create_line(points))

        points= [((HS-4)*X,(VS*Y - ZERO)), ((HS-3)*X,(VS*Y - ZERO))]
        tmp.append(self.canvas.create_line(points))

        points= [((HS-2)*X,(VS*Y - ZERO)), ((HS-1)*X,(VS*Y - ZERO)), ((HS*X-ZERO),(VS-1)*Y), \
                 ((HS*X-ZERO),1*Y+ZERO)]
        tmp.append(self.canvas.create_line(points))

        points= [((HS-1)*X,Y+ZERO), ((HS-1)*X,(VS-2)*Y-ZERO)]
        tmp.append(self.canvas.create_line(points))
        
        for i in tmp:
            self.canvas.itemconfig(i, joinstyle = tk.ROUND, capstyle=tk.BUTT, fill='old lace', width=LINE_WIDTH)
        
    def blocked(self, groupId, routeId):
        self.routes[groupId][routeId].setBlocked()
    def free(self, groupId, routeId):
        self.routes[groupId][routeId].setFree()
    def unknown(self, groupId):
        for i in range(6):
            if isinstance(self.routes[groupId][i], Route):
                self.routes[groupId][i].setUnknown()
                
######################################################################
class layoutWindow:
    def __init__(self, windowTitle):
        self.root = tk.Tk()

        # Create a window at top left that can't be resized
        w, h = self.root.maxsize()
        w = self.root.winfo_screenwidth()
        self.root.minsize(width = w //2, height = h//2 )
        self.root.attributes("-fullscreen", True) # Change to false for debug
        
        self.root.geometry("+0+0")
        self.root.title(windowTitle)
        self.root.configure(background='dark green')
        self.root.update_idletasks() # Needed to update sizes so we can use them below    
        
        # It is nice to have a way to stop the program
        self.root.bind('<Escape>', self.escQuits)
            
        # Add widgets
        self.canvas = TurnoutCnv(self.root, width = self.root.winfo_width(),\
                                 height = self.root.winfo_height() - STATUS_ROW_HEIGHT)
        self.statusLbls = []
        self.statusLbls.append(StatusLbl(self.root, grpName = "Grupp 1"))
        self.statusLbls.append(StatusLbl(self.root, grpName = "Grupp 2"))
        self.statusLbls.append(StatusLbl(self.root, grpName = "Grupp 3"))
        self.statusLbls.append(StatusLbl(self.root, grpName = "Grupp 4"))
        # Place widgets
        self.canvas.grid(row = 0, columnspan = 4, sticky=tk.W+tk.E+tk.N+tk.S)
        for i in range(4):
            self.statusLbls[i].grid(row = 1, column = i, sticky=tk.W+tk.E+tk.S)
        self.root.update_idletasks() # Needed to update sizes so we can use them below
        
        # Draw routes
        self.routes = RingenRoutes(self.canvas)
        self.routes.draw()
        
    # Getters and setters
    def getRoutes(self):
        return self.routes
    def getRoot(self):
        return self.root
    def getStatusLbls(self):
        return self.statusLbls
    
    # Callback function that exit the program
    def escQuits(self, event):
        self.root.destroy()


######################################################################
if __name__ == '__main__':

    w = layoutWindow("Växellägen")
    
    routes = w.getRoutes()

    routes.free(1,1)
    routes.blocked(1,2)
    routes.blocked(2,1)
    routes.blocked(2,2)
    routes.blocked(2,3)
    routes.blocked(2,4)
    routes.blocked(2,5)
    routes.free(4,1)
    routes.blocked(4,2)
    routes.free(3,3)
    routes.free(3,4)
    routes.blocked(3,1)
    routes.blocked(3,2)
    routes.blocked(3,5)
    

    routes.unknown(4)
    routes.unknown(2)
    
    a, h = w.getRoot().maxsize()
    
    w.getRoot().mainloop()


