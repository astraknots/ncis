from enum import Enum

from src.pattern.enums.GarmentType import GarmentType


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
        garment_dict_str = ""
        for g in self.garment_dict:

            #print("X", self.garment_dict[g])
            aspect_str = ""
            for planet_dict in self.garment_dict[g]:
                for p_entry in planet_dict:
                    #print("Y", p_entry)
                    aspect_str = aspect_str + str(p_entry) + "\n"
                    for aspect in planet_dict[p_entry]:
                        #print("Z", aspect)
                        aspect_str = aspect_str + "     " + str(aspect) + "\n"
            garment_dict_str = garment_dict_str + str(g) + " : " + aspect_str + "\n"

        return f"{self.garment_type.name} (degrees/st = {self.garment_type.value}) \n {garment_dict_str}"

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
