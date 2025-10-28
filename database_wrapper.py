import os
from datetime import datetime
from typing import Dict, List, Optional

import psycopg2
from dotenv import load_dotenv

from type import MatchData

load_dotenv()

host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
port = os.getenv("DB_PORT")


def connect_db():
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )
    cur = conn.cursor()
    return conn, cur


conn, cur = connect_db()


def close_db(conn, cur):
    cur.close()
    conn.close()


def list_tables(cur):
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='public';
    """)
    return [table[0] for table in cur.fetchall()]


def get_team_id_by_name(name):
    cur.execute("SELECT id FROM teams WHERE name = %s", (name,))
    filtered_id = cur.fetchone()
    return filtered_id[0] if filtered_id else None


def get_id_games_by_name(date, championship, team_1_id, team_2_id):
    cur.execute("""
                    SELECT id FROM games WHERE date = %s AND championship = %s AND team_1_id = %s AND team_2_id = %s;
                """, (date, championship, team_1_id, team_2_id))
    filtered_id = cur.fetchone()
    return filtered_id


def get_id_channel_by_name(channel_name):
    cur.execute("""
                    SELECT id FROM channels WHERE name = %s;
                """, (channel_name,))
    filtered_id = cur.fetchone()
    print(filtered_id, 'existente id')
    return filtered_id


def insert_into_teams(team_name, team_img):
    try:
        cur.execute("""
            INSERT INTO teams (name, img)
            VALUES (%s, %s)
            RETURNING id;
                    """, (team_name, team_img))
        team_id = cur.fetchone()
        conn.commit()

        return team_id[0]

    except:
        return None


def insert_into_games(date, championship, team_1_id, team_2_id):
    try:
        cur.execute("""
            INSERT INTO games (date, championship, team_1_id, team_2_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (date, championship, team_1_id, team_2_id))
        game_id = cur.fetchone()
        conn.commit()
        return game_id[0]
    except Exception as e:
        print("Erro ao inserir em games:", e)
        return None


def insert_into_channels(channel_name):
    try:
        cur.execute("""
            INSERT INTO channels (name)
            VALUES (%s)
            RETURNING id;
        """, (channel_name,))
        channel_id = cur.fetchone()
        conn.commit()
        return channel_id[0]
    except Exception as e:
        print('error:', e)


def add_team_if_not_exists(current_match: MatchData):
    team_1_name = current_match["team_1_name"]
    team_1_img = current_match["team_1_img"]

    team_2_name = current_match["team_2_name"]
    team_2_img = current_match["team_2_img"]

    date = current_match["date"]
    hour = current_match["hour"]

    championship = current_match["event_name"]

    channels = current_match["channels"]

    try:
        team_1_id = get_team_id_by_name(team_1_name) if get_team_id_by_name(
            team_1_name) else insert_into_teams(team_1_name, team_1_img)

        team_2_id = get_team_id_by_name(team_2_name) if get_team_id_by_name(
            team_2_name) else insert_into_teams(team_2_name, team_2_img)

        datetime_formatted = datetime.strptime(
            f"{date} {hour}", "%d-%m-%Y %H:%M")

        game_id = get_id_games_by_name(datetime_formatted, championship, team_1_id, team_2_id) if get_id_games_by_name(
            datetime_formatted, championship, team_1_id, team_2_id) else insert_into_games(datetime_formatted, championship, team_1_id, team_2_id)

        for channel in channels:
            channel_id = get_id_channel_by_name(channel) if get_id_channel_by_name(channel) else insert_into_channels(channel)
            

    except Exception as e:
        print("ERROR", e)
