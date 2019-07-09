#-- wktparser.py
#-- Assignment #3 of GEO1002--2017
#-- Script by Hugo Ledoux <h.ledoux@tudelft.nl> and Ravi Peters <r.y.peters@tudelft.nl>
#-- 2015/09/30

from re import compile as _regexp_compile

class WKTUnSerializer:
    """
    Class to transform a WKT string to a Python geometry object
    """
    def __init__(self):
        self.rx_coord_list = _regexp_compile(
                    r"[ \t]*(\([ \t]*)*(?P<coords>[^\)]+)[ \t]*(\)[ \t]*)+,?"
                    )
        self._wkt_types = ["POLYGON",
                           "LINESTRING",
                           "POINT", ]

    def from_wkt(self, wkt):
        """
        Return the geometry given in well-known text format as python objects
    
        The function accepts only 2D data and supports the POINT, LINESTRING 
        and POLYGON geometries.

        The string wkt may contain an SRID specification in addition to the
        actual geometry. This SRID is ignored.
        """
        parts = wkt.split(";")
        for part in parts:
            part = part.strip()
            if part.startswith("SRID"):
                # ignore SRIDs
                continue
            else:
                for geotype in self._wkt_types:
                    
                    if part.upper().startswith(geotype) and geotype == 'POINT':
                        return 'POINT', self.parse_coord(part[len(geotype):])
                    elif part.upper().startswith(geotype) and geotype == 'LINESTRING':
                        return 'LINESTRING', self.parse_linestring(part[len(geotype):])
                    elif part.upper().startswith(geotype) and geotype == 'POLYGON':
                        return 'POLYGON', self.parse_polygon(part[len(geotype):])
                
                else:
                    raise ValueError("Unsupported WKT-part %s" % repr(part[:20]))
        else:
            raise ValueError("No recognized geometry in WKT string")
    def parse_coordinate_lists(self, wkt):
        """Return the coords in wkt as a list of lists of coord_t pairs.
    
        The wkt parameter is the coord_t part of a geometry in well-known
        text format.
        """
        geometry = []
        while wkt:
            match = self.rx_coord_list.match(wkt)
            if match:
                poly = []
                wktcoords = match.group("coords")
                for pair in wktcoords.split(","):
                    # a pair may be a triple actually. For now we just
                    # ignore any third value
                    x, y = map(float, pair.split()[:2])
                    poly.append( (x, y) )
                geometry.append(poly)
                wkt = wkt[match.end(0):].strip()
            else:
                raise ValueError("Invalid well-known-text (WKT) syntax")
        return geometry
    def parse_polygon(self, wkt):
        """Return the POLYGON geometry in wkt as a list of float pairs"""
        return self.parse_coordinate_lists(wkt)
    def parse_linestring(self, wkt):
        """Return the LINESTRING geometry in wkt as a list of geomtools.Point"""
        ls = []
        c = self.parse_coordinate_lists(wkt)[0]
        for i in c:
            ls.append( (i[0], i[1]) )        
        return ls
    def parse_coord(self, wkt):
        """Return the POINT geometry in wkt format as pair of floats"""
        c = self.parse_coordinate_lists(wkt)[0][0]
        return (c[0], c[1])
