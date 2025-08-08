# tsp_solver.py
import pandas as pd
from main import gmaps

def get_distance_matrix(places):
    attractions = [p['name'] for p in places]
    # Add "Vancouver BC" to each location for better accuracy
    locations = [place + ", Vancouver BC" for place in attractions]
    # Create a square DataFrame for the duration matrix
    n = len(attractions)
    duration_matrix = pd.DataFrame(index=attractions, columns=attractions)

    # Query duration between each pair of places
    for i in range(n):
        for j in range(n):
            if j <= i:
                if i == j:
                    duration_matrix.iloc[i, j] = -1
                continue
            try:
                result = gmaps.directions(locations[i], locations[j])
                duration = result[0]['legs'][0]['duration']['value']  # Get Second
                if duration < 60:
                    duration = 1  # Make sure no 0 min
                else:
                    duration = round(duration / 60)  # Change to minute
                duration_matrix.iloc[i, j] = duration
                duration_matrix.iloc[j, i] = duration  # symmetric fill
            except Exception as e:
                print(f"Error: {attractions[i]} to {attractions[j]} - {e}")
                duration_matrix.iloc[i, j] = "Error"
    return duration_matrix


def tsp(matrix, start):
    attractions = matrix.index.tolist()  # List of all attraction names
    remaining_attractions = attractions.copy()
    current_location = start
    tour = [current_location]
    remaining_attractions.remove(current_location)

    while remaining_attractions:
        # Find the closest attraction
        closest_attraction = None
        min_duration = float('inf')

        for attraction in remaining_attractions:
            duration = matrix.loc[current_location, attraction]
            if duration < min_duration:
                min_duration = duration
                closest_attraction = attraction

        # Add the closest attraction to the tour
        tour.append(closest_attraction)

        # Update the current location and remove the visited attraction
        current_location = closest_attraction
        remaining_attractions.remove(closest_attraction)

    # Add the return trip to the starting point (optional)
    tour.append(start)

    return tour


def get_route_url(tour):
    # Generate the base URL for Google Maps directions
    base_url = "https://www.google.com/maps/dir/?api=1"

    # The first point is the origin, and the last point is the destination
    origin = tour[0]
    destination = tour[-1]

    # Generate waypoints by joining the intermediate attractions
    waypoints = '|'.join(tour[1:-1])  # Remove the origin and destination from waypoints

    # Construct the full URL
    if waypoints:
        url = f"{base_url}&origin={origin}&destination={destination}&waypoints={waypoints}"
    else:
        url = f"{base_url}&origin={origin}&destination={destination}"
    return url
