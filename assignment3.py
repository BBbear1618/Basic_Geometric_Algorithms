#-- assignment3.py
#-- Assignment #3 of GEO1002--2017
#-- Script by Hugo Ledoux <h.ledoux@tudelft.nl> and Ravi Peters <r.y.peters@tudelft.nl>
#-- Implementation by Yifang Zhao <Y.Zhao-18@student.tudelft.nl> and Jinglan Li <J.Li-31@student.tudelft.nl>
#-- 2015/09/30
from wktparser import WKTUnSerializer

def get_area_polygon(polygon):
    """
    !!! TO BE COMPLETED !!!
    
    Function that calculates the area of the input polygon
    
    Input:
        polygon:   a list of the rings of the polygon (outer is polygon[0]). Each ring is a list of tuple.
    Output:
        returns the value of the area

    """   
    area_outer = get_area_single_polygon(polygon[0])
    area_inner = 0
    for poly in polygon[1:]:
        area_inner += get_area_single_polygon(poly)
    return area_outer - area_inner


def get_area_single_polygon(single_polygon):          
    """
    Function that calculates the area of the input single polygon
    
    Input:
        single_polygon:   a ring of the polygon represented by a list of tuple.
    Output:
        returns the value of the area

    """
    x,y = [c[0] for c in single_polygon], [c[1] for c in single_polygon]
    area = 0
    for i in range(len(single_polygon) - 1):
        area += 0.5 * (x[i] * y[i + 1] - x[i + 1] * y[i])
    return abs(area)

    
    
def is_polygon_convex(polygon):
    """
    !!! TO BE COMPLETED !!!
    
    Function that tests if a polygon is convex or not
    
    Input:
        polygon:    a list of the rings of the polygon (outer is polygon[0]). Each ring is a list of tuple.
    Output:
        True:       polygon is convex
        False:      polygon is non-convex

    """   
    x,y = [c[0] for c in polygon[0]], [c[1] for c in polygon[0]]
    x.append(polygon[0][1][0])  #correspondingly append the coordinates of the second point to x,y list
    y.append(polygon[0][1][1])  #for the convenience of calculation of the cross product
    for i in range(len(polygon[0]) - 1):
        if (x[i + 1] - x[i]) * (y[i + 2] - y[i + 1]) - (x[i + 2] - x[i + 1]) * (y[i + 1] - y[i]) > 0:
            return False
    return True
    
    
def is_point_inside_polygon(pt, polygon):
    """
    !!! TO BE COMPLETED !!!
    
    Function that tests if a point is inside a polygon. If the point is on the
    boundary (outer or inners) then it's considered inside.
    
    Input:
        pt:         the point to test (a tuple of coordinates)
        polygon:    a list of the rings of the polygon (outer is polygon[0]). Each ring is a list of tuple.
    Output:
        True:       pt is inside/on polygon
        False:      pt is outside polygon

    """  
    if is_point_inside_single_polygon(pt, polygon[0], True):
        for flag in [is_point_inside_single_polygon(pt, poly, False) for poly in polygon[1:]]:
            if flag:
                return False
        return True
    else:
        return False


def is_point_inside_single_polygon(pt, polygon, on = True):
    """
    Function that tests if a point is inside a polygon. 
    
    Input:
        pt:         the point to test (a tuple of coordinates)
        polygon:    a ring of the polygon represented by a list of tuple.
        on:         if the point on the boundary is considered inside. 'True' means inside and vice versa.
    Output:
        True:       pt is inside polygon
        False:      pt is outside polygon

    """ 
    flag = False
    for i in range(len(polygon) - 1):
        x = pt[0]
        y = pt[1]
        x1 = polygon[i][0]
        y1 = polygon[i][1]
        x2 = polygon[i + 1][0]
        y2 = polygon[i + 1][1]

        if on and ((x == x1 and y ==y1) or (x == x2 and y ==y2)):  #pt is on the border (one of the vertices) of the polygon
            return True
        
        if y1 <= y < y2 or y2 <= y < y1:
            x_crossing_point = (x2 - x1) / (y2 - y1) * (y - y1) + x1
            if on and x_crossing_point == x:  #pt is on the border (not horizontal lines) of the polygon
                return True                  
            elif x_crossing_point > x:        #pt is inside (not on the border of) the polygon
                flag = not flag              
        elif on and y1 == y == y2:           
            if x1 < x < x2 or x2 < x < x1:    #pt is on the border (horizontal lines) of the polygon
                return True
    return flag