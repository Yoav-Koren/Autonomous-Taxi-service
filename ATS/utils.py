class Utils:
    def _calculate_manhatten_distance(x1,x2,y1,y2)->int:
        return int(abs(x1 - x2) + abs(y1 - y2))