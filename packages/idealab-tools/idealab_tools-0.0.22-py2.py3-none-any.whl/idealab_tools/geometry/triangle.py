# -*- coding: utf-8 -*-
"""
copyright 2016-2017 Dan Aukes
"""
import numpy
import numpy.linalg

class Triangle(object):
    def __init__(self,*points):
        self.points = numpy.array(points)

    def centroid(self):
        return self.points.sum(0)/len(self.points)
        
    def J(self):
        J = self.points[1:] - self.points[0]
        return J

    def area(self):
        return abs(numpy.linalg.det(self.J())/2)

    def extrude(self,z_lower,z_upper):
        from idealab_tools.geometry.tetrahedron import Tetrahedron
        p_lower = numpy.c_[self.points,[z_lower]*3]
        p_upper = numpy.c_[self.points,[z_upper]*3]

        tet1 = Tetrahedron(p_upper[0],p_lower[1],p_lower[0],p_lower[2])
        tet2 = Tetrahedron(p_upper[0],p_lower[1],p_upper[2],p_lower[2])
        tet3 = Tetrahedron(p_upper[0],p_lower[1],p_upper[1],p_upper[2])
        return tet1,tet2,tet3

if __name__=='__main__':
    p0= numpy.array([0,0.1])
    p1= numpy.array([1,0])
    p2= numpy.array([0,1])
    t=Triangle(p0,p1,p2)
    c=t.centroid()    
    J = t.J()
    Jdet = numpy.linalg.det(J)