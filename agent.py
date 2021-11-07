from shapely.geometry import LineString, Point, Polygon
import numpy as np
import math

class agent:
    def __init__(self, pos, props):
        self.x, selfy = pos
        self.props = {"spped":0, "scan":0.00001}
        self.props = props
        self.p_i = Point()
        self.p_f = Point()
        self.road = LineString()
        self.road_index = 0

        
    def follow_line(self):
        angle = math.atan2(self.p_f.xy[0][0] - self.p_i.xy[0][0], self.p_f.xy[1][0] - self.p_i.xy[1][0])
        
        self.x += math.cos(angle) * self.props["speed"]
        self.y += math.sin(angle) * self.props["speed"]

    def find_linestrings(self, roads):
        scan = Polygon( (self.x+math.cos(x)*self.props["scan"], self.y+math.sin(x)*self.props["scan"]) for x in np.arange(-1*np.pi, np.pi, np.pi/4))
        
        line_roads = roads[roads.within(scan)]
        """
        line_roads = []
        for r in roads:
            if r.intersects(scan):
                line_roads.append(r)
        """
        return line_roads


    def line_point(self, p, a, b):
        P = (p.xy[0][0], p.xy[1][0])
        A = (a.xy[0][0], a.xy[1][0])
        B = (b.xy[0][0], b.xy[1][0])
        
        area = abs ( (A.x - P.x) * (B.y - P.y) - (A.y - P.y) * (B.x - P.x) )
        AB = ( (A.x - B.x) ** 2 + (A.y - B.y) ** 2 ) ** 0.5
        h = ( area / AB )
        l1 = ( (P.x - A.x) ** 2 + (P.y - A.y) ** 2 ) ** 0.5
        l2 = ( (P.x - B.x) ** 2 + (P.y - B.y) ** 2 ) ** 0.5
        return h, l1, l2
        
    def find_destination(self, roads, mode):
        self.p_i = Point((self.x, self.y))
        
        road = self.find_linestrings(roads)

        min_dis = 1
        
        self.p_f = (self.x, self.y)
        
        for r in road:
            set = False
            for i in range(r.xy[0]-1):
                h, l1, l2 = self.line_point((self.x, self.y), (r.xy[0][i], r.xy[1][i]), (r.xy[0][i+1], r.xy[1][i+1]))
                dis = min((h, l1, l2))
                if dis<min_dis:
                   if not set:
                       set = True
                       self.road = r
                    self.road_index = i

                    
                    min_dis = dis
                    if dis==h:
                        u = np.array([self.x - r.xy[0][i], self.y - r.xy[1][i]])
                        v = np.array([r.xy[0][i+1] - r.xy[0][i], r.xy[1][i+1] - r.xy[1][i]])
                        
                        v_norm = np.sqrt(sum(v**2))    

                        proj_of_u_on_v = (np.dot(u, v)/v_norm**2)*v + np.array([r.xy[0][i], r.xy[1][i]])
                        
                        self.p_f = tuple(proj_of_u_on_v)]
                        
                    elif dis==l1:
                        self.p_f = (r.xy[0][i], r.xy[1][i])
                        
                    elif dis==l2:
                        self.p_f = (r.xy[0][i+1], r.xy[1][i+1])]
                        
        
    def find_destination(self):
