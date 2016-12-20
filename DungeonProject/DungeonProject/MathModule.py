import sys
import math

class MathModule:
    
    # Added for precision issues
    @staticmethod
    def sin(angle):
        while angle < 0:
            angle += 360
        while angle >= 360:
            angle -= 360
        return {
            0: 0,
            90: 1,
            180: 0,
            270: -1
            }.get(angle, math.sin(math.radians(angle)))

    # Added for precision issues
    @staticmethod
    def cos(angle):
        while angle < 0:
            angle += 360
        while angle >= 360:
            angle -= 360
        return {
            0: 1,
            90: 0,
            180: -1,
            270: 0
            }.get(angle, math.cos(math.radians(angle)))





