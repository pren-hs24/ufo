# Utility base class for Pylons. It is supposed to make
# the code more understandable, well organized and easier to
# adapt in case something changes. In this case it stores the
# information of the Pylon in the image to make it more
# accessable in calculations.

class Pylon:

    REAL_HEIGHT: int = 100 # TODO: real height of Pylons messured in mm
    PYLON_COUNTER: int = 1 # unique id for each detected pylon

    xmin: int
    ymin: int
    xmax: int
    ymax: int
    id: int

    # [Constructor] with the values for physical nodes
    # - start     = (RealNode) one of the two connected nodes
    # - end       = (RealNode) second of the two connected nodes
    # (edges are treated als bidirectional)
    # - status    = (EdgeState) reflects the current amount
    #               of knowledge we have of this edge
    def __init__(self, xmin: int, ymin: int, xmax: int, ymax: int):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.id = Pylon.PYLON_COUNTER
        
        Pylon.PYLON_COUNTER += 1
    
    def __str__(self) -> str:
        return f"Pylon Image: {self.id} [({self.xmin},{self.ymin}), "\
            + f"({self.xmax},{self.ymax})]"
    
    def __eq__(self, value) -> bool:
        if not isinstance(value, Pylon):
            return False
        
        return self.xmin == value.xmin and self.ymin == value.ymin and\
                self.xmax == value.xmax and self.ymax == value.ymax

    def get_xmin(self) -> int:
        return self.xmin
    
    def get_ymin(self) -> int:
        return self.ymin
    
    def get_xmax(self) -> int:
        return self.xmax
    
    def get_ymax(self) -> int:
        return self.ymax
    
    def get_id(self) -> str:
        return f"P{str(self.id)}"
        
    def get_width(self) -> int:
        return self.xmax - self.xmin
    
    def get_height(self) -> int:
        return self.ymax - self.ymin
    
    @classmethod
    def get_real_height(cls) -> int:
        return Pylon.REAL_HEIGHT