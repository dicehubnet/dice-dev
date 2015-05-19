"""
Visualization
=============
"""

# External modules
# ================
from bokeh.plotting import *
from PyQt5.QtCore import pyqtProperty, pyqtSlot, pyqtSignal
from bokeh.models.renderers import GlyphRenderer


class Visualization:

    def __init__(self):

        self.p1 = None
        self.__plot_html_path = ""
        self.page_name = 'index.html'
        self.__reload_web_engine = False

        self.x1 = [0]
        self.y1 = [0]

        self.default_plot_width = 500
        self.default_plot_height = 500

    def visualization_load(self):

        self.__plot_html_path = self.config_path(self.page_name)
        output_file(self.__plot_html_path)

        self.p1 = figure(plot_width=self.default_plot_width,
                         plot_height=self.default_plot_height,
                         tools="pan,wheel_zoom,box_zoom,reset,resize,previewsave")
        self.p1.scatter(self.x1, self.y1, size=12, color="red", alpha=0.5)
        self.p1.toolbar_location = None
        save(self.p1)

    # HTML Path
    # =========
    plot_html_path_changed = pyqtSignal(name="plotHTMLPathChanged")

    @property
    def plot_html_path(self):
        return self.__plot_html_path

    @plot_html_path.setter
    def plot_html_path(self, plot_html_path):
        if self.__plot_html_path != plot_html_path:
            self.__plot_html_path = plot_html_path
            self.plot_html_path_changed.emit()

    plotHTMLPath = pyqtProperty(str, fget=plot_html_path.fget, fset=plot_html_path.fset, notify=plot_html_path_changed)

    # Figure Size
    # ===========
    def change_plot_size(self, width, height):
        self.p1.plot_height = width
        self.p1.plot_width = height
        self.reload_plot()

    @pyqtSlot(int, name="setPlotWidth")
    def set_plot_width(self, width):
        self.p1.plot_width = width
        self.reload_plot()

    @pyqtSlot(int, name="setPlotHeight")
    def set_plot_heighth(self, height):
        self.p1.plot_height = height
        self.reload_plot()

    # Reload plot
    # ===========
    @pyqtSlot(name="reload")
    def reload_plot(self):
        self.reload_web_engine = False
        save(self.p1)
        # self.plot_html_path = self.config_path(self.page_name)
        self.reload_web_engine = True

    reload_web_engine_changed = pyqtSignal(name="reloadWebEngineChanged")

    @property
    def reload_web_engine(self):
        return self.__reload_web_engine

    @reload_web_engine.setter
    def reload_web_engine(self, reload_web_engine):
        if self.__reload_web_engine != reload_web_engine:
            self.__reload_web_engine = reload_web_engine
            self.reload_web_engine_changed.emit()

    reloadWebEngine = pyqtProperty(bool, fget=reload_web_engine.fget, fset=reload_web_engine.fset, notify=reload_web_engine_changed)

    # Load data and reload plot
    # =========================
    def load_data(self, x1, y1):
        my_renderer = self.p1.select(dict(type=GlyphRenderer))
        data_src = my_renderer[0].data_source

        self.x1 = x1
        self.y1 = y1

        data_src.data["x"] = x1
        data_src.data["y"] = y1
        data_src._dirty = True

        self.reload_plot()