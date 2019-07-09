#-- main.py
#-- Assignment #3 of GEO1002--2017
#-- Script by Hugo Ledoux <h.ledoux@tudelft.nl> and Ravi Peters <r.y.peters@tudelft.nl>
#-- 2015/09/30

from interface import GEO1002_hw3_interface

def main():
    print("Initialised with default polygon. For testing custom polygons copy the content of a WKT file and paste it in the GUI window.")
    gui = GEO1002_hw3_interface()
    gui.mainloop()

if __name__ == "__main__":
    main()
