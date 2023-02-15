from enum import Enum


class GarmentType(Enum):
    SLOUCH_HAT = 3
    HAT = 4
    SCARF = 1
    COWL = 2


def get_garment_type_by_name(gname):
    if gname == "HAT":
        return GarmentType.HAT
    elif gname == "SLOUCH_HAT":
        return GarmentType.SLOUCH_HAT
    elif gname == "SCARF":
        return GarmentType.SCARF
    elif gname == "COWL":
        return GarmentType.COWL
    else:
        return GarmentType.HAT
