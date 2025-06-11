# Utility base class for Nodes in order to make the code
# more understandable, better structured and easier to
# adapt and fix

import numpy as np

class Robot:

    posX: int
    posY: int
    angle: int

    # [Constructor] with all the values for the robot
    # - posX      = (int) horizontal position of the robot in mm
    # - posY      = (int) vertical position of the robot in mm
    # (center (0,0) is left upper corner) 
    # - angle     = (int) degree in which direction the camera is facing
    #               (0° to the right - East, 90° straight down - South,
    #               180° to the left - Weast, 270° straight up - North)
    def __init__(self, posX: int, posY: int, angle: int):
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

    def getPosX(self) -> int:
        return self.posX
    
    def __setPosX(self, newPosX: int) -> None:
        self.posX = newPosX
    
    def getPosY(self) -> int:
        return self.posY
    
    def __setPosY(self, newPosY: int) -> None:
        self.posY = newPosY
    
    def getDirection(self) -> int:
        return self.angle
    
    def __setDirection(self, newAngle: int) -> None:
        self.angle = newAngle

    def changePosition(self, posX: int, posY: int) -> None:
        self.__setPosX(posX)
        self.__setPosY(posY)

    def turnAround(self, turnAngle: int) -> None:
        self.__setDirection = (self.getDirection + turnAngle) % 360

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
    def compute_distance(self, x: int, y: int) -> tuple[float, float]:
        # type check
        if not isinstance(x, int) or not isinstance(y, int):
            raise ImportError('Incorrct parameters')
        
        # setup
        dx = x - self.posX
        dy = y - self.posY
        
        # calculate angle
        baseDeg = 0
        # testing for edgecases and direction because arctan fails
        # if dx == 0 and it can only show angles from -90° to +90°
        # so it checks if the position is left (+90 to +270) or
        # right (-90 to +90) of the robot
        if dx == 0:
            if dy == 0:
                baseDeg = 0
            elif y > self.posY: 
                baseDeg = 90.0
            else:
                baseDeg = 270.0
        else:
            if x < self.posX:
                baseDeg = 180.0 + np.degrees(np.arctan(dy/dx))
            else:
                baseDeg = np.degrees(np.arctan(dy/dx)) % 360.0
        # getting the relative angle
        tempDeg = (baseDeg - float(self.angle)) % 360.0
        dDeg = 0
        # normalizing angle to be between -180° and +180°
        if tempDeg > 180.0:
            dDeg = tempDeg - 360.0
        else:
            dDeg = tempDeg

        # calculate distance
        dDis = float(np.sqrt(dx**2 + dy**2))
        
        return (dDeg, dDis)