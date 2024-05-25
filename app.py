import json
import urllib.parse

from flask import Flask, render_template, request, abort, Response, redirect, url_for

#api.openweathermap.org/data/2.5/forecast?q={city name}&appid={API key}


app = Flask(__name__)
APPID = '420615314e7863288d189898845f7330'


@app.route('/', methods=['POST', 'GET'])
def form_input():
    if request.method == 'POST':
        city = request.form.get('city')
        print(city)
        return redirect(url_for('get_weather', city=city))
    return render_template('form.html')


@app.route('/forecast', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if city is None:
        abort(400, "Missing argument city")

    url = 'https://api.openweathermap.org/data/2.5/weather'
    src = urllib.request.urlopen(url + '?q=' + city + '&appid=' + APPID).read()
    list_of_data = json.loads(src)

    data = {
        "country_code": str(list_of_data['sys']['country']),
        "city": str(list_of_data['name']),
        "temp": str(round(float(list_of_data['main']['temp']) - 273.15, 2)) + '°C',
        "pressure": str(list_of_data['main']['pressure']),
        "humidity": str(list_of_data['main']['humidity']),
    }
    print(data)
    return render_template('index.html', title='weather app', data=data)


if __name__ == '__main__':
    app.run(debug=True)
