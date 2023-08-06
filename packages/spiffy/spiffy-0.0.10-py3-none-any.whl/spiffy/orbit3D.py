from spiffy.orbit import Orbit
from numpy import cos, sin, linspace, pi
from spiffy.plotter import Plotter
from sympy.physics.mechanics import *


class CircularOrbit3D(Orbit):
    """Model of a ideal 3D orbit"""

    def __init__(self, parentFrame, center = None,
                 radius: float = 0, omega: float = 0, inclination: float = 0,
                 phase: float = 0, ascNode: float = 0, color = (0, 0, 0),
                 opt = 'sun'):
        super().__init__(parentFrame, center, color)
        self.frame = parentFrame.orientnew(
                'frame', 'Space', (inclination, 0, ascNode), 123)
        # todo: orient new frame with 'Space'
        # todo: fix frame naming scheme
        self.radius = radius

        self.phase = phase  # todo: rename parm
        self.ascNode = ascNode  # todo: rename parm
        self.dim = 3
        if opt == 'sun':
            self.mu = 1.327e20
        elif opt == 'earth':
            self.mu = 3.986004418e14
        self.period = self.get_period()

    def get_position(self, epoch, frame = None):
        '''given an epoch, returns a sympy vector for position'''
        # todo pass other frame argument
        r = self.radius

        ph = self.phase
        if frame is None:
            frame = self.frame

        x = r * cos((2*pi/self.period)*epoch + ph) * frame.x
        y = r * sin((2*pi/self.period)*epoch + ph) * frame.y
        z = 0 * frame.z
        if self.center is None:
            return x + y + z
        else:
            return x + y + z + self.center.get_position(epoch).express(frame)

    def get_position_matrix(self, epoch, frame):
        """Returns matrix instead of Vector to be used w/ Plotter"""
        return self.get_position(epoch).to_matrix(frame)

    def get_direction_matrix(self, other, epoch, frame):
        # print("get dir:")
        # print(self)
        se = self.get_position_matrix(epoch, frame)
        # print(other)
        ot = other.get_position_matrix(epoch, frame)
        direction = ot - se
        return direction

    def get_period(self):
        T = 2 * pi * (self.radius ** 3.0/self.mu) ** .5
        return T


class EllipticalOrbit3D(Orbit):
    """Model of a ideal 3D elliptical orbit"""

    def __init__(self, parentFrame, center = None,
                 eccentricity: float = 0, semiMajorAxis: float = 0,
                 inclination: float = 0, ascNode: float = 0,
                 periArg: float = 0, trueAnomaly: float = 0,
                 color = (0, 0, 0), opt = 'sun'):
        super().__init__(parentFrame, center, color)
        self.eccentricity = eccentricity
        self.semiMajorAxis = semiMajorAxis
        self.inclination = inclination
        self.ascNode = ascNode
        self.periArg = periArg
        self.trueAnomaly = trueAnomaly
        self.frame = parentFrame.orientnew(
                'frame', 'Space', (inclination, 0, ascNode), 123)
        # todo: orient new frame with 'Space'
        # todo: fix frame naming scheme
        self.dim = 3
        if opt == 'sun':
            self.mu = 1.327e20
        elif opt == 'earth':
            self.mu = 3.986004418e14
        self.period = self.get_period()

    def get_position(self, epoch, frame = None):
        '''given an epoch, returns a sympy vector for position'''
        # todo pass other frame argument
        e = self.eccentricity
        a = self.semiMajorAxis
        i = self.inclination
        Om = self.ascNode
        w = self.periArg
        f = self.trueAnomaly
        if frame is None:
            frame = self.frame

        r = a * (1.0 - e ** 2.0) / (1 + e * cos(2 * pi * epoch / self.period))
        x = r * cos(2 * pi * epoch / self.period + self.periArg) * frame.x
        y = r * sin(2 * pi * epoch / self.period + self.periArg) * frame.y
        z = 0 * frame.z
        if self.center is None:
            return x + y + z
        else:
            return x + y + z + self.center.get_position(epoch).express(frame)

    def get_position_matrix(self, epoch, frame):
        """Returns matrix instead of Vector to be used w/ Plotter"""
        return self.get_position(epoch).to_matrix(frame)

    def get_period(self):
        T = 2 * pi * (self.semiMajorAxis ** 3.0/self.mu) ** .5
        return T


if __name__ == '__main__':
    # testing the orbit and plotter classes
    N = ReferenceFrame('N')
    t = linspace(0, 10 * 24 * 3600, 5000)  # numpy array

    # creates orbits. Two objects orbiting a main body
    earth_orbit = CircularOrbit3D(N, radius = 1.5e11, color = (0, .6, .20))
    sat1_orbit = EllipticalOrbit3D(N, center = earth_orbit, semiMajorAxis = 1e9,
                                   eccentricity = .9, color = (1, 0, 0), opt = 'earth')
    #sat1_orbit = EllipticalOrbit3D(N, center = None, semiMajorAxis = 1e9,
    #                               eccentricity = .9, periArg = 0, opt = 'earth')
    sat2_orbit = EllipticalOrbit3D(N, center = earth_orbit, semiMajorAxis = 1e9,
                                   eccentricity = .9, periArg = (120 / 180) * pi,
                                   color = (0, 1, 0), opt = 'earth')
    sat3_orbit = EllipticalOrbit3D(N, center = earth_orbit, semiMajorAxis = 1e9,
                                   eccentricity = .9, periArg = (240 / 180) * pi,
                                   inclination = 15*(pi/180),
                                   color = (0, 0, 1), opt = 'sun')
    orbits = [earth_orbit, sat1_orbit, sat2_orbit, sat3_orbit]#, sat2_orbit, sat3_orbit]

    for obt in orbits:
        Plotter.plot_trajectory(obt.get_trajectory(t, frame = N), color = obt.color,
                                tube_radius = None)

    Plotter.show3d()  # calls matplotlib show