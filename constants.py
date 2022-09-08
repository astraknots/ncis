#!/usr/bin/python

SIGNS = ['ARIES', 'TAURUS', 'GEMINI', 'CANCER', 'LEO', 'VIRGO', 'LIBRA', 'SCORPIO', 'SAGITARRIUS', 'CAPRICORN', 'AQUARIUS', 'PISCES']

PLANETS = ['SUN', 'MOON', 'ASC', 'MERCURY', 'VENUS', 'MARS', 'JUPITER', 'SATURN', 'URANUS', 'NEPTUNE','PLUTO']

BIG_THREE = ['SUN', 'MOON', 'ASC']

ASPECTS = ['CONJ', 'SEMISEXTILE', 'SEXTILE', 'SQUARE', 'TRINE', 'QUINCUNX', 'OPPOSITION']
ASPECTS2 = ['CONJ', 'SEXTILE', 'SQUARE', 'TRINE', 'OPPOSITION']

SIGNS_DEGREE_BASE = {'ARIES' : 0, 'TAURUS' : 30, 'GEMINI' : 60, 'CANCER' : 90, 'LEO' : 120, 'VIRGO' : 150 , 'LIBRA' : 180, 'SCORPIO' : 210, 'SAGITARRIUS' : 240, 'CAPRICORN' : 270, 'AQUARIUS' : 300, 'PISCES' : 330}

ORBS = {'CONJ' : 10, 'SEMISEXTILE' : 0, 'SEXTILE' : 6, 'SQUARE' : 8, 'TRINE' : 8, 'QUINCUNX' : 0, 'OPPOSITION' : 10, 'BIG3' : 9 }

ASPECT_DEGREES = {'CONJ' : 0, 'SEMISEXTILE' : 30, 'SEXTILE' : 60, 'SQUARE' : 90, 'TRINE' : 120, 'QUINCUNX' : 150, 'OPPOSITION' : 180}

ASPECT_VALUE = {'CONJ' : 0, 'SEMISEXTILE' : -30, 'SEXTILE' : 60, 'SQUARE' : -90, 'TRINE' : 120, 'QUINCUNX' : -150, 'OPPOSITION' : -180}

SIGN_ASPECT = {'ARIES' : 'TRINE', 'TAURUS' : 'SQUARE', 'GEMINI' : 'SEXTILE', 'CANCER' : 'SEMISEXTILE', 'LEO' : 'CONJ', 'VIRGO': 'SEMISEXTILE', 'LIBRA' : 'SEXTILE', 'SCORPIO' : 'SQUARE', 'SAGITARRIUS' : 'TRINE', 'CAPRICORN' : 'QUINCUNX', 'AQUARIUS' : 'OPPOSITION', 'PISCES' : 'QUINCUNX' }

SIGN_ELEMENT = {'ARIES' : 'FIRE', 'TAURUS' : 'EARTH', 'GEMINI' : 'AIR', 'CANCER' : 'WATER', 'LEO' : 'FIRE', 'VIRGO': 'EARTH', 'LIBRA' : 'AIR', 'SCORPIO' : 'WATER', 'SAGITARRIUS' : 'FIRE', 'CAPRICORN' : 'EARTH', 'AQUARIUS' : 'AIR', 'PISCES' : 'WATER' }

SIGN_MODE = {'ARIES' : 'CARDINAL', 'TAURUS' : 'FIXED', 'GEMINI' : 'MUTABLE', 'CANCER' : 'CARDINAL', 'LEO' : 'FIXED', 'VIRGO': 'MUTABLE', 'LIBRA' : 'CARDINAL', 'SCORPIO' : 'FIXED', 'SAGITARRIUS' : 'MUTABLE', 'CAPRICORN' : 'CARDINAL', 'AQUARIUS' : 'FIXED', 'PISCES' : 'MUTABLE' }

