from datetime import datetime


class Ticket:
    def __init__(self, plate, floor):
        self._plate = plate
        self._floor = floor
        self._arrival = datetime.now()

    @property
    def arrival(self):
        return self._arrival


class Floor:
    def __init__(self, id, spaces=48):
        self._id = id
        self._spaces = spaces
        self._car = 0

    def av_spaces(self): # available spaces
        return self._spaces - self._car


class Parking:
    def __init__(self, floor):
        pass

