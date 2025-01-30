import math
import csv
import re

def dms_to_decimal(degrees, minutes, seconds, direction):
    """
    Convert degrees, minutes, and seconds (DMS) to decimal degrees (DD).
    
    Parameters:
    degrees (float): The degrees part
    minutes (float): The minutes part
    seconds (float): The seconds part
    direction (str): 'N', 'S', 'E', 'W' to indicate hemisphere

    Returns:
    float: The decimal degree representation
    """
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if direction in ['S', 'W']:
        decimal *= -1
    return decimal

def parse_coordinate(value):
    """
    Parses latitude or longitude input in decimal degrees (DD) or degrees, minutes, seconds (DMS).
    
    Parameters:
    value (str or float): The coordinate to be parsed

    Returns:
    float: Decimal degrees representation of the coordinate
    """
    try:
        # Check if already in decimal format
        return float(value)
    except ValueError:
        # Try parsing DMS format
        match = re.match(r"(\d+)°\s*(\d+)'?\s*(\d+\.?\d*)\"?\s*([NSEW])", value.strip(), re.IGNORECASE)
        if match:
            degrees, minutes, seconds, direction = match.groups()
            return dms_to_decimal(float(degrees), float(minutes), float(seconds), direction.upper())
        else:
            raise ValueError(f"Invalid coordinate format: {value}")

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth's surface.
    Uses the Haversine formula.

    Parameters:
    lat1, lon1: Latitude and Longitude of the first point in decimal degrees
    lat2, lon2: Latitude and Longitude of the second point in decimal degrees

    Returns:
    Distance in kilometers between the two points
    """
    R = 6371.0  # Radius of the Earth in kilometers

    # Convert latitude and longitude from degrees to radians
    lat1_rad, lon1_rad = map(math.radians, [lat1, lon1])
    lat2_rad, lon2_rad = map(math.radians, [lat2, lon2])

    # Differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Distance in kilometers

def match_closest_points(array1, array2):
    """
    Match each point in array1 to the closest point in array2 based on GPS coordinates.

    Parameters:
    array1: List of tuples containing (latitude, longitude)
    array2: List of tuples containing (latitude, longitude)

    Returns:
    List of tuples where each tuple is (point_from_array1, closest_point_from_array2)
    """
    if not array2:
        return [(point1, None) for point1 in array1]  # Return None for unmatched points

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

def load_csv(filepath):
    """
    Load latitude and longitude points from a CSV file.

    Parameters:
    filepath (str): Path to the CSV file

    Returns:
    List of tuples: [(lat1, lon1), (lat2, lon2), ...]
    """
    coordinates = []
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header if present
            for row in reader:
                if len(row) >= 2:
                    try:
                        lat = parse_coordinate(row[0])
                        lon = parse_coordinate(row[1])
                        coordinates.append((lat, lon))
                    except ValueError as e:
                        print(f"Skipping invalid row: {row} - {e}")
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
    return coordinates

if __name__ == "__main__":
    # Example usage with direct input
    array1 = [(37.7749, -122.4194), "34°3'8\"N, 118°14'37\"W"]
    array2 = [(40.7128, -74.0060), "36°10'11\"N, 115°8'23\"W"]

    # Convert all input coordinates to decimal degrees
    array1 = [(parse_coordinate(lat), parse_coordinate(lon)) if isinstance(lat, str) else (lat, lon) for lat, lon in array1]
    array2 = [(parse_coordinate(lat), parse_coordinate(lon)) if isinstance(lat, str) else (lat, lon) for lat, lon in array2]

    matches = match_closest_points(array1, array2)
    for match in matches:
        print(f"Point {match[0]} is closest to {match[1]}")

    # Example usage with CSV files
    file1 = "data1.csv"  # Replace with actual path
    file2 = "data2.csv"  # Replace with actual path

    csv_array1 = load_csv(file1)
    csv_array2 = load_csv(file2)

    if csv_array1 and csv_array2:
        csv_matches = match_closest_points(csv_array1, csv_array2)
        for match in csv_matches:
            print(f"Point {match[0]} is closest to {match[1]}")
