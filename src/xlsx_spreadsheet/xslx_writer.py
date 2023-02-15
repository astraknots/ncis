import logging

import constants
from src.xlsx_spreadsheet.AstraXslxChart import AstraXslxChart


def write_orb_range_to_fsheet(orb_range_start, orb_range_end, header_row_cnt, p_cnt, planet, aspect, xchart):
    '''Write formatted planet color range of an orb to the sheet'''
    degree_inc = xchart.degree_inc()  # the degree increment we're charting per row (i.e. COWL = 2)

    # aspect_score = aspects.get_aspect_score(aspect)
    for orb_color_range in range(orb_range_start, orb_range_end):
        orb_color_row = int(orb_color_range / degree_inc)
        orb_row = orb_color_row + header_row_cnt
        # logging.debug(
        #    "Orb row:" + str(orb_row) + " p_cnt_col:" + str(p_cnt) + " for planet:" + planet + " and aspect:" + aspect)
        xchart.write_to_sheet_format(orb_row, p_cnt, planet.name + ' ' + aspect.name,
                                     xchart.get_cell_color_format(planet.color))
    # xchart.write_to_sheet(orb_row, p_cnt+len(constants.PLANETS), aspect_score)


def write_orb_colors_to_sheet(achart, xchart, h_row_cnt):
    '''Color in the orb sections of the chart'''

    # Loop over the orbs by planet and color in
    p_cnt = constants.SHEET_PLANET_COLOR_COL_START
    for planet in achart.aspect_orbs_by_planet:
        aspect_range = achart.aspect_orbs_by_planet[planet]
        for aspect in aspect_range:
            orb_range_start = aspect_range[aspect][0]
            orb_range_end = aspect_range[aspect][1]
            logging.debug("orb range:[" + str(orb_range_start) + " to " + str(orb_range_end) + "]")
            if orb_range_end < orb_range_start:  # then it's like [349 to 1] and loops over the end of Pisces to Aries
                # so break it into two

                write_orb_range_to_fsheet(orb_range_start, constants.MAX_CHART_DEGREES, h_row_cnt, p_cnt, planet,
                                          aspect,
                                          xchart)
                write_orb_range_to_fsheet(constants.MIN_CHART_DEGREES, orb_range_end, h_row_cnt, p_cnt, planet,
                                          aspect,
                                          xchart)
            else:
                write_orb_range_to_fsheet(orb_range_start, orb_range_end, h_row_cnt, p_cnt, planet,
                                          aspect,
                                          xchart)
        p_cnt += 1


def inc_cnt_to_next_sign(deg, deg_inc):
    '''If we've reached a degree in the next sign, return 1 to increment sign cnter, else return 0'''
    thirty = constants.MAX_SIGN_DEGREES
    zero = constants.MIN_SIGN_DEGREES
    cnt_to_next_sign = 0
    if deg % thirty == zero and deg != zero:
        cnt_to_next_sign += 1
    elif deg >= thirty and deg % thirty < deg_inc:
        # print("deg=", deg, " deg % 30=", deg % thirty, " dec inc:", deg_inc)
        cnt_to_next_sign += 1
    return cnt_to_next_sign


