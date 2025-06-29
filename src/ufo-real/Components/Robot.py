# Utility base class for Nodes in order to make the code
# more understandable, better structured and easier to
# adapt and fix

from math import atan2, degrees, sqrt

class Robot:

    posX: int
    posY: int
    angle: float

    # [Constructor] with all the values for the robot
    # - posX      = (int) horizontal position of the robot in mm
    # - posY      = (int) vertical position of the robot in mm
    # (center (0,0) is left upper corner) 
    # - angle     = (int) degree in which direction the camera is facing
    #               (0° to the right - East, 90° straight down - South,
    #               180° to the left - Weast, 270° straight up - North)
    def __init__(self, posX: int, posY: int, angle: float):
        self.posX = posX
        self.posY = posY
        self.angle = angle

    def __str__(self) -> str:
        return f"Robot:\n"\
            +f"------\n"\
            +f"- Position:\t({self.posX}mm,{self.posY}mm)\n"\
            +f"- Direction:\t{self.angle}°"
    
    def __eq__(self, value) -> bool:
        if isinstance(value, Robot):
            return self.posX == value.posX and\
                self.posY == value.posY and\
                self.angle == value.angle
        else:
            return False

    def get_posX(self) -> int:
        return self.posX
    
    def __set_posX(self, newPosX: int) -> None:
        self.posX = newPosX
    
    def get_posY(self) -> int:
        return self.posY
    
    def __set_posY(self, newPosY: int) -> None:
        self.posY = newPosY
    
    def get_direction(self) -> float:
        return self.angle
    
    def __setDirection(self, newAngle: float) -> None:
        self.angle = newAngle

    def change_position(self, coordinates: tuple[int, int]) -> None:
        self.__set_posX(coordinates[0])
        self.__set_posY(coordinates[1])

    def turnBy(self, turn_angle: float) -> None:
        """
        Change the direction in which the robot is facing by\n
        ``turn_angle`` amount of degrees. Should be of type ``float``.
        """
        self.__setDirection(self.get_direction() + turn_angle % 360.0)

    def turnTowards(self, coordinates: tuple[int, int]) -> None:
        """
        Set the robot's direction by inputting the new\n
        ``coordinates`` it should be facing.
        """
        self.__setDirection(self._compute_angle(coordinates))

    # Helper function to determine the distance and angle of
    # a point on the plane in comparison to the robot
    # - x       = (int) mm horizontel coordinate of the point
    # - y       = (int) mm vertical coordinate of the point
    # (The center (0,0) is the upper-left corner of the map,
    # going down or right from there increases the value)
    # - return  = (dDeg, dDis)
    # - dDeg    = (int) amount of ° to turn in order to be
    #             aligned between -180 and 180
    # - dDis    = (float) distance in mm towards the point
    def compute_distance_and_difference(self, coordinates: tuple[int, int]) -> tuple[float, float]:
        """
        It computes the distance between the robot and the point\n
        with the given ``coordinates``, as well as the difference\n
        between the direction in which the robot is facing and\n
        the angle at which the point can be found.
        """
        # calculate difference in angles
        dDeg = (self._compute_angle(coordinates) - self.get_direction() + 180.0) % 360 - 180.0

        # calculate distance
        dDis = self._compute_distance(coordinates)
        
        return (dDeg, dDis)

    def _compute_angle(self, coordinates: tuple[int, int]) -> float:
        dx, dy = self._compute_deltas(coordinates)
        return degrees(atan2(dy, dx))
    
    def _compute_distance(self, coordinates: tuple[int, int]) -> float:
        dx, dy = self._compute_deltas(coordinates)
        return sqrt(dx**2 + dy**2)
    
    def _compute_deltas(self, coordinates: tuple[int, int]) -> tuple[int, int]:
        dx = coordinates[0] - self.get_posX()
        dy = coordinates[1] - self.get_posY()
        return (dx, dy)