"""
db_stuff.py
27. November 2022

Functions for handling the database.

Author:
Nilusink
"""
import sqlite3


def to_dict(keys: list, values: list) -> dict:
    return {key: value for key, value in zip(keys, values)}


def station_by_name(connection: sqlite3.Connection, name: str) -> dict:
    """
    get a station by its name
    """
    result = connection.execute("PRAGMA table_info(stations);")
    t_info = result.fetchall()
    keys = [column[1] for column in t_info]

    result = connection.execute(
        "SELECT * FROM stations WHERE name = ?;",
        (name,)
    ).fetchone()

    # no results
    if not result:
        raise KeyError(f"No station with name {name}")

    return to_dict(keys, result)


def get_last_weather(
        connection: sqlite3.Connection,
        station_id: int
) -> dict | None:
    """
    get the stations last entry
    """
    result = connection.execute("PRAGMA table_info(weather);")
    t_info = result.fetchall()
    keys = [column[1] for column in t_info]

    result = connection.execute(
        "SELECT * FROM weather WHERE station_id = ? ORDER BY id DESC",
        (station_id,)
    ).fetchone()

    if result:
        return to_dict(keys, result)

    return


def get_all_weather(
        connection: sqlite3.Connection,
        station_id: int,
        n_results: int = -1
) -> list[dict]:
    """
    get all collected data points of a station
    """
    result = connection.execute("PRAGMA table_info(weather);")
    t_info = result.fetchall()
    keys = [column[1] for column in t_info]

    query = connection.execute(
        "SELECT * FROM weather WHERE station_id = ? ORDER BY id DESC",
        (station_id,)
    )
    if n_results < 0:
        result = query.fetchall()

    else:
        result = query.fetchmany()

    out: list[dict] = []
    for r in result:
        out.append(to_dict(keys, r))

    return out
