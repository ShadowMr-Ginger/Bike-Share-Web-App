"""
测试所有关键依赖是否正常工作
Test all critical dependencies for Python 3.14 compatibility
"""

import sys
print(f"Python 版本: {sys.version}")
print("=" * 80)

# 测试计数器
total_tests = 0
passed_tests = 0
failed_tests = []

def test_import(module_name, description=""):
    """测试导入模块"""
    global total_tests, passed_tests, failed_tests
    total_tests += 1
    try:
        __import__(module_name)
        print(f"✅ {module_name:30s} - 导入成功 {description}")
        passed_tests += 1
        return True
    except Exception as e:
        print(f"❌ {module_name:30s} - 导入失败: {e}")
        failed_tests.append((module_name, str(e)))
        return False

print("\n🔍 测试核心 Web 框架...")
print("-" * 80)
test_import("flask", "(Flask Web 框架)")
test_import("flask_cors", "(CORS 支持)")
test_import("waitress", "(WSGI 服务器)")
test_import("jinja2", "(模板引擎)")

print("\n🔍 测试数据科学包...")
print("-" * 80)
test_import("numpy", "(数值计算)")
test_import("pandas", "(数据处理)")
test_import("scipy", "(科学计算)")
test_import("sklearn", "(机器学习)")
test_import("joblib", "(模型序列化)")

print("\n🔍 测试数据库相关...")
print("-" * 80)
test_import("sqlalchemy", "(ORM)")
test_import("pymysql", "(MySQL 驱动)")

print("\n🔍 测试工具包...")
print("-" * 80)
test_import("requests", "(HTTP 客户端)")
test_import("dotenv", "(环境变量)")
test_import("apscheduler", "(任务调度)")
test_import("cryptography", "(加密)")

print("\n🔍 测试可视化...")
print("-" * 80)
test_import("matplotlib", "(绘图)")

print("\n" + "=" * 80)
print("\n🧪 测试关键功能...")
print("-" * 80)

# 测试 NumPy 基本操作
try:
    import numpy as np
    arr = np.array([1, 2, 3, 4, 5])
    result = np.where(arr > 3, arr, 0)
    assert list(result) == [0, 0, 0, 4, 5]
    print("✅ NumPy np.where() 功能正常")
    passed_tests += 1
    total_tests += 1
except Exception as e:
    print(f"❌ NumPy 功能测试失败: {e}")
    failed_tests.append(("numpy.where", str(e)))
    total_tests += 1

# 测试 Pandas 基本操作
try:
    import pandas as pd
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    df2 = pd.DataFrame({'c': [7, 8, 9]})
    result = df.merge(df2, how='cross')
    assert len(result) == 9
    print("✅ Pandas DataFrame 和 merge 功能正常")
    passed_tests += 1
    total_tests += 1
except Exception as e:
    print(f"❌ Pandas 功能测试失败: {e}")
    failed_tests.append(("pandas.merge", str(e)))
    total_tests += 1

# 测试 dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()  # 即使没有 .env 文件也不会报错
    print("✅ python-dotenv load_dotenv() 功能正常")
    passed_tests += 1
    total_tests += 1
except Exception as e:
    print(f"❌ dotenv 功能测试失败: {e}")
    failed_tests.append(("dotenv.load_dotenv", str(e)))
    total_tests += 1

# 测试 Flask
try:
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/test')
    def test():
        return 'OK'
    
    print("✅ Flask 应用创建和路由功能正常")
    passed_tests += 1
    total_tests += 1
except Exception as e:
    print(f"❌ Flask 功能测试失败: {e}")
    failed_tests.append(("flask.app", str(e)))
    total_tests += 1

# 测试 SQLAlchemy
try:
    from sqlalchemy import create_engine, text
    # 创建内存数据库测试
    engine = create_engine('sqlite:///:memory:')
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.fetchone()[0] == 1
    print("✅ SQLAlchemy 连接和查询功能正常")
    passed_tests += 1
    total_tests += 1
except Exception as e:
    print(f"❌ SQLAlchemy 功能测试失败: {e}")
    failed_tests.append(("sqlalchemy", str(e)))
    total_tests += 1

# 测试 requests
try:
    import requests
    # 不实际发送请求，只测试导入和基本功能
    session = requests.Session()
    print("✅ requests HTTP 客户端功能正常")
    passed_tests += 1
    total_tests += 1
except Exception as e:
    print(f"❌ requests 功能测试失败: {e}")
    failed_tests.append(("requests", str(e)))
    total_tests += 1

# 测试 APScheduler
try:
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    print("✅ APScheduler 任务调度器功能正常")
    passed_tests += 1
    total_tests += 1
except Exception as e:
    print(f"❌ APScheduler 功能测试失败: {e}")
    failed_tests.append(("apscheduler", str(e)))
    total_tests += 1

print("\n" + "=" * 80)
print("\n📊 测试结果汇总:")
print("-" * 80)
print(f"总测试数: {total_tests}")
print(f"✅ 通过: {passed_tests}")
print(f"❌ 失败: {len(failed_tests)}")
print(f"成功率: {(passed_tests/total_tests*100):.1f}%")

if failed_tests:
    print("\n❌ 失败的测试:")
    for name, error in failed_tests:
        print(f"  - {name}: {error}")
    sys.exit(1)
else:
    print("\n🎉 所有测试通过！项目已准备好使用 Python 3.14！")
    sys.exit(0)
