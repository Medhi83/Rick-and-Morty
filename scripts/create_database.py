import logging

import sqlalchemy

DB_NAME = "rick_n_morty"
DB_USER = "root"
DB_PASSWORD = "test"


def create_database() -> None:
    engine = sqlalchemy.create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost")
    conn = engine.connect()
    conn.execute("commit")
    try:
        conn.execute(f"CREATE DATABASE {DB_NAME}")
        logging.info("Done!")
    except Exception as e:
        logging.exception(f"Error during database creation\r\n\n{e}")
    conn.close()


if __name__ == "__main__":
    create_database()
