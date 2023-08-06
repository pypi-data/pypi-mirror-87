import numpy as np
from sympy.physics.mechanics import *

class Orbit:
    '''Base orbit class that is used to build circular and eliptical orbits
    frame: sympy.ReferenceFrame object
    center: point/trajectory of the attractor #todo rename?
    color: (R,G,B) tuple to be used when plotting trajectory and body'''

    def __init__(self, frame, center, color = (0, 0, 0)):
        self.frame = frame
        self.center = center
        self.color = color
        self.dim = 0

    def get_position(self, epoch) -> Vector:
        pass

    def get_trajectory(self, epoch: np.array, center = None, frame = None):
        '''Returns a 2D or 3D numpy array of results from get_position()
        over time'''
        # todo: fix array dims
        #if self.dim == 3:
        pos = np.zeros_like([epoch, epoch, epoch], dtype = float)
        #elif self.dim ==2:
        #    pos = np.zeros_like([epoch, epoch], dtype = float)

        if frame is None:
            # todo: better explanation of how sympy frames work here,
            # some way to add the possib. of plotting around earth
            frame = self.frame

        for idx, ti in enumerate(epoch):
            # calls get_position() for each time, subtract center position
            if center is None:
                vec = self.get_position(ti).to_matrix(frame)
            else:
                vec = (self.get_position(ti) -
                       center.get_position(ti)).to_matrix(frame)
            pos[:, idx] = vec[:]
        return pos


