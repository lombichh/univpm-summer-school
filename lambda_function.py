import datetime, pyeto, urllib3, json


def get_data(url):
    # returns the response text from a get request
    http = urllib3.PoolManager()

    r = http.request("GET", url)

    return json.loads(r.data)


def calculate_eto(lat_deg, t_max, t_min, t_avg, date=datetime.datetime.now()):
    # calculate eto given latitude, temperature and date
    lat_rad = pyeto.deg2rad(lat_deg)
    day_of_year = datetime.date(date.year, date.month, date.day).timetuple().tm_yday

    sol_dec = pyeto.sol_dec(day_of_year)
    sha = pyeto.sunset_hour_angle(lat_rad, sol_dec)
    ird = pyeto.inv_rel_dist_earth_sun(day_of_year)
    et_rad = pyeto.et_rad(lat_rad, sol_dec, sha, ird)

    res = pyeto.hargreaves(23, 34, 27, et_rad)
    return res

def lambda_handler(event, context):
    
    # get fields and crop json from s3
    fields = get_data("https://forecast-et.s3.eu-central-1.amazonaws.com/fields.json")
    crop = get_data("https://forecast-et.s3.eu-central-1.amazonaws.com/crop.json")
    
    # get field_num and days from the body of the post request
    field_num = event["field_num"]
    days = event["days"]
    
    # get chosen field
    field = fields[str(field_num)]
    
    # get latitude and longitude of chosen field
    lat = field["lat"]
    lon = field["lon"]
    
    # get weather forecast using openweathermap api
    weather_forecast = get_data(
        "https://api.openweathermap.org/data/2.5/onecall?lat="
        + str(lat)
        + "&lon="
        + str(lon)
        + "&exclude=minutely,hourly&appid=f363c66492ed166783b1304cc814a105"
    )
    
    # calculate eto
    day_forecast = weather_forecast["daily"][days - 1]
    eto_forecast = calculate_eto(
        lat,
        day_forecast["temp"]["max"],
        day_forecast["temp"]["min"],
        day_forecast["temp"]["eve"],
        datetime.datetime.fromtimestamp(day_forecast["dt"]),
    )
    
    # get kc of the given day
    timestamp_forecast = weather_forecast["daily"][days]["dt"]
    day_from_seeding = int((timestamp_forecast - field["seedingDate"]) / 86400)
    
    kc_forecast = crop[field["crop"]]["coefficients"][day_from_seeding]
    
    # calculate etc
    etc_forecast = eto_forecast * kc_forecast
    
    return {
        'statusCode': 200,
        'body': etc_forecast
    }