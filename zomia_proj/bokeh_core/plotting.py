import numpy as np
from bokeh.io import show
from bokeh.plotting import figure, curdoc
from bokeh.models import GraphRenderer, Circle, StaticLayoutProvider, LayoutProvider
from bokeh.palettes import Spectral8
from tree import get_tree

from typing import Type, Callable


class EdgeFactory:
    """
        Builds constructor kwargs for default edge_renderer
    """
    def __init__(self, indices, edge_gen_func: Callable[[int], list[int]]):
        self.nodes = indices
        self.edge_gens = [edge_gen_func(ind) for ind in indices]

    @property
    def edges(self):
        edges_kwargs_constructor = {'start': [], 'end': []}
        for cursor, index in enumerate(self.nodes):
            edge_gen = self.edge_gens[cursor]
            edges_kwargs_constructor['start'].extend([index] * len(edge_gen))
            edges_kwargs_constructor['end'].extend(edge_gen)
        return edges_kwargs_constructor


class GraphFactory:
    """
        Graph DI.\n
        Sets nodes, edges, tree
    """
    _layout_class = StaticLayoutProvider

    def __init__(self):
        self.coords = None
        self.indices = None
        self._graph = GraphRenderer()
        self._graph.node_renderer.glyph = Circle(radius=10, fill_color='#abdda4')
        self._tree = {}

    @property
    def graph(self) -> GraphRenderer:
        """
        Applies all the renderer attributes and returns built graph-renderer
        :return:
        """
        self.indices = self.export_indices(self._tree)
        self.coords = self.export_coords(self._tree)
        self._graph.node_renderer.data_source.data = dict(
            index=self.indices,
            fill_color=Spectral8
        )
        edge_factory = EdgeFactory(self.indices, lambda ind: self.export_edges(ind, self._tree))
        self._graph.edge_renderer.data_source.data = dict(
            **edge_factory.edges
        )
        self._graph.layout_provider = self._build_layout_provider()
        return self._graph

    @property
    def tree(self):
        return self._tree

    @tree.setter
    def tree(self, tree: dict):
        """
        :param tree: 1: {
            'link_to': [2, 3, 4],
            'pos': (130, 25)
        },
        :return:
        """
        self._tree = tree

    @staticmethod
    def export_indices(tree) -> tuple[int]:
        return tuple(tree.keys())

    @staticmethod
    def export_edges(index, tree):
        return tree[index]['link_to']

    @staticmethod
    def export_coords(tree) -> np.array:
        coords = np.array([i['pos'] for i in tree.values()], np.ulonglong)
        return coords

    def _build_layout_provider(self) -> LayoutProvider:
        """
        :return:
        """
        graph_layout_provider = self._layout_class(
            graph_layout=dict(zip(self.indices, self.coords))
        )
        return graph_layout_provider

    @classmethod
    def set_layout_class(cls, layout_class: Type):
        cls._layout_class = layout_class


class PlotContainer:

    def __init__(self, size_x: int, size_y: int):
        self._plot = figure(x_range=(0, size_x), y_range=(0, size_y))
        self._renderers = []

    @property
    def plot(self):
        return self._plot

    def add_renderer(self, renderer):
        self.plot.renderers.append(renderer)

    def show_plot(self):
        show(self.plot)


plot_di = PlotContainer(1080, 720)
graph_factory = GraphFactory()
graph_factory.tree = get_tree()
plot_di.add_renderer(graph_factory.graph)
plot_di.show_plot()

curdoc().add_root(plot_di.plot)
