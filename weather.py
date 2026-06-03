# Execute this statement.
import logging
# Import os.
import os
from pathlib import Path
# Import requests.
import requests

# Import APP_NAME from core.
from core import APP_NAME

def _load_local_env() -> None:
    env_path = Path(__file__).resolve().parent / '.env'
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_local_env()

# OpenWeather API key must be provided through the environment in production.
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')

# Set LOGGER.
LOGGER = logging.getLogger(APP_NAME)

# Set _DEFAULT_HEADERS.
_DEFAULT_HEADERS = {'User-Agent': 'AgriYieldAI/1.0'}


# Define function _get_json.
def _get_json(url: str) -> dict:
    # Set resp.
    resp = requests.get(url, timeout=8, headers=_DEFAULT_HEADERS)
    # Check condition and run block if true.
    if resp.status_code != 200:
        # Raise an exception.
        raise RuntimeError(f'Location provider error: {resp.status_code} {resp.text}')
    # Return the computed value.
    return resp.json()


# Define function _format_location.
def _format_location(
    # Execute this statement.
    city: str | None,
    # Execute this statement.
    region: str | None,
    # Execute this statement.
    country_code: str | None,
    # Execute this statement.
    country_name: str | None
# Execute this statement.
) -> str | None:
    # Check condition and run block if true.
    if not city:
        # Return the computed value.
        return None
    # Check condition and run block if true.
    if country_code:
        # Return the computed value.
        return f'{city},{country_code}'
    # Check condition and run block if true.
    if country_name:
        # Return the computed value.
        return f'{city},{country_name}'
    # Check condition and run block if true.
    if region:
        # Return the computed value.
        return f'{city},{region}'
    # Return the computed value.
    return city


# Define function fetch_weather.
def fetch_weather(city: str) -> dict:
    # Set api_key.
    api_key = OPENWEATHER_API_KEY or os.getenv('OPENWEATHER_API_KEY')
    # Check condition and run block if true.
    if not api_key:
        # Raise an exception.
        raise RuntimeError('OpenWeather API key is not set.')

    # Set url.
    url = 'https://api.openweathermap.org/data/2.5/weather'
    # Set params.
    params = {
        # Execute this statement.
        'q': city,
        # Execute this statement.
        'appid': api_key,
        # Execute this statement.
        'units': 'metric'
    # Close the previous block or structure.
    }
    # Set resp.
    resp = requests.get(url, params=params, timeout=10)
    # Check condition and run block if true.
    if resp.status_code != 200:
        # Raise an exception.
        raise RuntimeError(f'Weather API error: {resp.status_code} {resp.text}')

    # Set data.
    data = resp.json()
    # Set temp_c.
    temp_c = float(data['main']['temp'])
    # Set humidity.
    humidity = float(data['main']['humidity'])
    # Set feels_like.
    feels_like = float(data['main'].get('feels_like', temp_c))
    # Set pressure.
    pressure = float(data['main'].get('pressure', 0.0))
    # Set wind_speed.
    wind_speed = float(data.get('wind', {}).get('speed', 0.0))
    # Set clouds.
    clouds = float(data.get('clouds', {}).get('all', 0.0))
    # Set country.
    country = data.get('sys', {}).get('country')

    # Set rainfall.
    rainfall = 0.0
    # Set rain_source.
    rain_source = 'none'
    # Check condition and run block if true.
    if 'rain' in data:
        # Set rainfall.
        rainfall = data['rain'].get('1h')
        # Check condition and run block if true.
        if rainfall is None:
            # Set rainfall.
            rainfall = data['rain'].get('3h')
        # Set rainfall.
        rainfall = rainfall or 0.0
        # Set rain_source.
        rain_source = 'current'

    # Fallback to short-term forecast if current response has no rain or is dry.
    # Check condition and run block if true.
    if rainfall <= 0.0:
        # Start a protected block for error handling.
        try:
            # Set forecast_url.
            forecast_url = 'https://api.openweathermap.org/data/2.5/forecast'
            # Set forecast.
            forecast = requests.get(forecast_url, params=params, timeout=10)
            # Check condition and run block if true.
            if forecast.status_code == 200:
                # Set fdata.
                fdata = forecast.json()
                # Set upcoming.
                upcoming = (fdata.get('list') or [])[:4]
                # Set total.
                total = 0.0
                # Loop over items in a sequence.
                for item in upcoming:
                    # Set total +.
                    total += float(item.get('rain', {}).get('3h', 0.0) or 0.0)
                # Check condition and run block if true.
                if total > 0.0:
                    # Set rainfall.
                    rainfall = total
                    # Set rain_source.
                    rain_source = 'forecast'
        # Handle an error case.
        except Exception:
            # Set rainfall.
            rainfall = rainfall or 0.0

    # Call LOGGER.info.
    LOGGER.info('Weather fetch ok for %s', city)

    # Return the computed value.
    return {
        # Execute this statement.
        'temperature': temp_c,
        # Execute this statement.
        'humidity': humidity,
        # Execute this statement.
        'rainfall': float(rainfall),
        # Execute this statement.
        'rain_source': rain_source,
        # Execute this statement.
        'feels_like': feels_like,
        # Execute this statement.
        'pressure': pressure,
        # Execute this statement.
        'wind_speed': wind_speed,
        # Execute this statement.
        'clouds': clouds,
        # Execute this statement.
        'resolved_name': data.get('name'),
        # Execute this statement.
        'country': country
    # Close the previous block or structure.
    }


