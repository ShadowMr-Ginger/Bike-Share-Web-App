"""
数据库初始化脚本
自动检查 MySQL 连接、创建数据库和表
运行此脚本后，可以直接运行 run.py
"""

import os
import sys
from dotenv import load_dotenv
import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# 加载环境变量
load_dotenv()

def get_db_config():
    """获取数据库配置，提供默认值"""
    config = {
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'port': os.getenv('DB_PORT', '3306'),
        'db_name': os.getenv('DB_NAME', 'local_databasejcdecaux'),
        'uri': os.getenv('DB_URI', '127.0.0.1')
    }
    
    # 清理端口值
    if config['port'] is None or config['port'] == 'None' or config['port'] == '':
        config['port'] = '3306'
    
    # 转换为整数
    try:
        config['port'] = int(config['port'])
    except ValueError:
        print(f"⚠️  警告: DB_PORT 值 '{config['port']}' 无效，使用默认值 3306")
        config['port'] = 3306
    
    return config

def test_mysql_connection(config):
    """测试 MySQL 服务器连接"""
    print("\n🔍 步骤 1: 测试 MySQL 服务器连接...")
    print(f"   连接到: {config['user']}@{config['uri']}:{config['port']}")
    
    try:
        connection = pymysql.connect(
            host=config['uri'],
            user=config['user'],
            password=config['password'],
            port=config['port'],
            connect_timeout=5
        )
        connection.close()
        print("   ✅ MySQL 服务器连接成功！")
        return True
    except pymysql.err.OperationalError as e:
        print(f"   ❌ MySQL 服务器连接失败: {e}")
        print("\n💡 请检查:")
        print("   1. MySQL 服务是否正在运行")
        print("   2. 用户名和密码是否正确")
        print("   3. 主机地址和端口是否正确")
        print("   4. 防火墙是否允许连接")
        return False
    except Exception as e:
        print(f"   ❌ 连接错误: {e}")
        return False

