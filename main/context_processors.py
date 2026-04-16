import json
import urllib.request
from datetime import datetime
from .models import Category

def global_context(request):
    categories = Category.objects.all()
    
    # Havo harorati uchun (Farg'ona, O'zbekiston)
    temp_c = "--"
    weather_icon = "/static/img/weather-icon.png"  # Default
    
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=40.3842&longitude=71.7843&current_weather=true"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())
            temp_c = data.get("current_weather", {}).get("temperature", "--")
            
            # Simplified icon logic based on WMO Weather interpretation codes
            # (0: Clear, 1-3: Cloudy, 45-48: Fog, 51-67: Rain, 71-77: Snow, 95-99: Thunderstorm)
            weather_code = data.get("current_weather", {}).get("weathercode", 0)
            if weather_code == 0:
                weather_icon = "/static/img/sun.png" # Need to ensure these exist or fallback
            elif 1 <= weather_code <= 3:
                weather_icon = "/static/img/cloud.png"
            elif 51 <= weather_code <= 67:
                weather_icon = "/static/img/rain.png"
            elif 71 <= weather_code <= 77:
                weather_icon = "/static/img/snow.png"
    except Exception:
        pass # Fallback to default if API fails

    return {
        'categories': categories,
        'temp_c': temp_c,
        'weather_icon': weather_icon,
        'today': datetime.today(),
    }
