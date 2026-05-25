from sqlalchemy import create_engine,text
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv

load_dotenv()

def create_db_engine():
    '''
    Create the database and return the engine.
    This function is tend to be run for only once.
    '''
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    port = os.getenv('DB_PORT', '3306')  # Default to 3306 if not set
    db_name = os.getenv('DB_NAME')
    uri = os.getenv('DB_URI', 'localhost')  # Default to localhost if not set
    
    # Validate and clean port value
    if port is None or port == 'None' or port == '':
        port = '3306'
    
    # connect to mysql
    connection_string = "mysql+pymysql://{}:{}@{}:{}".format(user, password, uri, port)
    engine = create_engine(connection_string)

    # create database
    try:
        with engine.connect() as connection:
            sql = """
            CREATE DATABASE IF NOT EXISTS {};
            """.format(db_name)
            connection.execute(text(sql))
            connection.commit()
            print(f"{db_name} created successfully.")
    except SQLAlchemyError as e:
        print("Fail to create database.")
        print("Error:",e)
    
    connection_string = "mysql+pymysql://{}:{}@{}:{}/{}".format(user, password, uri, port,db_name)
    engine = create_engine(connection_string)

    create_tables(engine)

    return engine


def create_tables(engine):
    '''
    Create the tables.
    This function is tend to be run for only once.
    All the names of tables and attributes are lowercased.
    All the name of attributes keep the same with raw data.
    '''

    try:
        with engine.connect() as connection:
            
            # create the table station
            sql = '''
            CREATE TABLE IF NOT EXISTS station (
            number SMALLINT UNSIGNED NOT NULL PRIMARY KEY,
            name VARCHAR(50),               
            address VARCHAR(100), 
            position_lat DOUBLE,
            position_lng DOUBLE,
            bike_stands SMALLINT UNSIGNED,
            banking TINYINT(1),
            bonus TINYINT(1)
            );'''
            connection.execute(text(sql))
            
            
            # create the table availability
            sql = '''
            CREATE TABLE IF NOT EXISTS availability (
            number SMALLINT UNSIGNED,
            available_bikes SMALLINT UNSIGNED,
            available_bike_stands SMALLINT UNSIGNED,
            last_update DATETIME,
            status VARCHAR(10), 
            PRIMARY KEY (number,last_update),
            INDEX idx_last_update (last_update),
            FOREIGN KEY (number) REFERENCES station(number)
                ON UPDATE CASCADE
                ON DELETE CASCADE
            );
            '''
            connection.execute(text(sql))
            
            # creaete table user
            sql='''
            CREATE TABLE IF NOT EXISTS user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            avatar_url VARCHAR(255) DEFAULT "",
            create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            token VARCHAR(255) UNIQUE
            )ENGINE=InnoDB AUTO_INCREMENT=1000;
            '''
            connection.execute(text(sql))
            
            # creaete table favorite
            sql='''
            CREATE TABLE IF NOT EXISTS favorite (
            user_id INT,
            station_number SMALLINT UNSIGNED,
            PRIMARY KEY (user_id,station_number),
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
            sql='''
            CREATE TABLE IF NOT EXISTS current_weather (
            dt DATETIME PRIMARY KEY,
            temperature FLOAT,
            windspeed FLOAT,
            appearent_temperature FLOAT,
            weathercode INTEGER
            );
            '''
            connection.execute(text(sql))
            
            # create table forecast_hourly
            sql='''
            CREATE TABLE IF NOT EXISTS forecast_hourly (
            dt DATETIME PRIMARY KEY,
            temperature FLOAT,
            windspeed FLOAT,
            weathercode INTEGER
            );
            '''
            connection.execute(text(sql))
            
            # create table forecast_daily
            sql='''
            CREATE TABLE IF NOT EXISTS forecast_daily (
            dt DATE PRIMARY KEY,
            temp_max FLOAT,
            temp_min FLOAT,
            weathercode INTEGER
            );
            '''
            connection.execute(text(sql))
            
            connection.commit()
            print("Table station created successfully.")
            print("Table availability created successfully.")
            print("Table user created successfully.")
            print("Table favorite created successfully.")
            print("Table current_weather created successfully.")
            print("Table forecast_hourly created successfully.")
            print("Table forecast_daily created successfully.")
            
    except SQLAlchemyError as e:
        print("Table creating failed")
        print("Error: ", e)

# 只在直接运行此文件时创建数据库
# 正常情况下，应该先运行 init_database.py 进行初始化
if __name__ == "__main__":
    engine = create_db_engine()
else:
    # 当被其他模块导入时，只连接到已存在的数据库
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    port = os.getenv('DB_PORT', '3306')
    db_name = os.getenv('DB_NAME')
    uri = os.getenv('DB_URI', 'localhost')
    
    # 验证并清理端口值
    if port is None or port == 'None' or port == '':
        port = '3306'
    
    connection_string = "mysql+pymysql://{}:{}@{}:{}/{}".format(user, password, uri, port, db_name)
    engine = create_engine(connection_string)
