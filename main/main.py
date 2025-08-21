from helper_functions import get_api, connect_to_db, insert_records, create_schema_table
import logging

logger = logging.getLogger(__name__)

def main():
    try:
        url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-matches-by-league"
        logger.info("Starting weather data ETL process...")
        data = get_api(url)
        conn = connect_to_db()
        create_schema_table(conn)
        for record in data:
            insert_records(conn, record)
    except Exception as e:
        logger.error(f"error occured during ETL drill: {e}", exc_info=True)
    finally:
        if "conn" in locals():
            conn.close()
            logger.info("closed postgres connection")

if __name__ == "__main__":
    main()