from matplotlib.artist import Artist
from igraph import BoundingBox, Graph, palettes

class GraphArtist(Artist):
    """Matplotlib artist class that draws igraph graphs.
    Only Cairo-based backends are supported.
    """

    def __init__(self, graph, figsize, palette=None, *args, **kwds):
        """Constructs a graph artist that draws the given graph within
        the given bounding box.

        `graph` must be an instance of `igraph.Graph`.
        `bbox` must either be an instance of `igraph.drawing.BoundingBox`
        or a 4-tuple (`left`, `top`, `width`, `height`). The tuple
        will be passed on to the constructor of `BoundingBox`.
        `palette` is an igraph palette that is used to transform
        numeric color IDs to RGB values. If `None`, a default grayscale
        palette is used from igraph.

        All the remaining positional and keyword arguments are passed
        on intact to `igraph.Graph.__plot__`.
        """
        Artist.__init__(self)

        if not isinstance(graph, Graph):
            raise TypeError("expected igraph.Graph, got %r" % type(graph))

        self.graph = graph
        self.palette = palette or palettes["gray"]
        self.figsize = figsize
        self.args = args
        self.kwds = kwds

    def draw(self, renderer):
        from matplotlib.backends.backend_cairo import RendererCairo
        if not isinstance(renderer, RendererCairo):
            raise TypeError("graph plotting is supported only on Cairo backends")
            
        self.graph.__plot__(renderer.gc.ctx, BoundingBox(60 * self.figsize[0] // 6, 60 * self.figsize[1] // 8, 600 * self.figsize[0] // 12, 600 * self.figsize[1] // 12 ), self.palette, *self.args, **self.kwds)