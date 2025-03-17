import sys
import requests
from datetime import datetime, timezone
import pytz

def get_timezone(lat, lon):
    try:
        url = f'https://www.timeapi.io/api/timezone/coordinate?latitude={lat}&longitude={lon}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['timeZone']
        raise Exception("Timezone not found.")
    except Exception as e:
        # Handle exceptions and print error messages
        print(f"Error calling the free API please retry: {e}")

def get_sun_times(lat, lon):
    try:
        # Construct the API URL with the given latitude and longitude
        url = f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&formatted=0'

        # Make the GET request to the API to get sunrise and sunset times
        response = requests.get(url)

        # Parse the JSON response
        data = response.json()

        # Return the sunrise and sunset times
        return data['results']['sunrise'], data['results']['sunset'], data['results']['solar_noon'], data['results']['civil_twilight_end']

    except Exception as e:
        # Handle exceptions and print error messages
        print(f"Error calling the free API please retry: {e}")

def determine_time_of_day(current_utc, sunrise_utc, sunset_utc, solar_noon_utc, civil_twilight_end_utc):
    # Check if the current time is equal sunrise
    if current_utc == sunrise_utc:
        return 'sunrise.png'

    # Check if the current time is equal sunset
    if current_utc == sunset_utc:
        return 'sunset.png'

    # Determine if it's morning (starts at sunrise, ends around solar noon)
    if current_utc >= sunrise_utc and current_utc < solar_noon_utc:
        return 'morning.png'

    # Determine if it's afternoon (starts after solar noon, ends around sunset)
    if current_utc > solar_noon_utc and current_utc < sunset_utc:
        return 'noon.png'

    # Determine if it's evening (starts after sunset, ends at the end of civil twilight)
    if current_utc > sunset_utc and current_utc <= civil_twilight_end_utc:
        return 'evening.png'

    # Determine if it's night (starts after civil twilight, ends around sunrise)
    if current_utc > civil_twilight_end_utc or current_utc < sunrise_utc:
        return 'night.png'

def main():
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python wallpaper.py <latitude> <longitude>")
        return

    # Read latitude and longitude from command-line arguments
    latitude = sys.argv[1]
    longitude = sys.argv[2]

    try:
        # Get the sunrise and sunset times from the API
        sunrise_str, sunset_str, solar_noon_str, civil_twilight_str = get_sun_times(latitude, longitude)

        # Convert the ISO format strings to datetime objects in UTC
        sunrise_utc = datetime.fromisoformat(sunrise_str.replace('Z', '+00:00'))
        sunset_utc = datetime.fromisoformat(sunset_str.replace('Z', '+00:00'))
        solar_noon_utc = datetime.fromisoformat(solar_noon_str.replace('Z', '+00:00'))
        civil_twilight_end_utc = datetime.fromisoformat(civil_twilight_str.replace('Z', '+00:00'))

        # Get local timezone based on coordinates
        tz_str = get_timezone(latitude, longitude)
        tz = pytz.timezone(tz_str)

        # Convert UTC times to local timezone
        sunrise_local = sunrise_utc.astimezone(tz)
        sunset_local = sunset_utc.astimezone(tz)
        solar_noon_local = solar_noon_utc.astimezone(tz)
        civil_twilight_end_local = civil_twilight_end_utc.astimezone(tz)
        
        # Get the current UTC time
        current_utc = datetime.now(timezone.utc)
        print(current_utc)
        current_local = current_utc.astimezone(tz)
        print(current_local)

        # Determine the appropriate wallpaper based on the current time
        wallpaper = determine_time_of_day(current_local, sunrise_local, sunset_local, solar_noon_local, civil_twilight_end_local)

        # Output the selected wallpaper filename
        print(wallpaper)

    except Exception as e:
        # Handle exceptions and print error messages
        print(f"Error: {e}")

# Entry point for the script
if __name__ == "__main__":
    main()