ELEMENT_SCORES = {'EARTH' : (2,6,10), 'AIR' : (3,7,11), 'WATER' : (4,8,12), 'FIRE' : (1,5,9)}

MODE_SCORES = {'CARDINAL' : (1,10,7,4), 'FIXED' : (5,2,11,8), 'MUTABLE' : (9,6,3,12)}

SIGN_SCORE = {'ARIES' : 1, 'TAURUS' : 2, 'GEMINI' : 3, 'CANCER' : 4, 'LEO' : 5, 'VIRGO': 6, 'LIBRA' : 7, 'SCORPIO' : 8, 'SAGITARRIUS' : 9, 'CAPRICORN' : 10, 'AQUARIUS' : 11, 'PISCES' : 12 }

GARMENTS = ['HAT', 'SCARF']
GARMENT_ST_TO_DEGREES = {'HAT' : 3, 'SCARF' : 1}

MAX_SIGN_DEGREES = 30
MIN_SIGN_DEGREES = 0
MAX_CHART_DEGREES = 360
MIN_CHART_DEGREES = 0

PATTERN_ASPECT_SCORES = { 'weavy' : ('SEXTILE', 61),
'butterflies' : ('SQUARE', 91),
'windmill' : ('CONJ', 1),
'feathered' : ('TRINE', 121),
'loopy' : ('OPPOSITION', 183),
'tree' : ('SQUARE', 94),
'circles' : ('QUINCUNX', 184),
'stringy' : ('OPPOSITION', 186),
'diagonals' : ('SEXTILE', 66),
'angles' : ('SQUARE', 97),
'messy' : ('SEMISEXTILE', 8),
'twisty' : ('SEMISEXTILE', 10),
'stars' : ('SEXTILE', 72),
'wavy' : ('TRINE', 132),
'diamonds' : ('TRINE', 139),
'triangles' : ('TRINE', 144),
'squares' : ('SQUARE', 115),
'holes' : ('QUINCUNX', 206),
'dots' : ('SEXTILE', 88),
'lines' : ('CONJ', 56) }

PATTERN_SHAPE_ASPECTS = { 'weavy' : 'SEXTILE',
'butterflies' : 'SQUARE',
'windmill' : 'CONJ',
'feathered' : 'TRINE',
'loopy' : 'OPPOSITION',
'tree' : 'SQUARE',
'circles' : 'QUINCUNX',
'stringy' : 'OPPOSITION',
'diagonals' : 'SEXTILE',
'angles' : 'SQUARE',
'messy' : 'SEMISEXTILE',
'twisty' : 'SEMISEXTILE',
'stars' : 'SEXTILE',
'wavy' : 'TRINE',
'diamonds' : 'TRINE',
'triangles' : 'TRINE',
'squares' : 'SQUARE',
'holes' : 'QUINCUNX',
'dots' : 'SEXTILE',
'lines' : 'CONJ' }

PATTERN_ASPECT_SHAPES = { 'SEXTILE' : ['weavy', 'diagonals', 'stars', 'dots'],
'SQUARE' : ['butterflies', 'tree', 'angles', 'squares'],
'CONJ' : ['windmill', 'lines'],
'TRINE' : ['feathered', 'wavy', 'diamonds', 'triangles'],
'OPPOSITION' : ['loopy', 'stringy'],
'QUINCUNX' : ['holes', 'circles'],
'SEMISEXTILE' : ['messy', 'twisty'] }

PATTERN_ASPECT_WEIGHTS = { 'SEXTILE' : (6,8),
'SQUARE' : (9,11),
'CONJ' : (0,3),
'TRINE' : (12,15),
'OPPOSITION' : (18,100),
'QUINCUNX' : (4,5),
'SEMISEXTILE' : (16,17) }

