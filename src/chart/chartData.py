#!/usr/bin/python

from enums import SignDegreeBase as sd


# Start with a chart
# Genevieve's chart
gchart = { 'SUN' : ['PISCES',1], 'MOON' : ['CAPRICORN', 17], 'ASC' : ['VIRGO', 28], 'MERCURY' : ['AQUARIUS', 5], 'VENUS' : ['CAPRICORN', 25], 'MARS' : ['LIBRA', 19], 'JUPITER' : ['SCORPIO', 10], 'SATURN' : ['LIBRA', 21], 'URANUS' : ['SAGITTARIUS', 4], 'NEPTUNE' : ['SAGITTARIUS', 26], 'PLUTO' : ['LIBRA', 26]}
#gchart = { 'SUN' : [sd.PISCES,1], 'MOON' : [sd.CAPRICORN, 17], 'ASC' : [sd.VIRGO, 28], 'MERCURY' : [sd.AQUARIUS, 5], 'VENUS' : [sd.CAPRICORN, 25], 'MARS' : [sd.LIBRA, 19], 'JUPITER' : [sd.SCORPIO, 10], 'SATURN' : [sd.LIBRA, 21], 'URANUS' : [sd.SAGITTARIUS, 4], 'NEPTUNE' : [sd.SAGITTARIUS, 26], 'PLUTO' : [sd.LIBRA, 26]}

# Brian's chart
bchart = { 'SUN' : ['VIRGO',8], 'MOON' : ['SCORPIO', 2], 'ASC' : ['LEO', 17], 'MERCURY' : ['VIRGO', 7], 'VENUS' : ['LIBRA', 15], 'MARS' : ['TAURUS', 6], 'JUPITER' : ['AQUARIUS', 3], 'SATURN' : ['CANCER', 2], 'URANUS' : ['LIBRA', 20], 'NEPTUNE' : ['SAGITTARIUS', 4], 'PLUTO' : ['LIBRA', 3]}

# Jacob's chart
jchart = { 'SUN' : ['SCORPIO',24], 'MOON' : ['CANCER', 28], 'ASC' : ['SAGITTARIUS', 16], 'MERCURY' : ['SCORPIO', 5], 'VENUS' : ['CAPRICORN', 4], 'MARS' : ['LIBRA', 7], 'JUPITER' : ['GEMINI', 7], 'SATURN' : ['TAURUS', 27], 'URANUS' : ['AQUARIUS', 17], 'NEPTUNE' : ['AQUARIUS', 4], 'PLUTO' : ['SAGITTARIUS', 12]}

# Rebecca's chart
rchart = { 'SUN' : ['CANCER',14], 'MOON' : ['VIRGO', 21], 'ASC' : ['CAPRICORN', 18], 'MERCURY' : ['GEMINI', 26], 'VENUS' : ['LEO', 8], 'MARS' : ['GEMINI', 22], 'JUPITER' : ['LIBRA', 2], 'SATURN' : ['LIBRA', 3], 'URANUS' : ['SCORPIO', 26], 'NEPTUNE' : ['SAGITTARIUS', 22], 'PLUTO' : ['LIBRA', 21]}

# JenniAdams's chart
jachart = { 'SUN' : ['TAURUS',17], 'MOON' : ['SCORPIO', 0], 'ASC' : ['AQUARIUS', 3], 'MERCURY' : ['TAURUS', 10], 'VENUS' : ['ARIES', 4], 'MARS' : ['PISCES', 12], 'JUPITER' : ['CANCER', 8], 'SATURN' : ['CAPRICORN', 25], 'URANUS' : ['CAPRICORN', 9], 'NEPTUNE' : ['CAPRICORN', 14], 'PLUTO' : ['SCORPIO', 16]}

# Linda Janiszewski's chart
ljchart = { 'SUN' : ['SAGITTARIUS', 16], 'MOON' : ['GEMINI', 1], 'ASC' : ['CANCER', 2], 'MERCURY' : ['SAGITTARIUS', 7], 'VENUS' : ['SCORPIO', 14], 'MARS' : ['PISCES', 3], 'JUPITER' : ['CANCER', 29], 'SATURN' : ['SCORPIO', 16], 'URANUS' : ['CANCER', 27], 'NEPTUNE' : ['LIBRA', 27], 'PLUTO' : ['LEO', 26]}

# AnnieWolff's chart
awchart = { 'SUN' : ['TAURUS',27], 'MOON' : ['ARIES', 23], 'ASC' : ['CANCER', 22], 'MERCURY' : ['GEMINI', 0], 'VENUS' : ['ARIES', 14], 'MARS' : ['LEO', 10], 'JUPITER' : ['LIBRA', 5], 'SATURN' : ['AQUARIUS', 29], 'URANUS' : ['CAPRICORN', 21], 'NEPTUNE' : ['CAPRICORN', 20], 'PLUTO' : ['SCORPIO', 24]}

# CaseyWeiss's chart
cwchart = { 'SUN' : ['GEMINI',27], 'MOON' : ['AQUARIUS', 8], 'ASC' : ['SCORPIO', 0], 'MERCURY' : ['CANCER', 17], 'VENUS' : ['GEMINI', 29], 'MARS' : ['TAURUS', 3], 'JUPITER' : ['VIRGO', 8], 'SATURN' : ['AQUARIUS', 18], 'URANUS' : ['CAPRICORN', 16], 'NEPTUNE' : ['CAPRICORN', 18], 'PLUTO' : ['SCORPIO', 20]}

