# 🚀 超级简单快速开始指南（2分钟完成）

## ✨ 使用 SQLite - 无需安装 MySQL！

---

## 📋 你需要做的事情

### 第 1 步：安装 Python 依赖

```bash
# 如果使用虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate  # Windows
# 或
source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt
```

### 第 2 步：初始化数据库

```bash
python init_database.py
```

**你会看到：**
```
🚀 SQLite 数据库初始化脚本
======================================================================

✨ 使用 SQLite - 无需安装 MySQL！

📋 当前配置:
   数据库类型: SQLite
   数据库路径: data/bike_share.db
   数据库大小: 将创建

🔍 步骤 1: 创建 SQLite 数据库...
   ✅ SQLite 数据库连接成功！

🔍 步骤 2: 创建数据表...
   📋 创建 station 表...
   📋 创建 availability 表...
   ...
   ✅ 所有数据表创建成功！

🔍 步骤 3: 验证数据库设置...
   ✅ 数据库设置验证成功！

🎉 数据库初始化完成！
```

### 第 3 步：启动应用

```bash
python run.py
```

**成功！** 🎉

应用会在 `http://localhost:5000` 运行

---

## 🎯 完整流程总结（超级简单）

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 初始化数据库（自动创建 SQLite 数据库）
python init_database.py

# 3. 启动应用
python run.py
```

**就这么简单！无需安装 MySQL！** 🎊

---

## 📝 配置说明

### .env 文件（已经配置好了）

```env
# 数据库配置 - SQLite（无需安装 MySQL！）
DB_PATH=data/bike_share.db

# API 密钥（暂时可以留空）
BIKE_API_KEY=
GOOGLE_KEY=
ORS_KEY=

# Flask 密钥
FLASK_SECRET_KEY=your-secret-key-change-this-in-production-2026
```

**你不需要修改任何配置！** 直接运行即可。

---

## 💡 为什么选择 SQLite？

✅ **无需安装数据库服务器** - SQLite 是文件数据库  
✅ **零配置** - 开箱即用  
✅ **轻量级** - 适合中小型应用  
✅ **跨平台** - Windows/Linux/Mac 都支持  
✅ **完全免费** - 无需任何许可证  

---

## 📊 数据库文件位置

数据库文件会自动创建在：
```
backend/data/bike_share.db
```

你可以使用任何 SQLite 客户端查看数据：
- [DB Browser for SQLite](https://sqlitebrowser.org/) (推荐)
- [SQLite Studio](https://sqlitestudio.pl/)
- VS Code 扩展：SQLite Viewer

---

## ❌ 如果遇到问题

### 问题 1: 依赖安装失败

```bash
# 升级 pip
python -m pip install --upgrade pip

# 重新安装
pip install -r requirements.txt
```

### 问题 2: 数据库初始化失败

```bash
# 删除旧数据库文件
rm data/bike_share.db  # Linux/Mac
del data\bike_share.db  # Windows

# 重新初始化
python init_database.py
```

### 问题 3: 端口被占用

```bash
# 检查 5000 端口
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # Linux/Mac

# 修改端口（在 run.py 中）
```

---

## 🔄 从 MySQL 迁移到 SQLite

如果你之前使用 MySQL，现在已经自动切换到 SQLite：

**变化：**
- ❌ 不再需要 MySQL 服务器
- ❌ 不再需要配置数据库用户名/密码
- ✅ 数据库文件直接存储在 `data/` 目录
- ✅ 更简单、更快速

**数据迁移：**
如果需要迁移旧数据，可以使用 SQLite 导入工具或手动导入。

---

## ✅ 检查清单

- [ ] Python 3.13+ 已安装
- [ ] 依赖已安装 (`pip install -r requirements.txt`)
- [ ] 数据库已初始化 (`python init_database.py`)
- [ ] 应用可以启动 (`python run.py`)

**全部完成？恭喜！** 🎊

你的后端现在应该在 `http://localhost:5000` 运行了！

---

## 🚀 下一步

1. **测试 API**：访问 `http://localhost:5000`
2. **查看数据库**：使用 DB Browser 打开 `data/bike_share.db`
3. **配置 API 密钥**：在 `.env` 文件中添加你的 API 密钥
4. **部署到服务器**：直接复制整个项目即可

---

## 📚 相关文档

- `init_database.py` - 数据库初始化脚本
- `database/db_setup.py` - 数据库设置模块
- `.env` - 环境变量配置
- `requirements.txt` - Python 依赖（Python 3.14 兼容）

---

## 🎉 总结

**使用 SQLite 后，部署变得超级简单：**

1. 安装依赖
2. 初始化数据库
3. 启动应用

**无需安装 MySQL，无需复杂配置！** 🎊
