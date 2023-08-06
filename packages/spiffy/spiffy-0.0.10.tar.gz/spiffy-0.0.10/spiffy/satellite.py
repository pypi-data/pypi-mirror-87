from sympy.physics.mechanics import Particle
from sympy import Symbol

class Satellite(Particle):

    def __init__(self, symbol, point, mass):
            Particle.__init__(symbol, point, mass)
