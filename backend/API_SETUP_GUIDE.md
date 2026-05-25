# 🔑 API 密钥配置指南

## 📋 需要的 API 密钥

你的应用需要 3 个 API 密钥：

1. **BIKE_API_KEY** - JCDecaux 自行车数据 API
2. **GOOGLE_KEY** - Google Maps API（地理编码）
3. **ORS_KEY** - OpenRouteService API（路线规划）

---

## 🚀 快速配置

### 1. JCDecaux Bike API Key

**用途：** 获取都柏林自行车站点的实时数据

**如何获取：**

1. 访问：https://developer.jcdecaux.com/
2. 点击 "Sign Up" 注册账号
3. 登录后，点击 "API Keys"
4. 创建新的 API Key
5. 复制 API Key

**免费额度：** 每天 5,000 次请求（足够使用）

**配置：**
```env
BIKE_API_KEY=你的JCDecaux_API_Key
```

---

### 2. Google Maps API Key

**用途：** 地理编码（地址转换为经纬度）

**如何获取：**

1. 访问：https://console.cloud.google.com/
2. 创建新项目或选择现有项目
3. 启用 "Geocoding API"
   - 在左侧菜单选择 "APIs & Services" > "Library"
   - 搜索 "Geocoding API"
   - 点击 "Enable"
4. 创建凭据
   - 在左侧菜单选择 "APIs & Services" > "Credentials"
   - 点击 "Create Credentials" > "API Key"
   - 复制 API Key

**免费额度：** 每月 $200 免费额度（约 40,000 次请求）

**配置：**
```env
GOOGLE_KEY=你的Google_API_Key
```

**重要：** 建议限制 API Key 的使用范围：
- 在 API Key 设置中，限制为只能使用 "Geocoding API"
- 可以限制 HTTP referrer 或 IP 地址

---

### 3. OpenRouteService API Key

**用途：** 计算自行车路线

**如何获取：**

1. 访问：https://openrouteservice.org/
2. 点击 "Sign Up" 注册账号
3. 登录后，进入 Dashboard
4. 点击 "Request a Token"
5. 复制 API Key

**免费额度：** 每天 2,000 次请求

**配置：**
```env
ORS_KEY=你的OpenRouteService_API_Key
```

---

## 📝 完整的 .env 文件示例

```env
# 数据库配置 - SQLite（无需安装 MySQL！）
DB_PATH=data/bike_share.db

# API 密钥
BIKE_API_KEY=your_jcdecaux_api_key_here
GOOGLE_KEY=your_google_api_key_here
ORS_KEY=your_openrouteservice_api_key_here

# Flask 密钥
FLASK_SECRET_KEY=your-secret-key-change-this-in-production-2026
```

---

## 🔍 哪些功能需要哪些 API？

| 功能 | 需要的 API | 是否必需 |
|------|-----------|---------|
| 获取自行车站点数据 | BIKE_API_KEY | ✅ 必需 |
| 地址搜索/地理编码 | GOOGLE_KEY | ⚠️ 可选 |
| 路线规划 | ORS_KEY | ⚠️ 可选 |
| 基本站点显示 | 无 | - |

---

## ⚡ 快速测试（不配置 API）

如果你只想快速测试应用，可以：

1. **暂时不配置 API 密钥**
2. **使用模拟数据或手动添加站点数据**

但是以下功能会受限：
- ❌ 无法自动获取实时自行车数据
- ❌ 无法使用地址搜索
- ❌ 无法计算路线

---

## 🛠️ 配置步骤

### 步骤 1: 编辑 .env 文件

```bash
# Windows
notepad .env

# Linux/Mac
nano .env
```

### 步骤 2: 填入 API 密钥

```env
BIKE_API_KEY=abc123def456...
GOOGLE_KEY=xyz789ghi012...
ORS_KEY=mno345pqr678...
```

### 步骤 3: 保存并重启应用

```bash
# 停止应用（Ctrl+C）
# 重新启动
python run.py
```

---

## 🧪 测试 API 配置

### 测试 JCDecaux API

```bash
curl "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=YOUR_API_KEY"
```

### 测试 Google Geocoding API

```bash
curl "https://maps.googleapis.com/maps/api/geocode/json?address=Dublin&key=YOUR_API_KEY"
```

### 测试 OpenRouteService API

```bash
curl -X POST "https://api.openrouteservice.org/v2/directions/cycling-regular/geojson" \
  -H "Authorization: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"coordinates":[[-6.26,53.35],[-6.25,53.34]]}'
```

---

## 💰 费用说明

| API | 免费额度 | 超出后费用 |
|-----|---------|-----------|
| JCDecaux | 5,000 次/天 | 需联系 |
| Google Maps | $200/月 | 按使用量计费 |
| OpenRouteService | 2,000 次/天 | 需升级套餐 |

**对于开发和小规模使用，免费额度完全足够！** ✅

---

## ❓ 常见问题

### Q1: 我必须配置所有 3 个 API 吗？

**A:** 
- **BIKE_API_KEY** - 强烈建议配置，否则无法获取实时数据
- **GOOGLE_KEY** - 可选，用于地址搜索
- **ORS_KEY** - 可选，用于路线规划

### Q2: API 密钥会过期吗？

**A:** 通常不会，但建议定期检查 API 控制台

### Q3: 如何保护 API 密钥？

**A:** 
- ✅ 不要提交 .env 文件到 Git
- ✅ 在 API 控制台设置使用限制
- ✅ 定期轮换密钥
- ✅ 监控 API 使用量

### Q4: 免费额度用完了怎么办？

**A:** 
- 等待第二天重置（每日限额）
- 或升级到付费套餐
- 或优化 API 调用频率

---

## 🎯 推荐配置顺序

1. **先配置 BIKE_API_KEY** - 这是最重要的
2. **测试应用是否能获取自行车数据**
3. **再配置其他 API**（如果需要）

---

## 📚 相关链接

- [JCDecaux Developer Portal](https://developer.jcdecaux.com/)
- [Google Cloud Console](https://console.cloud.google.com/)
- [OpenRouteService](https://openrouteservice.org/)
- [Google Maps API 定价](https://mapsplatform.google.com/pricing/)

---

## ✅ 配置完成检查清单

- [ ] 注册 JCDecaux 账号并获取 API Key
- [ ] 注册 Google Cloud 并启用 Geocoding API
- [ ] 注册 OpenRouteService 并获取 Token
- [ ] 在 .env 文件中填入所有 API 密钥
- [ ] 重启应用
- [ ] 测试自行车数据获取功能
- [ ] 测试地址搜索功能（如果配置了）
- [ ] 测试路线规划功能（如果配置了）

---

## 🎉 完成！

配置好 API 密钥后，你的应用就可以：
- ✅ 获取实时自行车站点数据
- ✅ 搜索地址并定位
- ✅ 规划自行车路线
- ✅ 显示站点可用性

**祝你使用愉快！** 🚴‍♂️
