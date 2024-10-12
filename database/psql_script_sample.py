import json
import jsonlines
import psycopg2
from psycopg2.extras import execute_batch
from tqdm import tqdm

# Database connection parameters
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "B@dmeetsevil9x"
DB_HOST = "localhost"
DB_PORT = "5432"

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS nba_player_info (
            id SERIAL PRIMARY KEY,
            player_name VARCHAR(255),
            team VARCHAR(50),
            age INTEGER,
            gp INTEGER,
            wins INTEGER,
            losses INTEGER,
            min FLOAT,
            pts FLOAT,
            fgm FLOAT,
            fga FLOAT,
            fg_pct FLOAT,
            three_pm FLOAT,
            three_pa FLOAT,
            three_ppct FLOAT,
            ftm FLOAT,
            fta FLOAT,
            ft_pct FLOAT,
            oreb FLOAT,
            dreb FLOAT,
            reb FLOAT,
            ast FLOAT,
            tov FLOAT,
            stl FLOAT,
            blk FLOAT,
            pf FLOAT,
            fp FLOAT,
            dd2 FLOAT,
            td3 FLOAT,
            plus_minus_box FLOAT
        )
        """)
    conn.commit()

def safe_cast(val, to_type, default=None):
    try:
        if to_type == int:
            # For integer fields, first convert to float then to int
            return int(float(val)) if val is not None else default
        return to_type(val) if val is not None else default
    except (ValueError, TypeError):
        return default

def import_player_data(file_path, conn):
    insert_query = """
    INSERT INTO nba_player_info (
        player_name, team, age, gp, wins, losses, min, pts, fgm, fga, fg_pct,
        three_pm, three_pa, three_ppct, ftm, fta, ft_pct, oreb, dreb, reb,
        ast, tov, stl, blk, pf, fp, dd2, td3, plus_minus_box
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    """

    player_data = []
    skipped_records = 0
    total_records = 0
    field_counts = {}

    print(f"Reading data from {file_path}")
    try:
        with jsonlines.open(file_path) as reader:
            for player in tqdm(reader):
                total_records += 1
                try:
                    # Count occurrences of each field
                    for key in player.keys():
                        field_counts[key] = field_counts.get(key, 0) + 1

                    player_data.append((
                        player.get("player"),
                        player.get("team"),
                        safe_cast(player.get("age"), int),
                        safe_cast(player.get("gp"), int),
                        safe_cast(player.get("wins"), int),
                        safe_cast(player.get("losses"), int),
                        safe_cast(player.get("min"), float),
                        safe_cast(player.get("pts"), float),
                        safe_cast(player.get("fgm"), float),
                        safe_cast(player.get("fga"), float),
                        safe_cast(player.get("fg_pct"), float),
                        safe_cast(player.get("three_pm"), float),
                        safe_cast(player.get("three_pa"), float),
                        safe_cast(player.get("three_ppct"), float),
                        safe_cast(player.get("ftm"), float),
                        safe_cast(player.get("fta"), float),
                        safe_cast(player.get("ft_pct"), float),
                        safe_cast(player.get("oreb"), float),
                        safe_cast(player.get("dreb"), float),
                        safe_cast(player.get("reb"), float),
                        safe_cast(player.get("ast"), float),
                        safe_cast(player.get("tov"), float),
                        safe_cast(player.get("stl"), float),
                        safe_cast(player.get("blk"), float),
                        safe_cast(player.get("pf"), float),
                        safe_cast(player.get("fp"), float),
                        safe_cast(player.get("dd2"), float),
                        safe_cast(player.get("td3"), float),
                        safe_cast(player.get("plus_minus_box"), float)
                    ))
                except Exception as e:
                    print(f"Error processing player: {player.get('player', 'Unknown')}")
                    print(f"Error details: {str(e)}")
                    skipped_records += 1

        print(f"\nTotal records in file: {total_records}")
        print(f"Records skipped due to errors: {skipped_records}")
        print(f"Records prepared for insertion: {len(player_data)}")
        
        print("\nField occurrence in the data:")
        for field, count in field_counts.items():
            print(f"{field}: {count} times")

        if player_data:
            with conn.cursor() as cur:
                execute_batch(cur, insert_query, player_data)
            conn.commit()
            print(f"\nInserted {len(player_data)} records into the database.")
        else:
            print("\nNo valid records found for insertion.")

    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except jsonlines.jsonlines.InvalidLineError as e:
        print(f"Error reading JSON line: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")

    return len(player_data)

if __name__ == "__main__":
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Successfully connected to the database.")
        create_table(conn)

        # Specify the path to your JSONL file here
        jsonl_file_path = "./nba_players.jsonl"

        records_inserted = import_player_data(jsonl_file_path, conn)
        print(f"Total records inserted: {records_inserted}")

    except psycopg2.Error as e:
        print(f"A database error occurred: {e}")
    except FileNotFoundError as e:
        print(f"File error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")