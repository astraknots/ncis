from unittest import TestCase
import astrology_aspects as aspects
import astrology_planets as planets


class TestAspects(TestCase):
    def test_get_aspect_orb(self):
        # Test a big three planet in aspect where big three orb is bigger
        self.assertEqual(aspects.get_aspect_orb(aspects.square, planets.sun), aspects.Aspect.BIG_THREE_ORB)
        self.assertEqual(aspects.get_aspect_orb(aspects.sextile, planets.moon), aspects.Aspect.BIG_THREE_ORB)
        # Test a big three planet in aspect where aspect orb is bigger
        self.assertEqual(aspects.get_aspect_orb(aspects.conj, planets.asc), aspects.conj.orb)
        self.assertEqual(aspects.get_aspect_orb(aspects.opposition, planets.sun), aspects.opposition.orb)
        # Test non-big three orb
        self.assertEqual(aspects.get_aspect_orb(aspects.conj, planets.mars), aspects.conj.orb)
        self.assertEqual(aspects.get_aspect_orb(aspects.square, planets.mars), aspects.square.orb)
        self.assertEqual(aspects.get_aspect_orb(aspects.sextile, planets.saturn), aspects.sextile.orb)
        self.assertEqual(aspects.get_aspect_orb(aspects.opposition, planets.neptune), aspects.opposition.orb)

    def test_adjust_degree_for_360(self):
        self.assertEqual(aspects.adjust_degree_for_360(10), 10)
        self.assertEqual(aspects.adjust_degree_for_360(-260), 100)
        self.assertEqual(aspects.adjust_degree_for_360(460), 100)

    def test_is_degree_in_range(self):
        self.assertEqual(aspects.is_degree_in_range(10, (1, 15)), True)
        self.assertEqual(aspects.is_degree_in_range(10, (1, 9)), False)
        self.assertEqual(aspects.is_degree_in_range(10, (1, 10)), True)
        self.assertEqual(aspects.is_degree_in_range(1, (1, 10)), True)
        self.assertEqual(aspects.is_degree_in_range(19, (1, 9)), False)