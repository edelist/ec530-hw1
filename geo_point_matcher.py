import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth's surface.
    The formula is based on the Haversine formula.

    Parameters:
    lat1, lon1: Latitude and Longitude of the first point in decimal degrees
    lat2, lon2: Latitude and Longitude of the second point in decimal degrees

    Returns:
    Distance in kilometers between the two points
    """
    R = 6371.0  # Radius of the Earth in kilometers

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance

def match_closest_points(array1, array2):
    """
    Match each point in the first array to the closest point in the second array based on GPS coordinates.

    Parameters:
    array1: List of tuples containing latitude and longitude [(lat1, lon1), (lat2, lon2), ...]
    array2: List of tuples containing latitude and longitude [(lat1, lon1), (lat2, lon2), ...]

    Returns:
    List of tuples where each tuple is (point_from_array1, closest_point_from_array2)
    """
    matches = []

    for point1 in array1:
        lat1, lon1 = point1
        closest_point = None
        min_distance = float('inf')

        for point2 in array2:
            lat2, lon2 = point2
            distance = haversine_distance(lat1, lon1, lat2, lon2)

            if distance < min_distance:
                min_distance = distance
                closest_point = point2

        matches.append((point1, closest_point))

    return matches

# Example usage
if __name__ == "__main__":
    array1 = [(37.7749, -122.4194), (34.0522, -118.2437)]  # Example array 1 (San Francisco, Los Angeles)
    array2 = [(40.7128, -74.0060), (36.1699, -115.1398)]  # Example array 2 (New York, Las Vegas)

    matches = match_closest_points(array1, array2)
    for match in matches:
        print(f"Point {match[0]} is closest to {match[1]}")