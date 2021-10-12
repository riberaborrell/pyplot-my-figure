from figures.myfigure import MyFigure
import matplotlib.pyplot as plt

import numpy as np
from pathlib import Path
import os
import pytest

SOURCE_PATH = Path(os.path.dirname(__file__))
PROJECT_PATH = SOURCE_PATH.parent
DATA_PATH = os.path.join(PROJECT_PATH, 'data')

class TestContour:
    '''
    '''
    @pytest.fixture
    def dir_path(self):
        ''' returns dir path for the test plots
        '''
        dir_path = os.path.join(DATA_PATH, 'tests')
        return dir_path

    @pytest.fixture
    def mesh(self):
        ''' returns tuple (X, Y)
        '''
        h = 0.1
        lb = 0
        rb = 10
        x = y = np.arange(lb, rb + h, h)
        return np.meshgrid(x, y, indexing='ij')

    @pytest.fixture
    def f(self, mesh):
        ''' returns function f evaluated at the grid
        '''
        X, Y = mesh
        return X * Y

    #@pytest.mark.skip(reason='')
    def test_contour(self, dir_path, mesh, f):
        ''' plot z = x*y
        '''
        fig = plt.figure(
            FigureClass=MyFigure,
            dir_path=dir_path,
            file_name='contour',
        )
        X, Y = mesh
        fig.contour(X, Y, f)

    def test_contour_limits(self, dir_path, mesh, f):
        ''' plot z = x*y
        '''
        fig = plt.figure(
            FigureClass=MyFigure,
            dir_path=dir_path,
            file_name='contour_limits',
        )
        X, Y = mesh
        fig.set_xlim(0, 0.5)
        fig.set_ylim(0, 0.5)
        fig.contour(X, Y, f)

    def test_contour_levels(self, dir_path, mesh, f):
        ''' plot z = x*y
        '''
        fig = plt.figure(
            FigureClass=MyFigure,
            dir_path=dir_path,
            file_name='contour_levels',
        )
        X, Y = mesh
        fig.contour(X, Y, f)