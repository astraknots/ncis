from src.pattern.pattern_objects.enums.GarmentType import GarmentType


class Garment:
    garment_type = GarmentType.HAT
    planet_aspect_scored_dict = {}
    garment_dict = {}

    def __init__(self, garment_type):
        a_garment = garment_type
        if isinstance(a_garment, GarmentType):
            self.garment_type = a_garment
        else:
            self.garment_type = GarmentType[a_garment]
        self.garment_dict = self.get_garment_degree_dict()
        self.planet_aspect_scored_dict = self.get_garment_degree_dict()

    def get_str_garment_rep(self):
        garment_dict_str = ""
        for g in self.garment_dict:
            for sd in self.garment_dict[g]:
                garment_dict_str = garment_dict_str + str(g) + " : " + str(sd) + "\n"
        return garment_dict_str

    def get_str_planet_aspect_rep(self):
        scored_aspect_dict_str = ""
        for g in self.planet_aspect_scored_dict:

            # print("X", self.garment_dict[g])
            aspect_str = ""
            for planet_dict in self.planet_aspect_scored_dict[g]:
                for p_entry in planet_dict:
                    # print("Y", p_entry)
                    aspect_str = aspect_str + str(p_entry) + "\n"
                    for aspect in planet_dict[p_entry]:
                        # print("Z", aspect)
                        aspect_str = aspect_str + "     " + str(aspect) + "\n"
            scored_aspect_dict_str = scored_aspect_dict_str + str(g) + " : " + aspect_str + "\n"
        return scored_aspect_dict_str

    def get_str_rep(self):
        garment_dict_str = self.get_str_garment_rep()
        scored_aspect_dict_str = self.get_str_planet_aspect_rep()

        return f"{self.garment_type.name} (degrees/st = {self.garment_type.value}) \n Scored Aspects: \n " \
               f"{scored_aspect_dict_str} Garment Guidance for {self.garment_type.name} ({self.garment_type.value} " \
               f"degrees/stitch): \n {garment_dict_str} \n "

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
