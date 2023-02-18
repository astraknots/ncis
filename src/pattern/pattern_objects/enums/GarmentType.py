from enum import Enum

from src.chart.chart_objects.ChartPlanet import ChartPlanet


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


def is_chart_planet_for_garment_type(gtype, chart_planet):
    '''Return true if this ChartPlanet is included in this garment type, false otherwise'''
    if isinstance(chart_planet, ChartPlanet):
        return is_planet_for_garment_type(gtype, chart_planet.planet)
    else:
        print("Wrong input type: ", type(chart_planet), ". Expected: ChartPlanet")


def is_planet_for_garment_type(gtype, planet):
    '''Return true if this ChartPlanet is included in this garment type, false otherwise'''
    if gtype in [GarmentType.HAT, GarmentType.SLOUCH_HAT]:
        #print("Hats are big three planets...")
        return planet.is_big_three()
    elif gtype in [GarmentType.SCARF, GarmentType.COWL]:
        print("All planets included for garment type:", gtype)
        return True # TODO: fix this later for other garment types
    else:
        print("No planets specified for garment type: ", gtype)
        return False

