import psycopg2
import sqlalchemy
from sqlalchemy import *
import pandas as pd
from secrets import DB_HOST, DB_NAME, DB_PASS, DB_USER

def load_spotify_data(songs_df):
    # Table to store spotify data
    table_name = "spotify_daily_songs"

    # DB engine
    engine = sqlalchemy.create_engine("postgresql://%s:%s@%s/%s" % (DB_USER, DB_PASS, DB_HOST, DB_NAME))

    # Connection to db
    conn = psycopg2.connect(
        host = DB_HOST,
        database = DB_NAME,
        user = DB_USER,
        password = DB_PASS
    )

    # Create table if it doesn't exist
    if not engine.dialect.has_table(engine, table_name):
        metadata = MetaData(engine)
        # Create a table with the appropriate columns
        Table(table_name, metadata,

            Column('song_name', String), 
            Column('artist_name', String),
            # Since the data is only for one user, played_at must be unique
            Column('played_at', DateTime, primary_key=True, nullable=False),
            Column('timestamp', Date)
        )
        # Execute table creation
        metadata.create_all()

    # Write from pandas dataframe directly to db
    try:
        songs_df.to_sql(table_name, engine, index=False, if_exists='append')
    except:
        print("Data already exists in db")
        
    # Close connection to db
    conn.close()