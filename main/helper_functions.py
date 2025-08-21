import logging
from dotenv import load_dotenv
import os
import requests
import psycopg2

load_dotenv()  # Load environment variables from .env file

# set up logging
logger = logging.getLogger(__name__)

def get_api(url):
    list= []
    querystring = {"leagueid":"42"}

    headers = {
        "x-rapidapi-key": "2813f45597msh5899e05f16ab51ap19ba1fjsna2ce013c7e99",
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    matches= data["response"]["matches"]

    for match in matches:
        listed = {
        "utcTime": match["status"]["utcTime"],
        "scoreStr": match["status"]["scoreStr"],
        "home": match["home"]["name"],
        "away": match["away"]["name"],
        "finished": match["status"]["finished"]
        }
        list.append(listed)
    return list

def connect_to_db():
    logger.info("Connecting to the Postgres Database...")
    try:
        conn = psycopg2.connect(
            host = os.getenv("host"),
            port= os.getenv("port"),
            dbname= os.getenv("dbname"),
            user= os.getenv("user"),
            password= os.getenv("password")
        )
        logger.info("Database connected to Postgress...")
        return conn
        
    except psycopg2.Error as e:
        logger.error(f"Database connection failed: {e}", exc_info= True)
        raise


def create_schema_table(conn):
    logger.info("Creating Tables and Schema if not exists...")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev2;
            CREATE TABLE IF NOT EXISTS dev2.matches (
                id SERIAL PRIMARY KEY,
                local_time TIMESTAMP,
                score varchar(100),
                home varchar(100),
                away varchar(100),
                end_time BOOL
            ); 
        """)
        conn.commit()
        logger.info("Schema and Table created")
    except psycopg2.Error as e:
        logger.info(f"Failed to create schema and table: {e}", asc_info=True)
        raise

def insert_records(conn, data):
    logger.info("Inserting weather data into the database...")
    try:
        cur = conn.cursor()
        local_time = data["utcTime"]
        score = data["scoreStr"]
        home = data["home"]
        away = data["away"]
        end_time = data["finished"]
        logger.info(f"preparing insert for city: (location[name])")

        cur.execute("""
            INSERT INTO dev2.matches(
                local_time,
                score,
                home,
                away,
                end_time       
            ) VALUES(%s, %s, %s, %s, %s)
        """, (
            local_time,
            score,
            home,
            away,
            end_time
        ))
        conn.commit()
        logger.info("Insert Successful")
    except psycopg2.Error as e:
        logger.error("Error inserting the data:{e}", exc_info=True)
        raise

# def main():
#     try:
#         url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-matches-by-league"
#         logger.info("Starting weather data ETL process...")
#         data = get_api(url)
#         conn = connect_to_db()
#         create_schema_table(conn)
#         for record in data:
#             insert_records(conn, record)
#     except Exception as e:
#         logger.error(f"error occured during ETL drill: {e}", exc_info=True)
#     finally:
#         if "conn" in locals():
#             conn.close()
#             logger.info("closed postgres connection")

# if __name__ == "__main__":
#     main()

# url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-matches-by-league"
# get_api(url)
# connect_to_db()