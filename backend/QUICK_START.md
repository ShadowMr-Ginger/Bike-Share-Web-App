# 🚀 快速开始指南（5分钟完成）

## 📋 你需要做的事情

### 第 1 步：安装 MySQL（如果还没有）

#### Windows:
1. 下载 MySQL：https://dev.mysql.com/downloads/installer/
2. 运行安装程序，选择 "Developer Default"
3. 设置 root 密码（记住这个密码！）
4. 完成安装

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

#### Mac:
```bash
brew install mysql
brew services start mysql
```

### 第 2 步：配置 .env 文件

**我已经帮你创建了 `.env` 文件！**

你只需要修改一个地方：

```bash
# 打开 .env 文件
notepad .env  # Windows
# 或
nano .env     # Linux/Mac
```

**修改这一行：**
```env
DB_PASSWORD=        # 改成你的 MySQL root 密码
```

例如，如果你的 MySQL root 密码是 `mypassword123`：
```env
DB_PASSWORD=mypassword123
```

**其他配置说明：**
- `DB_USER=root` - 默认用户，不用改
- `DB_PORT=3306` - 默认端口，不用改
- `DB_NAME=local_databasejcdecaux` - 数据库名，不用改
- `DB_URI=127.0.0.1` - 本地地址，不用改
- API 密钥 - 暂时可以留空，后面需要时再填

### 第 3 步：安装 Python 依赖

```bash
# 如果使用虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate  # Windows
# 或
source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt
```

### 第 4 步：初始化数据库

```bash
python init_database.py
```

**你会看到：**
```
🚀 数据库初始化脚本
======================================================================

📋 当前配置:
   数据库用户: root
   数据库地址: 127.0.0.1
   数据库端口: 3306
   数据库名称: local_databasejcdecaux
   密码: 已设置

🔍 步骤 1: 测试 MySQL 服务器连接...
   ✅ MySQL 服务器连接成功！

🔍 步骤 2: 创建数据库 'local_databasejcdecaux'...
   ✅ 数据库 'local_databasejcdecaux' 创建成功！

🔍 步骤 3: 创建数据表...
   📋 创建 station 表...
   📋 创建 availability 表...
   ...
   ✅ 所有数据表创建成功！

🔍 步骤 4: 验证数据库设置...
   ✅ 数据库设置验证成功！

🎉 数据库初始化完成！
```

### 第 5 步：启动应用

```bash
python run.py
```

**成功！** 🎉

应用会在 `http://localhost:5000` 运行

---

## ❌ 如果遇到问题

### 问题 1: MySQL 连接失败

**检查 MySQL 是否运行：**

Windows:
```cmd
# 打开服务管理器
services.msc
# 找到 MySQL 服务，确保它正在运行
```

Linux:
```bash
sudo systemctl status mysql
sudo systemctl start mysql
```

Mac:
```bash
brew services list
brew services start mysql
```

### 问题 2: 密码错误

**重置 MySQL root 密码：**

```bash
# 登录 MySQL
mysql -u root -p

# 如果无法登录，说明密码不对
# 需要重置密码（搜索 "MySQL reset root password"）
```

### 问题 3: 端口被占用

**检查 3306 端口：**

Windows:
```cmd
netstat -ano | findstr :3306
```

Linux/Mac:
```bash
sudo lsof -i :3306
```

---

## 🎯 完整流程总结

```bash
# 1. 确保 MySQL 正在运行
# Windows: 检查服务管理器
# Linux: sudo systemctl status mysql

# 2. 修改 .env 文件中的 DB_PASSWORD

# 3. 安装依赖
pip install -r requirements.txt

# 4. 初始化数据库
python init_database.py

# 5. 启动应用
python run.py
```

---

## 📝 .env 文件完整示例

```env
# 数据库配置
DB_USER=root
DB_PASSWORD=your_mysql_password_here  # ⬅️ 改这里！
DB_PORT=3306
DB_NAME=local_databasejcdecaux
DB_URI=127.0.0.1

# API 密钥（暂时可以留空）
BIKE_API_KEY=
GOOGLE_KEY=
ORS_KEY=

# Flask 密钥
FLASK_SECRET_KEY=your-secret-key-change-this-in-production-2026
```

---

## 💡 提示

1. **MySQL 密码**：如果你刚安装 MySQL，密码可能是空的，那就保持 `DB_PASSWORD=` 不填
2. **API 密钥**：应用的某些功能需要 API 密钥，但基本功能可以先运行
3. **虚拟环境**：强烈建议使用虚拟环境，避免包冲突

---

## ✅ 检查清单

- [ ] MySQL 已安装
- [ ] MySQL 服务正在运行
- [ ] `.env` 文件中的 `DB_PASSWORD` 已设置
- [ ] Python 依赖已安装
- [ ] `python init_database.py` 运行成功
- [ ] `python run.py` 启动成功

**全部完成？恭喜！** 🎊

你的后端现在应该在 `http://localhost:5000` 运行了！