'''PATTERN_ASPECT_SCORES = { 'weavy' : ('SEXTILE', 1),
'butterflies' : ('SQUARE', 1),
'windmill' : ('CONJ', 1),
'feathered' : ('TRINE', 1),
'loopy' : ('OPPOSITION', 3),
'tree' : ('SQUARE', 4),
'circles' : ('OPPOSITION', 4),
'stringy' : ('OPPOSITION', 6),
'diagonals' : ('SEXTILE', 6),
'angles' : ('SQUARE', 7),
'messy' : ('CONJ', 8),
'twisty' : ('CONJ', 10),
'stars' : ('SEXTILE', 12),
'wavy' : ('TRINE', 12),
'diamonds' : ('TRINE', 19),
'triangles' : ('TRINE', 24),
'squares' : ('SQUARE', 25),
'holes' : ('OPPOSITION', 26),
'dots' : ('SEXTILE', 28),
'lines' : ('CONJ', 56) }
'''

PATTERN_MULT_ADD = { 'Basketweave' : (8, 5),
'Basketweave II' : (10, 0),
'Box Stitch' : (4, 2),
'Broken Rib' : (1, 1),
'Checks & Ridges' : (4, 2),
'Chevron' : (8, 1),
'Close Checks' : (6, 0),
'Diagonal Rib' : (4, 0),
'Diagonals' : (8, 6),
'Diamond Pattern' : (13, 0),
'Double Basket Weave' : (4, 3),
'Double Seed Stitch' : (4, 0),
'Elongated Chevron' : (18, 1),
'Embossed Diamonds' : (10, 3),
'Embossed Moss Rib' : (7, 3),
'Garter Rib' : (4, 2),
'Garter Stitch' : (1, 0),
'Garter Stitch Steps' : (8, 0),
'Inverness Diamonds' : (17, 0),
'King Charles Brocade' : (12, 1),
'Large Diamonds' : (15, 0),
'Little Pyramids' : (6, 5),
'Mistake Rib' : (4, 3),
'Mock Cable' : (10, 0),
'Moss Diamonds' : (10, 7),
'Moss Panels' : (8, 7),
'Moss Stitch' : (0, 0),
'Moss Stitch Border Diamonds' : (22, 1),
'Moss Stitch Parallelograms' : (10, 0),
'Parallelograms' : (10, 0),
'Parallelograms II' : (10, 0),
'Pavilion' : (18, 0),
'Pique Triangles' : (5, 0),
'Plain Diamonds' : (9, 0),
'Purled Ladder' : (4, 2),
'Rice Stitch' : (2, 1),
'Seed Rib' : (4, 1),
'Seed Stitch' : (0, 0),
'Single Chevron' : (8, 0),
'Spaced Checks' : (10, 2),
'Squares In Squares' : (10, 2),
'Thermal Underwear Stitch' : (4, 1),
'Triangle Ribs' : (8, 0),
'Triangle Squares' : (5, 0),
'Triangles' : (10, 0),
'Twin Rib' : (6, 0),
'Two By Two Rib' : (4, 0),
'Windmill' : (12, 0),
'Woven Stitch' : (4, 2),
'Brioche Rib' : (2, 0),
'Condo Stitch' : (0, 0),
'Fisherman\'s Rib' : (2, 0),
'Garter And Loops' : (4, 0),
'Layette' : (4, 0),
'Open Work Garter Ridges' : (2, 0),
'Roman Stripe' : (2, 0),
'Seafoam Stitch' : (10, 6),
'Butterfly' : (8, 7),
'Crossed Throw' : (3, 2),
'Diagonal Eyelets' : (2, 0),
'Eyelet Squares' : (10, 2),
'Garland' : (7, 0),
'Garter Eyelet' : (1, 0),
'Garter Lace' : (2, 2),
'Lace Ribbing' : (7, 0),
'Lacy Lattice': (6, 1),
'Ladder Rib' : (4, 2),
'Little Shell' : (7, 2),
'Open Honeycomb' : (1, 0),
'Open Twisted Rib' : (5, 3),
'Pillar Openwork' : (3, 2),
'Purl Barred Scallop I' : (13, 2),
'Purl Barred Scallop II' : (14, 1),
'Shell Lace' : (11, 1),
'Star Rib Mesh' : (4, 1),
'Triple Chevron' : (12, 5),
'Two Color Star' : (3, 0),
'Veil Stitch' : (0, 0),
'Zig Zag Lace' : (2, 0),
'Abstract' : (8, 3),
'Lattice' : (12, 3),
'Pyramid' : (28, 3),
'Zig Zag' : (6, 0),
'Afghan Stitch' : (12, 5),
'Two Color Basketweave' : (3, 0),
'Chevron Stripes' : (14, 2),
'Diamond Check' : (6, 3),
'Dots And Dashes' : (10, 7),
'Dots Within Stripes' : (2, 0),
'Flame Stitch' : (4, 1),
'Linked Stripe' : (4, 0),
'Swiss Check' : (4, 1),
'Triangle Check' : (6, 3),
'Two Color Lattice' : (6, 2),
'Two Stitch Check' : (4, 0),
'Welted Fantastic' : (13, 0),
'Bee Stitch' : (1, 0),
'Blanket Moss Stitch' : (2, 1),
'Chevron & Feather' : (13, 1),
'Crossed Throw' : (3, 2),
'Daisy Stitch' : (4, 1),
'Double Mock Rib' : (4, 2),
'Double Stockinette' : (0, 0),
'Double Lattice' : (6, 4),
'Gingham' : (10, 2),
'Hunter\'s Stitch' : (11, 4),
'Knit Lattice' : (16, 2),
'Knot Stitch' : (6, 2),
'Knotted Rib' : (5, 0),
'Linen Stitch' : (1, 0),
'Little Butterfly' : (10, 7),
'Mock Honeycomb' : (4, 1),
'Plaited Basket Stitch' : (1, 0),
'Puff Rib' : (3, 2),
'Quilted Lattice' : (6, 3),
'Ridges' : (6, 0),
'Rose Stitch' : (2, 1),
'Royal Quilting' : (6, 3),
'Slip Stitch Honeycomb' : (1, 0),
'Trellis Stitch' : (6, 5),
'Trinity Stitch' : (4, 0),
'Waffle Seed Stitch' : (1, 0),
'Waterfall' : (6, 3),
'Woven Herringbone' : (4, 2),
'6/6 Cable' : (10, 0),
'6/8 Cable' : (10, 0),
'8/10 Cable' : (12, 0),
'Bobble Tree' : (12, 0),
'Cabled Feather' : (18, 0),
'Criss Cross Cable With Twists' : (16, 0),
'Eccentric Cable' : (10, 0),
'Eccentric Cable II' : (10, 0),
'Twisted Braided Cable' :  (11, 0),
'Wave Lattice' : (6, 2),
'Knit' : (1,0),
'Purl' : (1,0) }

