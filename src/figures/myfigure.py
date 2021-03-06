from figures.utils import get_images_dir

from matplotlib.figure import Figure
from matplotlib import pyplot as plt, colors, cm, rc, rcParams
import numpy as np

import os

PLOT_SCALES = [
    'linear',
    'semilogx',
    'semilogy',
    'loglog',
]

LEGEND_LOCATION_STRINGS = [
    'best',
    'upper right',
    'upper left',
    'lower left',
    'lower right',
    'right',
    'center left',
    'center right',
    'lower center',
    'upper center',
    'center',
]

LEVELS_SCALES = [
    'linear',
    'log2',
    'log',
    'log10',
]

class MyFigure(Figure):
    ''' customize figure with one axes.
    '''

    def __init__(self, dir_path=None, file_name='foo', file_type='png', *args, **kwargs):

        # set figure size
        if kwargs['figsize'] is None:
            kwargs['figsize'] = (8, 6)

        super().__init__(*args, **kwargs)

        # file path attributes
        self.file_name = file_name
        self.file_type = file_type
        self.dir_path = dir_path

        # add set of subplots
        self.ax = self.subplots()

        # import rcParams by importing style sheet
        style_sheet_path = os.path.join(
            get_images_dir(),
            'article.mplstyle'
        )
        plt.style.use(style_sheet_path)

        # get legend default location 
        self.legend_loc = rcParams['legend.loc']
        self.show_legend = True

        # default plot type
        self.plot_scale = 'linear'

        # colormap
        self.colormap = None

        # levels
        self.levels_scale = 'linear'
        self.levels_decimals = None

        # x and y lim changed flag
        self.xlim_changed = False
        self.ylim_changed = False


    @property
    def file_path(self):
        if self.dir_path is not None:
            return os.path.join(self.dir_path, self.file_name + '.' + self.file_type)
        else:
            return None

    def set_font_sizes(self):
        #TODO! revise how **kwargs works

        SMALL_SIZE = 10
        MEDIUM_SIZE = 20
        BIGGER_SIZE = 18

        rc('font', size=SMALL_SIZE)
        rc('axes', titlesize=SMALL_SIZE)
        rc('axes', labelsize=MEDIUM_SIZE)
        rc('xtick', labelsize=SMALL_SIZE)
        rc('ytick', labelsize=SMALL_SIZE)
        rc('legend', fontsize=SMALL_SIZE)
        rc('figure', titlesize=BIGGER_SIZE)

    def set_title(self, title):
        self.ax.set_title(title)

    def set_xlabel(self, label):
        self.ax.set_xlabel(label)

    def set_ylabel(self, label):
        self.ax.set_ylabel(label)

    def set_xlim(self, xmin, xmax):
        self.ax.set_xlim(xmin, xmax)
        self.xlim_changed = True

    def set_ylim(self, ymin, ymax):
        self.ax.set_ylim(ymin, ymax)
        self.ylim_changed = True

    def set_zlim(self, zmin, zmax):
        self.ax.set_zlim(zmin, zmax)

    def set_legend_location(self, loc):
        assert loc in LEGEND_LOCATION_STRINGS, ''
        self.legend_loc = loc

    def turn_legend_off(self):
        self.show_legend = False

    def set_plot_scale(self, plot_scale):
        assert plot_scale in PLOT_SCALES, ''
        self.plot_scale = plot_scale

    def plot(self, x, y,  labels=None, colors=None, linestyles=None, markers=None):
        assert x.ndim == 1, ''
        assert y.ndim in [1, 2], ''

        # expand dimension of y if just one array is given
        if y.ndim == 1:
            assert x.shape[0] == y.shape[0], ''
            y = np.expand_dims(y, axis=0)
        else:
            assert x.shape[0] == y.shape[1], ''

        # number of lines to plot
        n_lines = y.shape[0]

        # labels
        if labels is not None and type(labels) == str:
            assert n_lines == 1, ''
            labels = [labels]
        elif labels is not None and type(labels) == list:
            assert n_lines == len(labels), ''
        else:
            labels = [None for i in range(n_lines)]

        # colors
        if colors is not None and type(colors) == str:
            assert n_lines == 1, ''
            colors = [colors]
        elif colors is not None and type(colors) == list:
            assert n_lines == len(colors), ''
        else:
            colors = [None for i in range(n_lines)]

        # linestyles
        if linestyles is not None and type(linestyles) == str:
            assert n_lines == 1, ''
            linestyle = [linestyles]
        elif linestyles is not None and type(linestyles) == list:
            assert n_lines == len(linestyles), ''
        else:
            linestyles = ['-' for i in range(n_lines)]

        # markers
        if markers is not None and type(markers) == str:
            assert n_lines == 1, ''
            markers = [markers]
        elif markers is not None and type(markers) == list:
            assert n_lines == len(markers), ''
        else:
            markers = [None for i in range(n_lines)]

        # plot lines
        for i in range(n_lines):
            if self.plot_scale == 'linear':
                self.ax.plot(x, y[i], color=colors[i], linestyle=linestyles[i],
                             label=labels[i], marker=markers[i])
            elif self.plot_scale == 'semilogx':
                self.ax.semilogx(x, y[i], color=colors[i], linestyle=linestyles[i],
                                 label=labels[i], marker=markers[i])
            elif self.plot_scale == 'semilogy':
                self.ax.semilogy(x, y[i], color=colors[i], linestyle=linestyles[i],
                                 label=labels[i], marker=markers[i])
            elif self.plot_scale == 'loglog':
                self.ax.loglog(x, y[i], color=colors[i], linestyle=linestyles[i],
                               label=labels[i], marker=markers[i])

        # legend
        if self.show_legend and any(label is not None for label in labels):
            self.ax.legend(loc=self.legend_loc)

        # set ylim if xlim has been changed
        if self.xlim_changed and not self.ylim_changed:

            # get x bounds
            xmin, xmax = self.ax.get_xbound()

            # get indices of the interval [xmin, xmax]
            idx_xmin = np.argmin(np.abs(x - xmin))
            idx_xmax = np.argmin(np.abs(x - xmax))
            idx_x = slice(idx_xmin, idx_xmax + 1)

            ymin = ymax = 0

            # get max and min of y_i in the interval
            for i in range(n_lines):
                if ymin > np.min(y[i][idx_x]):
                    ymin = np.min(y[i][idx_x])
                if ymax < np.max(y[i][idx_x]):
                    ymax = np.max(y[i][idx_x])

            self.set_ylim(ymin, ymax)

        # save figure
        if self.file_path is not None:
            self.savefig(self.file_path)

    def set_colormap(self, colormap, start=0, stop=1, num=100):
        assert 0 <= start <= stop <= 1, ''
        colormap = cm.get_cmap(colormap, 100)
        self.colormap = colors.ListedColormap(
            colormap(np.linspace(start, stop, num))
        )

    def set_contour_levels_scale(self, scale):
        assert scale in LEVELS_SCALES, ''
        self.levels_scale = scale

    def set_contour_levels_decimals(self, decimals):
        assert type(decimals) == int, ''
        self.levels_decimals = decimals

    def get_contour_levels(self, n_levels=10):
        if self.levels_scale == 'linear':
            levels = np.linspace(self.vmin, self.vmax, n_levels + 1)
        elif self.levels_scale == 'log2':
            levels = np.logspace(-1, np.log2(self.vmax), n_levels + 1, base=2)
        elif self.levels_scale == 'log':
            levels = np.logspace(-1, np.log(self.vmax), n_levels + 1, base=np.e)
        elif self.levels_scale == 'log10':
            levels = np.logspace(-1, np.log10(self.vmax), n_levels + 1, base=10)
        else:
            levels = None

        # round levels to 1 decimal
        if self.levels_decimals is not None:
            levels = np.around(levels, self.levels_decimals)

        return levels

    def reduce_arrays_xy_axis(self, X, Y, Z=None, U=None, V=None):
        '''
        '''
        # check if height Z or vector field U, V is given 
        if Z is None:
            assert U is not None and V is not None, ''
        else:
            assert U is None and V is None, ''

        # if xlim is given
        if self.xlim_changed:

            # get x axis
            x = X[:, 0]

            # get x bounds
            xmin, xmax = self.ax.get_xbound()

            # get indices of the given limits
            idx_xmin = np.argmin(np.abs(x - xmin))
            idx_xmax = np.argmin(np.abs(x - xmax))
            idx_x = slice(idx_xmin, idx_xmax + 1)

        else:
            idx_x = slice(None)

        # if ylim is given
        if self.ylim_changed:

            # get y axis
            y = Y[0, :]

            # get y bounds
            ymin, ymax = self.ax.get_ybound()

            # get indices of the given limits
            idx_ymin = np.argmin(np.abs(y - ymin))
            idx_ymax = np.argmin(np.abs(y - ymax))
            idx_y = slice(idx_ymin, idx_ymax + 1)

        else:
            idx_y = slice(None)

        # reduce coordinates
        X = X[idx_x, idx_y]
        Y = Y[idx_x, idx_y]

        # reduce height
        if Z is not None:
            Z = Z[idx_x, idx_y]
            return X, Y, Z

        # reduce U and V
        if U is not None and V is not None:
            U = U[idx_x, idx_y]
            V = V[idx_x, idx_y]
            return X, Y, U, V

    def contour(self, X, Y, Z, vmin=None, vmax=None, levels=None):
        '''
        '''
        assert X.ndim == Y.ndim == Z.ndim == 2, ''
        assert Z.shape == X.shape == Y.shape, ''

        # reduce arrays according to the x and y limits if changed
        if self.xlim_changed or self.ylim_changed:
            X, Y, Z = self.reduce_arrays_xy_axis(X, Y, Z=Z)

        # set colormap if is not set yet
        if self.colormap is None:
            self.set_colormap('coolwarm')

        # get minimum and maximum height values
        if vmin is not None:
            self.vmin = vmin
        else:
            self.vmin = Z.min()
        if vmax is not None:
            self.max = vmax
        else:
            self.vmax = Z.max()

        # get levels
        levels = self.get_contour_levels()

        # contour f
        cs = self.ax.contourf(
            X,
            Y,
            Z,
            vmin=self.vmin,
            vmax=self.vmax,
            levels=levels,
            cmap=self.colormap,
            extend='both',
            #norm=colors.LogNorm(self.zmin, self.zmax),
        )
        #TODO! test LogNorm possibility

        # colorbar
        cbar = self.colorbar(cs)

        # save figure
        if self.file_path is not None:
            self.savefig(self.file_path)

    def coarse_quiver_arrows(self, X, Y, U, V, kx, ky):
        # show every kx row and ky column
        X = X[::kx, ::ky]
        Y = Y[::kx, ::ky]
        U = U[::kx, ::ky]
        V = V[::kx, ::ky]
        return X, Y, U, V

    def vector_field(self, X, Y, U, V, kx=None, ky=None, scale=None, width=0.005):
        '''
        '''
        assert X.ndim == Y.ndim == U.ndim == V.ndim == 2, ''
        assert X.shape == Y.shape == U.shape == V.shape, ''

        # reduce arrays according to the x and y limits if changed
        if self.xlim_changed or self.ylim_changed:
            X, Y, U, V = self.reduce_arrays_xy_axis(X, Y, U=U, V=V)

        # coarse arrays
        l = 25
        if kx is None and X.shape[0] >= l:
            kx = X.shape[0] // 25
        elif kx is None and X.shape[0] < l:
            kx = 1

        if ky is None and Y.shape[1] >= l:
            ky = Y.shape[1] // 25
        elif ky is None and Y.shape[1] < l:
            ky = 1

        X, Y, U, V = self.coarse_quiver_arrows(X, Y, U, V, kx, ky)

        # set colormap if is not set yet
        if self.colormap is None:
            self.set_colormap('viridis_r', 0.20, 0.95, 75)

        # initialize norm object and make rgba array
        C = np.sqrt(U**2 + V**2)
        norm = colors.Normalize(vmin=np.min(C), vmax=np.max(C))
        sm = cm.ScalarMappable(cmap=self.colormap, norm=norm)

        # quiver
        quiv = self.ax.quiver(
            X,
            Y,
            U,
            V,
            C,
            cmap=self.colormap,
            angles='xy',
            scale_units='xy',
            scale=scale,
            width=width,
        )

        # colorbar
        self.colorbar(sm)

        # save figure
        if self.file_path is not None:
            self.savefig(self.file_path)
