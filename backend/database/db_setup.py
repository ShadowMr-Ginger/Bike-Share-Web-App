from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv

load_dotenv()

def create_db_engine():
    '''
    Create the database and return the engine.
    Uses SQLite - no MySQL installation required!
    '''
    # Get database path from env or use default
    db_path = os.getenv('DB_PATH', 'data/bike_share.db')
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Create SQLite connection string
    connection_string = f"sqlite:///{db_path}"
    engine = create_engine(connection_string)
    
    print(f"Using SQLite database at: {db_path}")
    
    # Create tables
    create_tables(engine)
    
    return engine


def create_tables(engine):
    '''
    Create the tables for SQLite.
    SQLite-compatible syntax (no UNSIGNED, no AUTO_INCREMENT, no ENGINE).
    '''

    try:
        with engine.connect() as connection:
            
            # create the table station
            sql = '''
            CREATE TABLE IF NOT EXISTS station (
                number INTEGER NOT NULL PRIMARY KEY,
                name VARCHAR(50),               
                address VARCHAR(100), 
                position_lat REAL,
                position_lng REAL,
                bike_stands INTEGER,
                banking INTEGER,
                bonus INTEGER
            );'''
            connection.execute(text(sql))
            
            # create the table availability
            sql = '''
            CREATE TABLE IF NOT EXISTS availability (
                number INTEGER,
                available_bikes INTEGER,
                available_bike_stands INTEGER,
                last_update DATETIME,
                status VARCHAR(10), 
                PRIMARY KEY (number, last_update),
                FOREIGN KEY (number) REFERENCES station(number)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );
            '''
            connection.execute(text(sql))
            
            # create index for availability
            sql = '''
            CREATE INDEX IF NOT EXISTS idx_last_update ON availability(last_update);
            '''
            connection.execute(text(sql))
            
            # create table user
            sql = '''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                avatar_url VARCHAR(255) DEFAULT '',
                create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                token VARCHAR(255) UNIQUE
            );
            '''
            connection.execute(text(sql))
            
            # create table favorite
            sql = '''
            CREATE TABLE IF NOT EXISTS favorite (
                user_id INTEGER,
                station_number INTEGER,
                PRIMARY KEY (user_id, station_number),
                FOREIGN KEY (station_number) REFERENCES station(number)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES user(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );
            '''
            connection.execute(text(sql))
            
            # create table current_weather
            sql = '''
            CREATE TABLE IF NOT EXISTS current_weather (
                dt DATETIME PRIMARY KEY,
                temperature REAL,
                windspeed REAL,
                appearent_temperature REAL,
                weathercode INTEGER
            );
            '''
            connection.execute(text(sql))
            
            # create table forecast_hourly
            sql = '''
            CREATE TABLE IF NOT EXISTS forecast_hourly (
                dt DATETIME PRIMARY KEY,
                temperature REAL,
                windspeed REAL,
                weathercode INTEGER
            );
            '''
            connection.execute(text(sql))
            
            # create table forecast_daily
            sql = '''
            CREATE TABLE IF NOT EXISTS forecast_daily (
                dt DATE PRIMARY KEY,
                temp_max REAL,
                temp_min REAL,
                weathercode INTEGER
            );
            '''
            connection.execute(text(sql))
            
            connection.commit()
            print("[OK] Table station created successfully.")
            print("[OK] Table availability created successfully.")
            print("[OK] Table user created successfully.")
            print("[OK] Table favorite created successfully.")
            print("[OK] Table current_weather created successfully.")
            print("[OK] Table forecast_hourly created successfully.")
            print("[OK] Table forecast_daily created successfully.")
            
    except SQLAlchemyError as e:
        print("[FAIL] Table creating failed")
        print("Error: ", e)

# 只在直接运行此文件时创建数据库
# 正常情况下，应该先运行 init_database.py 进行初始化
if __name__ == "__main__":
    engine = create_db_engine()
else:
    # 当被其他模块导入时，连接到 SQLite 数据库并确保表已创建
    db_path = os.getenv('DB_PATH', 'data/bike_share.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    connection_string = f"sqlite:///{db_path}"
    engine = create_engine(connection_string)
    create_tables(engine)
