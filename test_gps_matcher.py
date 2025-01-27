import unittest
from geo_point_matcher import haversine_distance, match_closest_points

class TestGPSMatcher(unittest.TestCase):
    def test_haversine_distance(self):
        # Test with known values
        self.assertAlmostEqual(haversine_distance(0, 0, 0, 0), 0.0, places=5)
        self.assertAlmostEqual(haversine_distance(0, 0, 0, 90), 10007.543, places=3)
        self.assertAlmostEqual(haversine_distance(37.7749, -122.4194, 34.0522, -118.2437), 559.120, places=3)

    def test_match_closest_points_basic(self):
        array1 = [(37.7749, -122.4194), (34.0522, -118.2437)]
        array2 = [(40.7128, -74.0060), (36.1699, -115.1398)]
        expected_matches = [
            ((37.7749, -122.4194), (36.1699, -115.1398)),
            ((34.0522, -118.2437), (36.1699, -115.1398))
        ]
        self.assertEqual(match_closest_points(array1, array2), expected_matches)

    def test_match_closest_points_edge_case(self):
        # Test empty arrays
        array1 = []
        array2 = []
        self.assertEqual(match_closest_points(array1, array2), [])

        # Test one empty array
        array1 = [(37.7749, -122.4194)]
        array2 = []
        self.assertEqual(match_closest_points(array1, array2), [])

    def test_haversine_large_distance(self):
        # Test distance between two far points
        self.assertAlmostEqual(
            haversine_distance(-90, 0, 90, 0),
            20015.086,  # Approx. half of Earth's circumference
            places=3
        )

if __name__ == "__main__":
    unittest.main()