def create_database(config):
    """创建数据库（如果不存在）"""
    print(f"\n🔍 步骤 2: 创建数据库 '{config['db_name']}'...")
    
    try:
        # 连接到 MySQL 服务器（不指定数据库）
        connection = pymysql.connect(
            host=config['uri'],
            user=config['user'],
            password=config['password'],
            port=config['port']
        )
        
        cursor = connection.cursor()
        
        # 检查数据库是否存在
        cursor.execute(f"SHOW DATABASES LIKE '{config['db_name']}'")
        result = cursor.fetchone()
        
        if result:
            print(f"   ℹ️  数据库 '{config['db_name']}' 已存在")
        else:
            # 创建数据库
            cursor.execute(f"CREATE DATABASE {config['db_name']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"   ✅ 数据库 '{config['db_name']}' 创建成功！")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"   ❌ 创建数据库失败: {e}")
        return False

def create_tables(config):
    """创建所有表"""
    print(f"\n🔍 步骤 3: 创建数据表...")
    
    try:
        # 连接到指定的数据库
        connection_string = f"mysql+pymysql://{config['user']}:{config['password']}@{config['uri']}:{config['port']}/{config['db_name']}"
        engine = create_engine(connection_string)
        
        with engine.connect() as conn:
            # 创建 station 表
            print("   📋 创建 station 表...")
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS station (
                    number SMALLINT UNSIGNED NOT NULL PRIMARY KEY,
                    name VARCHAR(50),               
                    address VARCHAR(100), 
                    position_lat DOUBLE,
                    position_lng DOUBLE,
                    bike_stands SMALLINT UNSIGNED,
                    banking TINYINT(1),
                    bonus TINYINT(1)
                )
            '''))
            
            # 创建 availability 表
            print("   📋 创建 availability 表...")
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS availability (
                    number SMALLINT UNSIGNED,
                    available_bikes SMALLINT UNSIGNED,
                    available_bike_stands SMALLINT UNSIGNED,
                    last_update DATETIME,
                    status VARCHAR(10), 
                    PRIMARY KEY (number, last_update),
                    INDEX idx_last_update (last_update),
                    FOREIGN KEY (number) REFERENCES station(number)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
                )
            '''))
            
            # 创建 user 表
            print("   📋 创建 user 表...")
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS user (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    avatar_url VARCHAR(255) DEFAULT "",
                    create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    token VARCHAR(255) UNIQUE
                ) ENGINE=InnoDB AUTO_INCREMENT=1000
            '''))
            
            # 创建 favorite 表
            print("   📋 创建 favorite 表...")
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS favorite (
                    user_id INT,
                    station_number SMALLINT UNSIGNED,
                    PRIMARY KEY (user_id, station_number),
                    FOREIGN KEY (station_number) REFERENCES station(number)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES user(id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
                )
            '''))
            
            # 创建 current_weather 表
            print("   📋 创建 current_weather 表...")
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS current_weather (
                    dt DATETIME PRIMARY KEY,
                    temperature FLOAT,
                    windspeed FLOAT,
                    appearent_temperature FLOAT,
                    weathercode INTEGER
                )
            '''))
            
            # 创建 forecast_hourly 表
            print("   📋 创建 forecast_hourly 表...")
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS forecast_hourly (
                    dt DATETIME PRIMARY KEY,
                    temperature FLOAT,
                    windspeed FLOAT,
                    weathercode INTEGER
                )
            '''))
            
            # 创建 forecast_daily 表
            print("   📋 创建 forecast_daily 表...")
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS forecast_daily (
                    dt DATE PRIMARY KEY,
                    temp_max FLOAT,
                    temp_min FLOAT,
                    weathercode INTEGER
                )
            '''))
            
            conn.commit()
        
        print("   ✅ 所有数据表创建成功！")
        return True
        
    except Exception as e:
        print(f"   ❌ 创建表失败: {e}")
        return False

def verify_setup(config):
    """验证数据库设置"""
    print(f"\n🔍 步骤 4: 验证数据库设置...")
    
    try:
        connection_string = f"mysql+pymysql://{config['user']}:{config['password']}@{config['uri']}:{config['port']}/{config['db_name']}"
        engine = create_engine(connection_string)
        
        with engine.connect() as conn:
            # 检查所有表
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            
            expected_tables = [
                'station', 'availability', 'user', 'favorite',
                'current_weather', 'forecast_hourly', 'forecast_daily'
            ]
            
            print(f"   📊 找到 {len(tables)} 个表:")
            for table in tables:
                status = "✅" if table in expected_tables else "⚠️"
                print(f"      {status} {table}")
            
            missing_tables = set(expected_tables) - set(tables)
            if missing_tables:
                print(f"   ⚠️  缺少表: {', '.join(missing_tables)}")
                return False
            
            print("   ✅ 数据库设置验证成功！")
            return True
            
    except Exception as e:
        print(f"   ❌ 验证失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 70)
    print("🚀 数据库初始化脚本")
    print("=" * 70)
    
    # 获取配置
    config = get_db_config()
    
    print("\n📋 当前配置:")
    print(f"   数据库用户: {config['user']}")
    print(f"   数据库地址: {config['uri']}")
    print(f"   数据库端口: {config['port']}")
    print(f"   数据库名称: {config['db_name']}")
    print(f"   密码: {'已设置' if config['password'] else '未设置'}")
    
    # 步骤 1: 测试连接
    if not test_mysql_connection(config):
        print("\n❌ 初始化失败: 无法连接到 MySQL 服务器")
        print("\n💡 解决方案:")
        print("   1. 确保 MySQL 服务正在运行")
        print("   2. 检查 .env 文件中的数据库配置")
        print("   3. 确认用户名和密码正确")
        sys.exit(1)
    
    # 步骤 2: 创建数据库
    if not create_database(config):
        print("\n❌ 初始化失败: 无法创建数据库")
        sys.exit(1)
    
    # 步骤 3: 创建表
    if not create_tables(config):
        print("\n❌ 初始化失败: 无法创建数据表")
        sys.exit(1)
    
    # 步骤 4: 验证设置
    if not verify_setup(config):
        print("\n⚠️  警告: 数据库设置可能不完整")
    
    # 完成
    print("\n" + "=" * 70)
    print("🎉 数据库初始化完成！")
    print("=" * 70)
    print("\n✅ 现在可以运行应用了:")
    print("   python run.py")
    print("\n📚 或者运行测试:")
    print("   python test_dependencies.py")
    print()

if __name__ == "__main__":
    main()