PATTERN_ROWS = {'Basketweave' : 8,
'Basketweave II' : 12,
'Box Stitch' : 4,
'Broken Rib' : 2,
'Checks & Ridges' : 4,
'Chevron' : 16,
'Close Checks' : 8,
'Diagonal Rib' : 8,
'Diagonals' : 8,
'Diamond Pattern' : 12,
'Double Basket Weave' : 8,
'Double Seed Stitch' : 4,
'Elongated Chevron' : 16,
'Embossed Diamonds' : 10,
'Embossed Moss Rib' : 4,
'Garter Rib' : 1,
'Garter Stitch' : 1,
'Garter Stitch Steps' : 16,
'Inverness Diamonds' : 12,
'King Charles Brocade' : 12,
'Large Diamonds' : 14,
'Little Pyramids' : 6,
'Mistake Rib' : 1,
'Mock Cable' : 6,
'Moss Diamonds' : 12,
'Moss Panels' : 10,
'Moss Stitch' : 4,
'Moss Stitch Border Diamonds' : 36,
'Moss Stitch Parallelograms' : 6,
'Parallelograms' : 10,
'Parallelograms II' : 24,
'Pavilion' : 36,
'Pique Triangles' : 4,
'Plain Diamonds' : 8,
'Purled Ladder' : 8,
'Rice Stitch' : 2,
'Seed Rib' : 2,
'Seed Stitch' : 2,
'Single Chevron' : 4,
'Spaced Checks' : 10,
'Squares In Squares' : 12,
'Thermal Underwear Stitch' : 4,
'Triangle Ribs' : 12,
'Triangle Squares' : 4,
'Triangles' : 10,
'Twin Rib' : 2,
'Two By Two Rib' : 2,
'Windmill' : 14,
'Woven Stitch' : 8,
'Brioche Rib' : 2,
'Condo Stitch' : 0,
'Fisherman\'s Rib' : 1,
'Garter And Loops' : 4,
'Layette' : 9,
'Open Work Garter Ridges' : 3,
'Roman Stripe' : 7,
'Seafoam Stitch' : 8,
'Butterfly' : 8,
'Crossed Throw' : 4,
'Diagonal Eyelets' : 4,
'Eyelet Squares' : 12,
'Garland' : 14,
'Garter Eyelet' : 6,
'Garter Lace' : 10,
'Lace Ribbing' : 4,
'Lacy Lattice' : 8,
'Ladder Rib' : 6,
'Little Shell' : 4,
'Open Honeycomb' : 4,
'Open Twisted Rib' : 4,
'Pillar Openwork' : 2,
'Purl Barred Scallop I' : 12,
'Purl Barred Scallop II' : 12,
'Shell Lace' : 12,
'Star Rib Mesh' : 4,
'Triple Chevron' : 18,
'Two Color Star' : 4,
'Veil Stitch' : 1,
'Zig Zag Lace' : 12,
'Abstract' : 15,
'Lattice' : 24,
'Pyramid' : 22,
'Zig Zag' : 40,
'Afghan Stitch' : 4,
'Two Color Basketweave' : 4,
'Chevron Stripes' : 4,
'Diamond Check' : 12,
'Dots And Dashes' : 8,
'Dots Within Stripes' : 20,
'Flame Stitch' : 4,
'Linked Stripe' : 16,
'Swiss Check' : 8,
'Triangle Check' : 8,
'Two Color Lattice' : 8,
'Two Stitch Check' : 8,
'Welted Fantastic' : 12,
'Bee Stitch' : 4,
'Blanket Moss Stitch' : 4,
'Chevron & Feather' : 2,
'Crossed Throw' : 4,
'Daisy Stitch' : 4,
'Double Mock Rib' : 2,
'Double Stockinette' : 2,
'Double Lattice' : 12,
'Gingham' : 36,
'Hunter\'s Stitch' : 2,
'Knit Lattice' : 16,
'Knot Stitch' : 8,
'Knotted Rib' : 2,
'Linen Stitch' : 2,
'Little Butterfly' : 12,
'Mock Honeycomb' : 12,
'Plaited Basket Stitch' : 2,
'Puff Rib' : 4,
'Quilted Lattice' : 8,
'Ridges' : 4,
'Rose Stitch' : 4,
'Royal Quilting' : 8,
'Slip Stitch Honeycomb' : 4,
'Trellis Stitch' : 12,
'Trinity Stitch' : 4,
'Waffle Seed Stitch' : 4,
'Waterfall' : 6,
'Woven Herringbone' : 24,
'6/6 Cable' : 6,
'6/8 Cable' : 8,
'8/10 Cable' : 4,
'Bobble Tree' : 10,
'Cabled Feather' : 8,
'Criss Cross Cable With Twists' : 23,
'Eccentric Cable' : 18,
'Eccentric Cable II' : 18,
'Twisted Braided Cable' : 12,
'Wave Lattice' : 8,
'Knit' : 1,
'Purl' : 1 }

