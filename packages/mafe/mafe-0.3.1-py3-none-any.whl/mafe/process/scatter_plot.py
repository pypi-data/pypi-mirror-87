__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

# flake8: noqa: F401

from os import environ
from typing import List

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d import Axes3D  # pylint: disable=unused-import
import pandas as pd


class ScatterPlot:

    MARKERS = ['x', 'o', '^', 'v', '.', '<', '1', '2', '3', '4']

    def __init__(self, marker_column: str, xyz_columns: List[str], image_file: str) -> None:
        self._marker_column = marker_column
        self._xyz_columns = xyz_columns
        self._image_file = image_file
        self._set_matplotlib_backend()
        self._axis = self._setup_3d_plot()

    def plot_data_point(self, row: pd.Series) -> None:
        marker = self.MARKERS[int(row[self._marker_column]) % 10]
        x_s, y_s, z_s = row[self._xyz_columns]
        self._axis.scatter(
            x_s, y_s, z_s, marker=marker,
            c=list(mcolors.TABLEAU_COLORS.keys())[int(row[self._marker_column]) % 10]
        )

    def show_or_save(self) -> None:
        if self._image_file is None:
            plt.show()
        else:
            plt.savefig(self._image_file, bbox_inches='tight')

    def _set_matplotlib_backend(self) -> None:
        if environ.get('DISPLAY'):
            matplotlib.use('qt5agg')
        else:
            if not self._image_file:
                raise ValueError('image_file must be set when running headless')
            matplotlib.use('Agg')

    @staticmethod
    def _setup_3d_plot() -> plt.axis:
        fig = plt.figure()
        axis = fig.add_subplot(111, projection='3d')
        axis.set_xlabel('0')
        axis.set_ylabel('1')
        axis.set_zlabel('2')
        return axis
