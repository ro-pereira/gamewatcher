import os
from datetime import datetime

import psycopg2
from dotenv import load_dotenv

from type import GameInfo, MatchData

load_dotenv()

host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
port = os.getenv("DB_PORT")


def connect_db():
    conn = psycopg2.connect(host=host,
                            database=database,
                            user=user,
                            password=password,
                            port=port)
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


def get_team_id_by_name(name: str):
    cur.execute("""
                    SELECT id FROM teams WHERE name = %s
                """, (name, ))
    filtered_id = cur.fetchone()
    return filtered_id[0] if filtered_id else None


def get_id_games_by_name(game_info: GameInfo):
    cur.execute("""
                    SELECT id FROM games WHERE date = %s AND championship = %s AND team_1_id = %s AND team_2_id = %s;
                """, (game_info.datetime_formatted, game_info.championship, game_info.team_1_id, game_info.team_2_id))
    filtered_id = cur.fetchone()
    return filtered_id


def get_id_channel_by_name(channel_name: str):
    cur.execute("""
                    SELECT id FROM channels WHERE name = %s;
                """, (channel_name,))
    filtered_id = cur.fetchone()
    return filtered_id


def check_save_transmition(channel_id: int, game_id: int):
    try:
        cur.execute("""
                        SELECT * FROM channels_games 
                        WHERE channel_id = %s AND game_id = %s;
                    """, (channel_id, game_id,))
        transmission = cur.fetchone()
        return transmission
    except Exception as e:
        print("error:", e)
        return None


def insert_into_teams(team_name: str, team_img: str):
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


def insert_into_games(game_info: GameInfo):
    try:
        cur.execute("""
                        INSERT INTO games (date, championship, team_1_id, team_2_id)
                        VALUES (%s, %s, %s, %s)
                        RETURNING id;
                    """, (game_info.datetime_formatted, game_info.championship, game_info.team_1_id, game_info.team_2_id))
        game_id = cur.fetchone()
        conn.commit()
        return game_id[0]
    except Exception as e:
        print("Erro ao inserir em games:", e)
        return None


def insert_into_channels(channel_name: str):
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


def insert_into_channels_games(channel_id: int, game_id: int):
    try:
        cur.execute(
            """
                INSERT INTO channels_games (channel_id, game_id) 
                VALUES (%s, %s)
            """, (channel_id, game_id,))
        conn.commit()
    except Exception as e:
        print(e)


def add_team_if_not_exists(match: MatchData):
    try:
        team_1_id = get_team_id_by_name(match.team_1_name) if get_team_id_by_name(
            match.team_1_name) else insert_into_teams(match.team_1_name, match.team_1_img)

        team_2_id = get_team_id_by_name(match.team_2_name) if get_team_id_by_name(
            match.team_2_name) else insert_into_teams(match.team_2_name, match.team_2_img)

        datetime_formatted = datetime.strptime(
            f"{match.date} {match.hour}", "%d-%m-%Y %H:%M")

        game_info = GameInfo(
            datetime_formatted=datetime_formatted,
            championship=match.event_name,
            team_1_id=team_1_id,
            team_2_id=team_2_id
        )

        game_id = get_id_games_by_name(game_info) if get_id_games_by_name(
            game_info) else insert_into_games(game_info)

        for channel in match.channels:
            channel_id = get_id_channel_by_name(
                channel) if get_id_channel_by_name(
                    channel) else insert_into_channels(channel)

            if not check_save_transmition(channel_id, game_id):
                try:
                    if game_id and channel_id:
                        insert_into_channels_games(channel_id, game_id)
                except Exception as e:
                    print("ERROR", e)

    except Exception as e:
        print("ERROR", e)