PATTERN_SHAPES = {'Basketweave' : ['squares'],
'Basketweave II' : ['squares'],
'Box Stitch' : ['squares'],
'Broken Rib' : ['lines', 'dots'],
'Checks & Ridges' : ['messy', 'dots'],
'Chevron' : ['triangles'],
'Close Checks' : ['squares'],
'Diagonal Rib' : ['diagonals', 'lines'],
'Diagonals' : ['diagonals', 'lines'],
'Diamond Pattern' : ['diamonds'],
'Double Basket Weave' : ['messy', 'dots'],
'Double Seed Stitch' : ['squares'],
'Elongated Chevron' : ['triangles'],
'Embossed Diamonds' : ['diamonds'],
'Embossed Moss Rib' : ['lines', 'dots'],
'Garter Rib' : ['lines'],
'Garter Stitch' : ['dots', 'lines'],
'Garter Stitch Steps' : ['diagonals', 'squares'],
'Inverness Diamonds' : ['diamonds'],
'King Charles Brocade' : ['diamonds'],
'Large Diamonds' : ['diamonds'],
'Little Pyramids' : ['triangles', 'diamonds'],
'Mistake Rib' : ['lines', 'dots'],
'Mock Cable' : ['triangles'],
'Moss Diamonds' : ['lines'],
'Moss Panels' : ['lines', 'diamonds', 'dots'],
'Moss Stitch' : ['dots'],
'Moss Stitch Border Diamonds' : ['dots', 'diamonds'],
'Moss Stitch Parallelograms' : ['diamonds', 'diagonals', 'dots'],
'Parallelograms' : ['squares'],
'Parallelograms II' : ['triangles'],
'Pavilion' : ['lines', 'triangles'],
'Pique Triangles' : ['lines', 'triangles'],
'Plain Diamonds' : ['diamonds'],
'Purled Ladder' : ['lines', 'squares'],
'Rice Stitch' : ['stars', 'dots'],
'Seed Rib' : ['lines', 'dots'],
'Seed Stitch' : ['dots'],
'Single Chevron' : ['triangles'],
'Spaced Checks' : ['squares'],
'Squares In Squares' : ['squares', 'squares'],
'Thermal Underwear Stitch' : ['dots', 'lines'],
'Triangle Ribs' : ['triangles', 'lines'],
'Triangle Squares' : ['lines', 'squares'],
'Triangles' : ['triangles'],
'Twin Rib' : ['lines'],
'Two By Two Rib' : ['lines'],
'Windmill' : ['windmill'],
'Woven Stitch' : ['squares'],
'Brioche Rib' : ['lines'],
'Condo Stitch' : ['holes'],
'Fisherman\'s Rib' : ['loopy', 'lines'],
'Garter And Loops' : ['lines', 'holes', 'dots', 'squares', 'triangles', 'stringy'],
'Layette' : ['lines', 'holes', 'wavy'],
'Open Work Garter Ridges' : ['lines', 'holes', 'messy', 'squares'],
'Roman Stripe' : ['holes', 'stars', 'triangles', 'lines'],
'Seafoam Stitch' : ['holes', 'diamonds', 'stringy'],
'Butterfly' : ['holes', 'butterflies', 'tree'],
'Crossed Throw' : ['lines', 'squares'],
'Diagonal Eyelets' : ['holes', 'lines', 'diagonals'],
'Eyelet Squares' : ['holes', 'squares'],
'Garland' : ['lines', 'holes', 'messy'],
'Garter Eyelet' : ['lines', 'holes', 'dots'],
'Garter Lace' : ['lines', 'stars'],
'Lace Ribbing' : ['lines', 'stars', 'tree'],
'Lacy Lattice' : ['holes', 'messy', 'tree'],
'Ladder Rib' : ['lines', 'stringy'],
'Little Shell' : ['lines', 'holes', 'wavy', 'lines'],
'Open Honeycomb' : ['lines', 'holes', 'stars', 'twisty'],
'Open Twisted Rib' : ['lines', 'circles', 'holes'],
'Pillar Openwork' : ['stringy', 'holes', 'diagonals'],
'Purl Barred Scallop I' : ['triangles', 'lines', 'lines'],
'Purl Barred Scallop II' : ['triangles', 'lines', 'lines', 'holes'],
'Shell Lace' : ['holes', 'wavy', 'triangles'],
'Star Rib Mesh' : ['stars', 'holes'],
'Triple Chevron' : ['holes', 'triangles'],
'Two Color Star' : ['stars'],
'Veil Stitch' : ['loopy'],
'Zig Zag Lace' : ['holes', 'wavy', 'lines'],
'Abstract' : ['messy'],
'Lattice' : ['dots', 'diamonds', 'squares'],
'Pyramid' : ['triangles', 'squares'],
'Zig Zag' : ['squares', 'dots', 'lines'],
'Afghan Stitch' : ['wavy', 'lines'],
'Two Color Basketweave' : ['wavy', 'triangles'],
'Chevron Stripes' : ['wavy', 'triangles'],
'Diamond Check' : ['diamonds'],
'Dots And Dashes' : ['dots', 'lines'],
'Dots Within Stripes' : ['dots', 'lines'],
'Flame Stitch' : ['diagonals', 'lines'],
'Linked Stripe' : ['wavy', 'dots'],
'Swiss Check' : ['stars'],
'Triangle Check' : ['triangles'],
'Two Color Lattice' : ['diamonds'],
'Two Stitch Check' : ['squares'],
'Welted Fantastic' : ['wavy', 'lines'],
'Bee Stitch' : ['wavy', 'messy'],
'Blanket Moss Stitch' : ['dots', 'squares'],
'Chevron & Feather' : ['lines', 'holes', 'angles'],
'Crossed Throw' : ['squares', 'lines', 'holes'],
'Daisy Stitch' : ['stars'],
'Double Mock Rib' : ['lines', 'lines'],
'Double Stockinette' : ['lines'],
'Double Lattice' : ['triangles', 'lines', 'angles'],
'Gingham' : ['squares', 'dots'],
'Hunter\'s Stitch' : ['lines', 'holes', 'loopy'],
'Knit Lattice' : ['diamonds'],
'Knot Stitch' : ['dots'],
'Knotted Rib' : ['stringy', 'lines', 'angles'],
'Linen Stitch' : ['dots'],
'Little Butterfly' : ['stars'],
'Mock Honeycomb' : ['triangles'],
'Plaited Basket Stitch' : ['angles', 'dots'],
'Puff Rib' : ['twisty', 'angles'],
'Quilted Lattice' : ['diamonds', 'stars'],
'Ridges' : ['lines'],
'Rose Stitch' : ['stars', 'holes'],
'Royal Quilting' : ['diamonds', 'dots', 'stringy'],
'Slip Stitch Honeycomb' : ['wavy', 'circles'],
'Trellis Stitch' : ['diamonds', 'triangles'],
'Trinity Stitch' : ['dots', 'circles'],
'Waffle Seed Stitch' : ['messy', 'dots'],
'Waterfall' : ['angles', 'holes', 'lines'],
'Woven Herringbone' : ['triangles', 'angles'],
'6/6 Cable' : ['twisty'],
'6/8 Cable' : ['twisty'],
'8/10 Cable' : ['twisty'],
'Bobble Tree' : ['tree', 'circles'],
'Cabled Feather' : ['wavy', 'feathered'],
'Criss Cross Cable With Twists' : ['twisty', 'twisty'],
'Eccentric Cable' : ['twisty'],
'Eccentric Cable II' : ['twisty', 'squares'],
'Twisted Braided Cable' : ['diamonds', 'twisty'],
'Wave Lattice' : ['wavy', 'weavy'],
'Knit' : ['lines'],
'Purl' : ['dots']}