from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_KEY = 'c898ebd1ac4831f9bc3cb036e2b382d4'

def generate_packing_list(temp, weather_desc):
    items = []
    
    # Temperature based logic
    if temp < 10:
        items.extend(["🥶 Heavy Winter Coat", "🧤 Thermal Gloves", "🧣 Warm Scarf", "🧦 Thick Wool Socks"])
    elif 10 <= temp <= 22:
        items.extend(["🧥 Light Jacket or Sweater", "👖 Comfortable Jeans", "👕 Long-sleeve shirts"])
    else:
        items.extend(["😎 Sunglasses", "🧴 Sunscreen", "🩳 Shorts or Light Skirts", "👕 Short-sleeve T-shirts"])

    # Weather condition based logic
    if 'rain' in weather_desc.lower() or 'drizzle' in weather_desc.lower():
        items.extend(["☔ Sturdy Umbrella", "👢 Waterproof Shoes", "🧥 Raincoat"])
    if 'snow' in weather_desc.lower():
        items.extend(["❄️ Snow Boots", "🏂 Thermal Innerwear"])
    if 'clear' in weather_desc.lower() and temp > 15:
        items.extend(["🧢 Baseball Cap or Sun Hat"])

    return items

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_info = None
    packing_list = None
    error_message = None

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    temp = int(data['main']['temp'])
                    desc = data['weather'][0]['description']
                    
                    weather_info = {
                        'location': f"{data['name']}, {data['sys']['country']}",
                        'temp': temp,
                        'description': desc.title()
                    }
                    
                    # Call our custom python function to get recommendations
                    packing_list = generate_packing_list(temp, desc)
                else:
                    error_message = "Destination not found. Please try another city."
            except Exception:
                error_message = "Network connection failed."
                
    return render_template('index.html', weather=weather_info, items=packing_list, error=error_message)

if __name__ == '__main__':
    app.run(debug=True)