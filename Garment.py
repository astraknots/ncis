from enum import Enum


class GarmentType(Enum):
    SLOUCH_HAT = 3
    HAT = 4
    SCARF = 1
    COWL = 2


class Garment:
    garment_type = GarmentType.HAT
    garment_dict = {}

    def __init__(self, *args):
        a_garment = args[0]
        if isinstance(a_garment, GarmentType):
            self.garment_type = a_garment
        else:
            self.garment_type = GarmentType[a_garment]
        self.garment_dict = self.get_garment_degree_dict()

    def get_str_rep(self):
        return f"{self.garment_type.name} (degrees/st = {self.garment_type.value})"

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()

    def get_garment_degree_dict(self):
        garment_dict = {}
        deg_inc = self.garment_type.value
        for d in range(0, 360, deg_inc):
            garment_dict[d] = []
        return garment_dict
