"""
数据库初始化脚本 - SQLite 版本
自动创建 SQLite 数据库和表
无需安装 MySQL！
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# 加载环境变量
load_dotenv()

def get_db_config():
    """获取数据库配置"""
    db_path = os.getenv('DB_PATH', 'data/bike_share.db')
    return {'db_path': db_path}

def create_database_and_tables(config):
    """创建 SQLite 数据库和所有表"""
    print(f"\n🔍 步骤 1: 创建 SQLite 数据库...")
    print(f"   数据库路径: {config['db_path']}")
    
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(config['db_path']), exist_ok=True)
        
        # 创建 SQLite 连接
        connection_string = f"sqlite:///{config['db_path']}"
        engine = create_engine(connection_string)
        
        print(f"   ✅ SQLite 数据库连接成功！")
        
        # 创建表
        print(f"\n🔍 步骤 2: 创建数据表...")
        
        with engine.connect() as conn:
            # 创建 station 表
            print("   📋 创建 station 表...")
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS station (
                    number INTEGER NOT NULL PRIMARY KEY,
                    name VARCHAR(50),               
                    address VARCHAR(100), 
                    position_lat REAL,
                    position_lng REAL,
                    bike_stands INTEGER,
                    banking INTEGER,
                    bonus INTEGER
                )
            '''))
            
            # 创建 availability 表
            print("   📋 创建 availability 表...")
            conn.execute(text('''
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
                )
            '''))
            
            # 创建索引
            conn.execute(text('''
                CREATE INDEX IF NOT EXISTS idx_last_update ON availability(last_update)
            '''))
            
            # 创建 user 表
            print("   📋 创建 user 表...")
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    avatar_url VARCHAR(255) DEFAULT '',
                    create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    token VARCHAR(255) UNIQUE
                )
            '''))
            
            # 创建 favorite 表
            print("   📋 创建 favorite 表...")
            conn.execute(text('''
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
                )
            '''))
            
            # 创建 current_weather 表
            print("   📋 创建 current_weather 表...")
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS current_weather (
                    dt DATETIME PRIMARY KEY,
                    temperature REAL,
                    windspeed REAL,
                    appearent_temperature REAL,
                    weathercode INTEGER
                )
            '''))
            
            # 创建 forecast_hourly 表
            print("   📋 创建 forecast_hourly 表...")
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS forecast_hourly (
                    dt DATETIME PRIMARY KEY,
                    temperature REAL,
                    windspeed REAL,
                    weathercode INTEGER
                )
            '''))
            
            # 创建 forecast_daily 表
            print("   📋 创建 forecast_daily 表...")
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS forecast_daily (
                    dt DATE PRIMARY KEY,
                    temp_max REAL,
                    temp_min REAL,
                    weathercode INTEGER
                )
            '''))
            
            conn.commit()
        
        print("   ✅ 所有数据表创建成功！")
        return True
        
    except Exception as e:
        print(f"   ❌ 创建失败: {e}")
        return False

def verify_setup(config):
    """验证数据库设置"""
    print(f"\n🔍 步骤 3: 验证数据库设置...")
    
    try:
        connection_string = f"sqlite:///{config['db_path']}"
        engine = create_engine(connection_string)
        
        with engine.connect() as conn:
            # 检查所有表
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
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
    print("🚀 SQLite 数据库初始化脚本")
    print("=" * 70)
    print("\n✨ 使用 SQLite - 无需安装 MySQL！")
    
    # 获取配置
    config = get_db_config()
    
    print("\n📋 当前配置:")
    print(f"   数据库类型: SQLite")
    print(f"   数据库路径: {config['db_path']}")
    print(f"   数据库大小: {'已存在' if os.path.exists(config['db_path']) else '将创建'}")
    
    # 创建数据库和表
    if not create_database_and_tables(config):
        print("\n❌ 初始化失败")
        sys.exit(1)
    
    # 验证设置
    if not verify_setup(config):
        print("\n⚠️  警告: 数据库设置可能不完整")
    
    # 完成
    print("\n" + "=" * 70)
    print("🎉 数据库初始化完成！")
    print("=" * 70)
    print("\n✅ 现在可以运行应用了:")
    print("   python run.py")
    print("\n� 数据库文件位置:")
    print(f"   {os.path.abspath(config['db_path'])}")
    print()

if __name__ == "__main__":
    main()