def write_chart_and_pattern(garment, astra_chart):
    """Write an astrology Chart & pattern to a spreadsheet"""
    wchart = AstraXslxChart(astra_chart.chartname)
    wchart.create_chart_booksheet(astra_chart.person)
    # this changes based on the pattern and how many degrees are represented by a stitch
    wchart.set_garment(garment.garment_type)
    deg_increments = wchart.degree_inc()

    # logging.info("Creating a blank astrology chart workbook named:" + wname)

    # iterating rows in spreadsheet
    row_cnt = 0
    # loop through signs array
    sign_cnt = 0

    # set width of first few columns
    wchart.set_col_width(0, constants.SHEET_DEGREE_SIGN_COL, 22)

    ## Section for top of sheet headers ##
    wchart.write_to_sheet_format(row_cnt, constants.USER_CHART_PLANET_COL, "Sign Degree: [Planet]",
                                 wchart.get_bold_format())
    wchart.write_to_sheet_format(row_cnt, constants.USER_CHART_DIGNITY_COL, "Dignity [Score]", wchart.get_bold_format())
    wchart.write_to_sheet_format(row_cnt, constants.USER_CHART_ASPECT_COL, "360 Degree: [Aspect]",
                                 wchart.get_bold_format())
    wchart.write_to_sheet_format(row_cnt, constants.SHEET_DEGREE_SIGN_COL, "Degree Sign", wchart.get_bold_format())
    wchart.write_to_sheet_format(row_cnt, constants.SHEET_DEGREE_COL, "Degree range start", wchart.get_bold_format())
    p_cnt = constants.SHEET_PLANET_COLOR_COL_START
    for planet in constants.PLANETS:
        wchart.write_to_sheet_format(row_cnt, p_cnt, planet.capitalize(), wchart.get_bold_format())
        p_cnt += 1

    # For planet aspect score
    for planet in constants.PLANETS:
        wchart.write_to_sheet_format(row_cnt, p_cnt, planet.capitalize() + " Aspect Score", wchart.get_bold_format())
        p_cnt += 1

    # Knitting pattern column setup
    # AC:  Personal Total column (leave blank for now, will do some excel calc)
    # AD-AE: Identifying cols for sig aspects (leave blank)
    # AF: Pattern
    # AG: Stitches
    # AH: Rounds:
    wchart.write_to_sheet_format(row_cnt, p_cnt, "Personal Total".capitalize(), wchart.get_bold_format())
    p_cnt += 3

    wchart.write_to_sheet_format(row_cnt, p_cnt, "Pattern", wchart.get_bold_format())
    PATTERN_COL = p_cnt
    p_cnt += 1

    wchart.write_to_sheet_format(row_cnt, p_cnt, "Stitches", wchart.get_bold_format())
    STITCH_COL = p_cnt
    p_cnt += 1
    st_cnt = 1

    wchart.write_to_sheet_format(row_cnt, p_cnt, "Rounds:", wchart.get_bold_format())
    p_cnt += 1
    # write round numbers going to the right
    for rnd_cnt in range(1, 17):  # TODO: replace 17 with something dynamic, perhaps later
        wchart.write_to_sheet_format(row_cnt, p_cnt + rnd_cnt, str(rnd_cnt), wchart.get_bold_format())
    ## End knitting pattern header col setup ##

    row_cnt += 1

    ## End section for top of sheet headers ##

    ## Section to prepare chart data ##
    write_orb_colors_to_sheet(astra_chart, wchart, row_cnt)
    ## End section to prepare chart data

    # Loop over the 360 chart
    for deg in garment.garment_dict:
        pattern_info = garment.garment_dict[deg]
        chart_info = garment.planet_aspect_scored_dict[deg]

        #  write out chart degrees in Col C
        wchart.write_to_sheet(row_cnt, constants.SHEET_DEGREE_COL, str(deg))

        # increment counter to next sign after 30 - i.e. when it is time
        sign_cnt += inc_cnt_to_next_sign(deg, deg_increments)

        # Get sign name from array
        sign_name = constants.SIGNS[sign_cnt]
        sign_deg = str(deg % constants.MAX_SIGN_DEGREES)
        # Add row of ex: '0 Aries" etc
        wchart.write_to_sheet(row_cnt, constants.SHEET_DEGREE_SIGN_COL, sign_deg + ' ' + sign_name.capitalize())

        wchart.set_row_cnt(row_cnt)
        # print("Row cnt: ", row_cnt)
        ## Section for writing specifics of a chart out ##
        if len(chart_info) > 0:  # since it's a list
            chart_dict = chart_info[0]
            user_chart_planets = ""
            user_chart_dignities = ""
            user_chart_planet_aspects = ""
            planets_at_sign_deg = []
            aspects_at_deg = []

            for chart_planet in chart_dict:
                chart_sign_deg = chart_planet.sign_degree
                planet_name = chart_planet.planet_name
                planet_sign_dignity = chart_planet.sign_dignity
                chart_aspects = chart_dict[chart_planet]
                # print("_________chart_planet & chart_sign_dg & planet sign dignity______")
                # print(chart_planet, " ", chart_sign_deg, " ", planet_sign_dignity)
                planets_at_sign_deg.append(planet_name)
                if planet_sign_dignity:
                    planet_sign_dignity.sign_dignity_score
                    user_chart_dignities += str(planet_sign_dignity.dignity_type.name) + ": [" + str(
                        planet_sign_dignity.sign_dignity_score) + "] "

                for an_aspect in chart_aspects:
                    asp_str = f"{an_aspect.aspect_score.deg_from_exact} {an_aspect.direction.name} {an_aspect.name} to " \
                              f"{an_aspect.planets_in_aspect[1].planet_name}"

                    aspects_at_deg.append(asp_str)

            user_chart_planets += str(chart_sign_deg[1].degree_360) + ": [" + '; '.join(planets_at_sign_deg) + "] "
            user_chart_planet_aspects += str(chart_sign_deg[1].degree_360) + ": [" + '; '.join(aspects_at_deg) + "] "

            wchart.write_to_sheet(wchart.row_cnt, constants.USER_CHART_PLANET_COL, user_chart_planets)
            wchart.write_to_sheet(wchart.row_cnt, constants.USER_CHART_DIGNITY_COL, user_chart_dignities)
            wchart.write_to_sheet(wchart.row_cnt, constants.USER_CHART_ASPECT_COL, user_chart_planet_aspects)

        ## End section for writing chart specifics

        ## Section for writing knitting pattern
        wchart.write_to_sheet(row_cnt, STITCH_COL, st_cnt)
        st_cnt += 1

        # write in the pattern stuff
        if len(pattern_info) > 0:  # it's a list
            aspect_pattern_str = ""
            aspect_pattern_sts = []

            for stitchd in pattern_info:
                #print("_________stitchd_______")
                #print(stitchd)
                aspect_pattern_sts.append(str(stitchd))

            aspect_pattern_str += f"{chart_sign_deg[1].degree_360}: [{'; '.join(aspect_pattern_sts)}]"

            wchart.write_to_sheet(wchart.row_cnt, PATTERN_COL, aspect_pattern_str)
        ## End section for writing knitting pattern

        row_cnt += 1

    # Close the workbook
    wchart.close_book()