#Jen Creighton's chart
jcchart = { 'SUN' : ['ARIES',7], 'MOON' : ['ARIES', 9], 'ASC' : ['CAPRICORN', 28], 'MERCURY' : ['ARIES', 0], 'VENUS' : ['AQUARIUS', 29], 'MARS' : ['PISCES', 22], 'JUPITER' : ['CANCER', 29], 'SATURN' : ['VIRGO', 8], 'URANUS' : ['SCORPIO', 20], 'NEPTUNE' : ['SAGITTARIUS', 20], 'PLUTO' : ['LIBRA', 18]}

#Katie Scuggs's chart
kschart = { 'SUN' : ['PISCES',23], 'MOON' : ['AQUARIUS', 26], 'ASC' : ['SCORPIO', 1], 'MERCURY' : ['ARIES', 4], 'VENUS' : ['ARIES', 24], 'MARS' : ['GEMINI', 19], 'JUPITER' : ['LEO', 3], 'SATURN' : ['AQUARIUS', 3], 'URANUS' : ['CAPRICORN', 13], 'NEPTUNE' : ['CAPRICORN', 16], 'PLUTO' : ['SCORPIO', 20]}

#Rebecca Barnard's chart
rbchart = { 'SUN' : ['AQUARIUS',0], 'MOON' : ['GEMINI', 4], 'ASC' : ['LEO', 11], 'MERCURY' : ['CAPRICORN', 23], 'VENUS' : ['AQUARIUS', 1], 'MARS' : ['SCORPIO', 22], 'JUPITER' : ['AQUARIUS', 22], 'SATURN' : ['SAGITTARIUS', 7], 'URANUS' : ['SAGITTARIUS', 20], 'NEPTUNE' : ['CAPRICORN', 4], 'PLUTO' : ['SCORPIO', 7]}

#Natalie Montoya's chart
nmchart = { 'SUN' : ['AQUARIUS',10], 'MOON' : ['VIRGO', 4], 'ASC' : ['PISCES', 20], 'MERCURY' : ['CAPRICORN', 17], 'VENUS' : ['PISCES', 1], 'MARS' : ['PISCES', 10], 'JUPITER' : ['SAGITTARIUS', 6], 'SATURN' : ['SCORPIO', 4], 'URANUS' : ['SAGITTARIUS', 8], 'NEPTUNE' : ['SAGITTARIUS', 28], 'PLUTO' : ['LIBRA', 29]}

#Marie V's chart
mvchart = { 'SUN' : ['VIRGO',3], 'MOON' : ['PISCES', 12], 'ASC' : ['SAGITTARIUS', 13], 'MERCURY' : ['VIRGO', 14], 'VENUS' : ['CANCER', 26], 'MARS' : ['LIBRA', 6], 'JUPITER' : ['CAPRICORN', 28], 'SATURN' : ['CAPRICORN', 24], 'URANUS' : ['LEO', 26], 'NEPTUNE' : ['SCORPIO', 8], 'PLUTO' : ['VIRGO', 7]}
mvchart_r = { 'SUN' : ['VIRGO',3], 'MOON' : ['PISCES', 12], 'ASC' : ['SAGITTARIUS', 2], 'MERCURY' : ['VIRGO', 14], 'VENUS' : ['CANCER', 26], 'MARS' : ['LIBRA', 6], 'JUPITER' : ['CAPRICORN', 28], 'SATURN' : ['CAPRICORN', 24], 'URANUS' : ['LEO', 26], 'NEPTUNE' : ['SCORPIO', 8], 'PLUTO' : ['VIRGO', 7]}

#CALLIA Stylianou's chart
cschart = { 'SUN' : ['AQUARIUS',26], 'MOON' : ['AQUARIUS', 20], 'ASC' : ['GEMINI', 14], 'MERCURY' : ['PISCES', 5], 'VENUS' : ['PISCES', 22], 'MARS' : ['SCORPIO', 7], 'JUPITER' : ['ARIES', 0], 'SATURN' : ['ARIES', 28], 'URANUS' : ['AQUARIUS', 13], 'NEPTUNE' : ['AQUARIUS', 2], 'PLUTO' : ['SAGITTARIUS', 10]}


def get_chart_person(chartname):
    '''Mapping of names to chart data is in this method'''
    if chartname == 'gchart':
        return 'Genevieve'
    elif chartname == 'bchart':
        return 'Brian'
    elif chartname == 'jchart':
        return 'Jacob'
    elif chartname == 'rchart':
        return 'Becca'
    elif chartname == 'jachart':
        return 'Jenni Adams'
    elif chartname == 'ljchart':
        return 'Linda Janiszewski'
    elif chartname == 'awchart':
        return 'Annie Wolff'
    elif chartname == 'cwchart':
        return 'Casey Weiss'
    elif chartname == 'jcchart':
        return 'Jen Creighton'
    elif chartname == 'kschart':
        return 'Katie Scruggs'
    elif chartname == 'rbchart':
        return 'Rebecca Barnard'
    elif chartname == 'nmchart':
        return 'Natalie Montoya'
    elif chartname == 'mvchart' or chartname == 'mvchart_r':
        return 'Marie V'
    elif chartname == 'cschart':
        return 'Callia Stylianou'
    else:
        return 'Other User'


def get_chart(chartname):
    print("Looking up chartname: ", chartname, " in chartData")
    for name in globals().keys():
        #print(name)
        if name == chartname:
            print("Found chart matching: ", globals()[name])
            return globals()[name]