# Define function detect_location.
def detect_location() -> str:
    # Set last_error.
    last_error = None

    # Start a protected block for error handling.
    try:
        # Set data.
        data = _get_json('https://ipapi.co/json/')
        # Set location.
        location = _format_location(
            # Call data.get.
            data.get('city'),
            # Call data.get.
            data.get('region'),
            # Call data.get.
            data.get('country'),
            # Call data.get.
            data.get('country_name')
        # Close the previous block or structure.
        )
        # Check condition and run block if true.
        if location:
            # Return the computed value.
            return location
    # Handle an error case.
    except Exception as e:
        # Set last_error.
        last_error = e

    # Start a protected block for error handling.
    try:
        # Set data.
        data = _get_json('https://ipinfo.io/json')
        # Set location.
        location = _format_location(
            # Call data.get.
            data.get('city'),
            # Call data.get.
            data.get('region'),
            # Call data.get.
            data.get('country'),
            # Execute this statement.
            None
        # Close the previous block or structure.
        )
        # Check condition and run block if true.
        if location:
            # Return the computed value.
            return location
    # Handle an error case.
    except Exception as e:
        # Set last_error.
        last_error = e

    # Start a protected block for error handling.
    try:
        # Set data.
        data = _get_json('http://ip-api.com/json/')
        # Set location.
        location = _format_location(
            # Call data.get.
            data.get('city'),
            # Call data.get.
            data.get('regionName'),
            # Call data.get.
            data.get('countryCode') or data.get('country'),
            # Execute this statement.
            None
        # Close the previous block or structure.
        )
        # Check condition and run block if true.
        if location:
            # Return the computed value.
            return location
    # Handle an error case.
    except Exception as e:
        # Set last_error.
        last_error = e

    # Check condition and run block if true.
    if last_error:
        # Raise an exception.
        raise RuntimeError('Unable to detect location automatically.') from last_error
    # Raise an exception.
    raise RuntimeError('Unable to detect location automatically.')


# Define function search_locations.
def search_locations(query: str, limit: int = 5) -> list[str]:
    # Set api_key.
    api_key = OPENWEATHER_API_KEY or os.getenv('OPENWEATHER_API_KEY')
    # Check condition and run block if true.
    if not api_key:
        # Raise an exception.
        raise RuntimeError('OpenWeather API key is not set.')

    # Set url.
    url = 'https://api.openweathermap.org/geo/1.0/direct'
    # Set params.
    params = {
        # Execute this statement.
        'q': query,
        # Execute this statement.
        'limit': limit,
        # Execute this statement.
        'appid': api_key
    # Close the previous block or structure.
    }
    # Set resp.
    resp = requests.get(url, params=params, timeout=10)
    # Check condition and run block if true.
    if resp.status_code != 200:
        # Raise an exception.
        raise RuntimeError(f'Geocoding error: {resp.status_code} {resp.text}')

    # Set data.
    data = resp.json()
    # Set results.
    results = []
    # Loop over items in a sequence.
    for item in data:
        # Set name.
        name = item.get('name')
        # Set state.
        state = item.get('state')
        # Set country.
        country = item.get('country')
        # Set parts.
        parts = [p for p in [name, state, country] if p]
        # Check condition and run block if true.
        if parts:
            # Call results.append.
            results.append(', '.join(parts))
    # Return the computed value.
    return results
