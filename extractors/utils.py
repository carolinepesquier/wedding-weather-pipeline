from geopy.geocoders import Nominatim

def get_location_name(coordinates):

    # Find the location name from coordinates:
    geolocator = Nominatim(user_agent="wedding_weather_pipeline")
    location = geolocator.reverse(f"{coordinates[0]}, {coordinates[1]}")
    raw = location.raw['address']
    location_name = (
        raw.get('suburb') or 
        raw.get('town') or 
        raw.get('city') or 
        raw.get('village') or 
        f"{coordinates[0]:.4f},{coordinates[1]:.4f}"  # fallback to coordinates as string
    )

    return location_name

# Test:
if __name__ == "__main__":
    wedding_place = (51.5540, 0.2520, 22)
    location_name = get_location_name(wedding_place)
    print(location_name)