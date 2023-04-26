from db_stuff import station_by_name, get_last_weather, get_all_weather
from flask import Flask, render_template, jsonify, request
import datetime
import random
import sys

app = Flask(__name__)


HOME_STATION: dict = station_by_name("HomeStation")


def month_from_date(month: int) -> str:
    """
    :param month: month number
    :return: month string
    """
    return [
        "",
        "Januar",
        "Februar",
        "März",
        "April",
        "Mai",
        "Juni",
        "Juli",
        "August",
        "September",
        "Oktober",
        "November",
        "Dezember",
    ][month]


def day_from_date(day: int) -> str:
    """
    :param day: day number
    :return: day string
    """
    return [
        "Montag",
        "Dienstag",
        "Mittwoch",
        "Donnerstag",
        "Freitag",
        "Samstag",
        "Sonntag",
    ][day]


@app.route('/')
def index():
    data = get_last_weather(HOME_STATION["id"])

    t = data["time"]

    date, time = t.split("-")
    year, month, day = date.split(".")
    weekday = datetime.datetime(int(year), int(month), int(day)).weekday()

    data["ftime"] = f"{time[:-3]}, {day_from_date(weekday)}, {day}. {month_from_date(int(month))} {year}"

    return render_template("index.html", data=data, station_data=HOME_STATION)


@app.route('/current_data')
def current_data():
    data = get_last_weather(HOME_STATION["id"])

    t = data["time"]

    date, time = t.split("-")
    year, month, day = date.split(".")
    weekday = datetime.datetime(int(year), int(month), int(day)).weekday()

    data["ftime"] = f"{time[:-3]}, {day_from_date(weekday)}, {day}. {month_from_date(int(month))} {year}"

    return jsonify(data)


@app.route('/graph_data')
def graph_data():
    n = request.args.get("n")

    w_data = get_all_weather(HOME_STATION["id"])[(-int(n) if n else -100):]

    times = [element["time"][-8:-3] for element in w_data]

    out = {
        "time": times,
        "temperature": [element["temperature"] for element in w_data],
        "temperature_i": [element["temperature_index"] for element in w_data],
        "humidity": [element["humidity"] for element in w_data]
    }

    return jsonify(out)


@app.context_processor
def inject_load():
    if sys.platform.startswith('linux'):
        with open('/proc/loadavg', 'rt') as f:
            load = f.read().split()[0:3]
    else:
        load = [int(random.random() * 100) / 100 for _ in range(3)]
    return {'load1': load[0], 'load5': load[1], 'load15': load[2]}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4999, debug=False)
