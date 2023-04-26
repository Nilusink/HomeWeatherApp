"""
db_stuff.py
27. November 2022

Functions for handling the database.

Author:
Nilusink
"""
import sqlalchemy as db
import typing as tp


# types
class CPUStats:
    core_voltage: float
    core_clock: float
    core_temp: float
    usage: int


# db setup---
META = db.MetaData()
DB_NAME: str = "./main.db"
ENGINE = db.create_engine(f"sqlite:///{DB_NAME}", echo=False)

WEATHER_EMP = db.Table(
    'weather', META,
    db.Column('id', db.Integer, primary_key=True),
    db.Column("time", db.String, nullable=False),
    db.Column("station_id", db.Integer, nullable=False),
    db.Column("temperature", db.Float, nullable=True),
    db.Column("temperature_index", db.Float, nullable=True),
    db.Column("humidity", db.Float, nullable=True),
    db.Column("air_pressure", db.Float, nullable=True),
)

STATIONS_EMP = db.Table(
    "stations", META,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("name", db.String, nullable=False),
    db.Column("position", db.String, nullable=False),
    db.Column("height", db.Float, nullable=True),
)


PI_STATS_EMP = db.Table(
    "pi_stats", META,
    db.Column("time", db.INT, primary_key=True, nullable=False),
    db.Column("core_voltage", db.FLOAT, nullable=False),
    db.Column("core_clock", db.FLOAT, nullable=False),
    db.Column("core_temp", db.FLOAT, nullable=False),
    db.Column("ram_total", db.INT, nullable=False),
    db.Column("ram_total", db.INT, nullable=False),
    db.Column("ram_left", db.INT, nullable=False),
    db.Column("net_in", db.INT, nullable=False, default=0),
    db.Column("net_out", db.INT, nullable=False, default=0),
    db.Column("disk_read", db.INT, nullable=False, default=0),
    db.Column("disk_write", db.INT, nullable=False, default=0),
)


def station_by_name(name: str) -> dict:
    """
    get a station by its name
    """
    connection = ENGINE.connect()
    stations = db.Table('stations', META, autoload=True, autoload_with=ENGINE)

    query = db.select([stations]).where(stations.columns.name == name)
    result = connection.execute(query).fetchall()

    # no results
    if not result:
        raise KeyError(f"No station with name {name}")

    return dict(result[0])


def get_last_weather(station_id: int) -> dict | None:
    """
    get the stations last entry
    """
    connection = ENGINE.connect()
    weather = db.Table('weather', META, autoload=True, autoload_with=ENGINE)

    query = db.select([weather]).where(weather.columns.station_id == station_id)
    result = connection.execute(query).fetchall()

    if result:
        return dict(result[-1])

    return


def get_all_weather(station_id: int) -> list[dict]:
    """
    get all collected data points of a station
    """
    connection = ENGINE.connect()
    weather = db.Table('weather', META, autoload=True, autoload_with=ENGINE)

    query = db.select([weather]).where(weather.columns.station_id == station_id)
    result = connection.execute(query).fetchall()

    out: list[dict] = []
    for i in range(len(result)):
        out.append(dict(result[i]))

    return out


def cpu_stats() -> CPUStats:
    ...
