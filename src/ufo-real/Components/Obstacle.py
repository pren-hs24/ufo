# Utility base class for images of Obstacles. It is supposed
# to make the code more understandable and allow the image
# recognition to same all the objects it recorded.

class Obstacle:

    LENGTH = 70 # length of the obstacle in mm
    DEPTH = 20 # depth of the obstacle in mm
    HEIGHT = 50 # hight of the obstacle in mm
    COUNTER: int = 1 # unique id for all obstacles

    x_min: int # upper left corner x value in px
    y_min: int # upper left corner y value in px
    x_max: int # lower right corner x value in px
    y_max: int # lower right corner y value in px
    id: int # unique id in order to compare and identify
    
    # [Constructor] with the values for the visual corners
    # of the image of the obstacle
    # x_min = (int) # upper left corner x value in px
    # y_min = (int) # upper left corner y value in px
    # x_max = (int) # lower right corner x value in px
    # y_max = (int) # lower right corner y value in px
    def __init__(self, x_min: int, y_min: int, x_max: int, y_max: int):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.id = self.COUNTER

        self.COUNTER += 1
    
    def __str__(self) -> str:
        return f"Obstacle {self.id}: ({self.x_min},{self.y_min}),({self.x_max},{self.y_max})"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Obstacle):
            return self.x_min == other.x_min and self.y_min == other.y_min\
                and self.x_max == other.x_max and self.y_max == other.y_max
        elif isinstance(other, str):
            return str(self.id) == other
        elif isinstance(other, int):
            return self.id == other
        else:
            raise ValueError("Incompatible type for comparison.")
     
    def get_upper_left(self) -> tuple[int, int]:
        return (self.x_min, self.y_min)
    
    def get_lower_right(self) -> tuple[int, int]:
        return (self.x_max, self.y_max)
    
    def get_id(self) -> str:
        return str(self.id)
    
    def get_length() -> int:
        return Obstacle.LENGTH
    
    def get_depth() -> int:
        return Obstacle.DEPTH
    
    def get_height() -> int:
        return Obstacle.HEIGHT