import unittest

from pyzbar.locations import bounding_box, convex_hull, Rect


class TestLocations(unittest.TestCase):
    def test_bounding_box(self):
        self.assertRaises(ValueError, bounding_box, [])
        self.assertEqual(
            Rect(left=0, top=0, width=0, height=0),
            bounding_box([(0, 0)])
        )
        self.assertEqual(
            Rect(left=37, top=550, width=324, height=76),
            bounding_box([(37, 551), (37, 625), (361, 626), (361, 550)])
        )

    def test_convex_hull_empty(self):
        self.assertEqual([], convex_hull([]))

    def test_convex_square(self):
        points = [(0, 0), (0, 1), (1, 1), (1, 0)]
        self.assertEqual(points, convex_hull(points)),

    def test_convex_duplicates(self):
        points = [(0, 0), (0, 1), (1, 1), (1, 0)]
        self.assertEqual(points, convex_hull(points * 10)),

    def test_other(self):
        # Taken from
        # https://codegolf.stackexchange.com/questions/11035/find-the-convex-hull-of-a-set-of-2d-points
        res = convex_hull([(1, 1), (2, 2), (3, 3), (1, 3)])
        self.assertEqual([(1, 1), (1, 3), (3, 3)], res)

        res = convex_hull([
            (4.4, 14), (6.7, 15.25), (6.9, 12.8), (2.1, 11.1), (9.5, 14.9),
            (13.2, 11.9), (10.3, 12.3), (6.8, 9.5), (3.3, 7.7), (0.6, 5.1),
            (5.3, 2.4), (8.45, 4.7), (11.5, 9.6), (13.8, 7.3), (12.9, 3.1),
            (11, 1.1)
        ])

        expected = [
            (0.6, 5.1), (2.1, 11.1), (4.4, 14), (6.7, 15.25), (9.5, 14.9),
            (13.2, 11.9), (13.8, 7.3), (12.9, 3.1), (11, 1.1), (5.3, 2.4)
        ]
        self.assertEqual(expected, res)


if __name__ == '__main__':
    unittest.main()
