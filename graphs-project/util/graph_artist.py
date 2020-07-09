from matplotlib.artist import Artist
from igraph import BoundingBox, Graph, palettes

class GraphArtist(Artist):
    """Artist to render the graph
    """
    def __init__(self, graph, figsize, dpi, palette=None, *args, **kwds):
        Artist.__init__(self)

        if not isinstance(graph, Graph):
            raise TypeError("expected igraph.Graph, got %r" % type(graph))

        self.graph = graph
        self.palette = palette or palettes["gray"]
        self.figsize = figsize
        self.dpi = dpi
        self.args = args
        self.kwds = kwds

    def draw(self, renderer):
        from matplotlib.backends.backend_cairo import RendererCairo
        
        # if not isinstance(renderer, RendererCairo):
        #     raise TypeError("graph plotting is supported only on Cairo backends")
        
        width = (self.figsize.width - 1) * self.dpi 
        height = (self.figsize.height - 1) * self.dpi
        
        x = self.figsize.x0 * self.dpi
        
        # TODO improve place of plot
        left = 1.4109875916077667e+002 * x ** 0 + -2.1491832476305572e+000 * x ** 1 +  1.2437197021687572e-002 * x ** 2 + -1.9415941246427828e-005 * x ** 3 +  1.0520878448135259e-008 * x ** 4

        self.graph.__plot__(renderer.gc.ctx, BoundingBox(left, self.figsize.y0 * self.dpi, width + left, height), self.palette, *self.args, **self.kwds)