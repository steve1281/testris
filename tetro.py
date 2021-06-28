# one-sided tetrominoes - the ones tetris uses
class Tetro:
    """ simple class to store tetrominoes attributes
    @todo: needs to be a dataclass
    """

    def __init__(self, tetro, shape, color):
        self.tetro = tetro
        self.shape = shape
        self.color = color
