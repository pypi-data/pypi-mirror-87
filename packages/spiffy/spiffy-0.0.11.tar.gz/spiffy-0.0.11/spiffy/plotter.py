import mayavi.mlab as mlab
import numpy as np
import matplotlib.pyplot as mtplt

class Plotter:
    """Class to gather plotting functionalities.
    Interfaces with mayavi functions"""
    def __init__(self):
        pass

    @staticmethod
    def plot_trajectory(trajectory, **kwargs):
        """Plots curve from trajectory (3d x time numpy array).
        Returns plot3d object"""
        plot = mlab.plot3d(trajectory[0, :], trajectory[1, :], trajectory[2, :],
                      **kwargs)
        return plot

    @staticmethod
    def plot_trajectory2d(trajectory, **kwargs):
        """Plots curve from trajectory (2d x time numpy array).
        Returns plot2d object"""
        plot = mtplt.plot(trajectory[0, :], trajectory[1, :])
        return plot

    @staticmethod
    def plot_separation(pos1, pos2, **kwargs):
        """Plots straight line between 2 points"""
        # todo: better way of dealing with np.arrays needed by mayavi
        plot = mlab.plot3d([np.double(pos1[0]), np.double(pos2[0])],
                      [np.double(pos1[1]), np.double(pos2[1])],
                      [np.double(pos1[2]), np.double(pos2[2])],
                      **kwargs)
        return plot

    @staticmethod
    def plot_vector(pos, direction, **kwargs):
        """Plots arrow at pos, pointing w/ direction"""

        # todo: guarantee normalized dir? and/or produce dir from 2 positions
        plot = mlab.quiver3d([np.double(pos[0])],
                        [np.double(pos[1])],
                        [np.double(pos[2])],
                        [np.double(direction[0])],
                        [np.double(direction[1])],
                        [np.double(direction[2])],
                        **kwargs)
        return plot

    @staticmethod
    def plot_point(pos, **kwargs):
        """PLots ball to represent body"""

        # todo: special visualization cases for Sun and planets?
        plot = mlab.points3d(np.double(pos[0]),
                        np.double(pos[1]),
                        np.double(pos[2]),
                        **kwargs)
        return plot

    @staticmethod
    def plot_surface(points, **kwargs):
        """Plots surface from points (3d numpy array).
        Returns plot3d object"""
        plot = mlab.contour3d(points[0], points[1], points[2])
        return plot

    @staticmethod
    def show3d():
        return mlab.show()

    @staticmethod
    def show2d():
        mtplt.axes().set_aspect('equal', 'datalim')
        return mtplt.show()
