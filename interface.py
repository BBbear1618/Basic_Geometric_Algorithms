#-- interface.py
#-- Assignment #3 of GEO1002--2017
#-- Script by Hugo Ledoux <h.ledoux@tudelft.nl> and Ravi Peters <r.y.peters@tudelft.nl>
#-- 2015/09/30

try:
    from tkinter import *
except ImportError:
    from Tkinter import *
from assignment3 import is_point_inside_polygon, get_area_polygon, is_polygon_convex
from wktparser import WKTUnSerializer

class GEO1002_hw3_interface(Tk):
    def __init__(self, wkt = "POLYGON ((10 10, 10 400, 400 400, 400 10, 10 10), (50 50, 100 50, 100 100, 50 100, 50 50), (150 150, 150 100, 200 200, 150 150))"):
        Tk.__init__(self)
        self.sizex = self.sizey = 600
        self.title("GEO1002 HW#3 Interface")
        self.resizable(0,0)
        self.bind('q', self.exit)
        self.bind('<<Paste>>', self.paste_wkt)
        self.canvas = Canvas(self, bg="white", width=self.sizex, height=self.sizey)
        self.canvas.pack()
        self.bind("<Motion>", self.display_coords_text)
        self.bind("<ButtonRelease>", self.mouse_click)

        self.tx = 0
        self.ty = 0
        self.scale = 1
        self.contentzoom = 0.7

        self.initialise_from_wkt(wkt)

    def paste_wkt(self, event):
        self.initialise_from_wkt(self.clipboard_get())

    def initialise_from_wkt(self, wkt):
        def print_info_polygon(polygon):
            print ("\n----- INFO ABOUT THE POLYGON -----")
            print("The input polygon has %d holes" % (len(polygon) - 1))
            
            is_convex = is_polygon_convex(polygon)
            if is_convex == True:
                print("The input polygon is CONVEX")
            elif is_convex == False:
                print("The input polygon is CONCAVE")
            else:
                print("is_polygon_convex() function not implemented!")
            
            area = get_area_polygon(polygon)
            if area is None:
                print("get_area_polygon() function not implemented!")
            else:
                print("Its area is: %.2f" % area)

        parser = WKTUnSerializer()
        try: 
            wkt_type, wkt_geom = parser.from_wkt(wkt)
            if wkt_type != "POLYGON":
                print("only POLYGON WKT is supported")
                return
            self.mypoly = wkt_geom
        except ValueError as e:
            print(e)
            return

        print_info_polygon(self.mypoly)

        x,y = [c[0] for c in self.mypoly[0]], [c[1] for c in self.mypoly[0]]
        self.set_transform(min(x), max(x), min(y), max(y))

        self.canvas.delete("all")
        self.coordstext = self.canvas.create_text(self.sizex, self.sizey, anchor='se', text='')
        self.draw_polygon()

    def t(self, x, y):
        """transform data coordinates to screen coordinates"""
        x = (x * self.scale) + self.tx
        y = self.sizey - ((y * self.scale) + self.ty)
        return (x,y)

    def t_(self, x, y):
        """transform screen coordinates to data coordinates"""
        x = (x - self.tx)/self.scale
        y = (self.sizey - y - self.ty)/self.scale
        return (x,y)

    def set_transform(self, minx, maxx, miny, maxy):
        """compute screen transformation parameters based on given data extent"""
        d_x = maxx-minx
        d_y = maxy-miny
        c_x = minx + (d_x)/2
        c_y = miny + (d_y)/2

        self.tx = self.sizex/2 - c_x
        self.ty = self.sizey/2 - c_y

        if d_x > d_y:
            self.scale = (self.sizex*self.contentzoom) / d_x
        else:
            self.scale = (self.sizey*self.contentzoom) / d_y

        self.tx = self.sizex/2 - c_x*self.scale
        self.ty = self.sizey/2 - c_y*self.scale
        
    def mouse_click(self, event):
        x,y = self.t_(event.x,event.y)
        is_inside = is_point_inside_polygon( (x, y), self.mypoly )
        if is_inside == True:
            self.draw_point(x, y, fill='green')
            print("Point (%.2f,%.2f) is INSIDE" % (x, y))
        elif is_inside == False:
            self.draw_point(x, y, fill='red')
            print("Point (%.2f,%.2f) is OUTSIDE" % (x, y))
        else:
            print("is_point_inside_polygon() function not implemented!")
        
    def display_coords_text(self, event):
        s = "(%.2f,%.2f)" % self.t_(event.x,event.y)
        self.canvas.itemconfig(self.coordstext, text=s)

    def draw_point(self, x, y, inside=False, **attributes):
        x,y = self.t(x,y)
        r = 4
        self.canvas.create_oval(x-r, y-r, x+r, y+r, outline='white', **attributes)

    def draw_polygon(self):
        for number,ring in enumerate(self.mypoly):
            temp = []
            for i in range(len(ring)-1):
                x,y = self.t(ring[i][0],ring[i][1])
                temp.append(x)
                temp.append(y)
            if number == 0:
                self.canvas.create_polygon(temp, fill="lightgray", outline='black')
            else:
                self.canvas.create_polygon(temp, fill="white", outline='darkgray')
        
    def exit(self, event):
        print("bye bye.")
        self.destroy()
