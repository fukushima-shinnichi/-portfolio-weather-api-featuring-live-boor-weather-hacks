import requests
from bottle import route, run, template, static_file, url, request

def weather_api(choice_city_id, date_id):
	base_url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city='
	cityID = choice_city_id
	url = '{}{}'.format(base_url, cityID)
	r = requests.get(url)
	weather_data = r.json()

	date_ID = int(date_id)

	def select_date_func(date_ID):
		if date_ID == 0:
			location = weather_data['location']['city']
			#day = weather_data['forecasts'][date_ID]['dateLabel']
			day = 'Today'
			date = weather_data['forecasts'][date_ID]['date']
			weather = weather_data['forecasts'][date_ID]['telop']
			max_temperature = weather_data['forecasts'][date_ID]['temperature']['max']
			min_temperature = weather_data['forecasts'][date_ID]['temperature']['min']
			image = weather_data['forecasts'][date_ID]['image']['url']

			weather_arry = [location, day, date, weather, max_temperature, min_temperature, image]

		elif date_ID == 1:
			location = weather_data['location']['city']
			#day = weather_data['forecasts'][date_ID]['dateLabel']
			day = 'Tomorrow'
			date = weather_data['forecasts'][date_ID]['date']
			weather = weather_data['forecasts'][date_ID]['telop']
			max_temperature = weather_data['forecasts'][date_ID]['temperature']['max']['celsius']
			min_temperature = weather_data['forecasts'][date_ID]['temperature']['min']['celsius']
			image = weather_data['forecasts'][date_ID]['image']['url']

			weather_arry = [location, day, date, weather, max_temperature, min_temperature, image]

		elif date_ID == 2:
			location = weather_data['location']['city']
			#day = weather_data['forecasts'][date_ID]['dateLabel']
			day = 'Day after tomorrow'
			date = weather_data['forecasts'][date_ID]['date']
			weather = weather_data['forecasts'][date_ID]['telop']
			max_temperature = weather_data['forecasts'][date_ID]['temperature']['max']
			min_temperature = weather_data['forecasts'][date_ID]['temperature']['min']
			image = weather_data['forecasts'][date_ID]['image']['url']

			weather_arry = [location, day, date, weather, max_temperature, min_temperature, image]
		
		return weather_arry
	
	weather_arry = select_date_func(date_ID)

	return weather_arry


@route('/')
def web_html():
	weather_arry = weather_api(130010, 0)
	location = weather_arry[0]
	day = weather_arry[1]
	date = weather_arry[2]
	weather = weather_arry[3]
	max_temperature = weather_arry[4]
	min_temperature = weather_arry[5]
	image_src = weather_arry[6]
	return template('weather_template', location=location, day=day, date=date, weather=weather, image_src=image_src, max_temperature=max_temperature, min_temperature=min_temperature, url=url)

@route('/static/<filepath:path>', name='static_file')
def static(filepath):
    return static_file(filepath, root='./static')

@route('/', method='POST')
def web_api_result_func():
	choice_city_id = request.forms.form_place
	date_id = request.forms.form_date
	weather_arry = weather_api(choice_city_id, date_id)
	location = weather_arry[0]
	day = weather_arry[1]
	date = weather_arry[2]
	weather = weather_arry[3]
	max_temperature = weather_arry[4]
	min_temperature = weather_arry[5]
	image_src = weather_arry[6]
	return template('weather_template', location=location, day=day, date=date, weather=weather, image_src=image_src, max_temperature=max_temperature, min_temperature=min_temperature, url=url)

run(host='localhost', port=8080, debug=True)

