<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# AI 輔助工單管理系統

一個基於 Django 後端與 React 前端的智能工單管理系統，整合 Ollama AI 模型提供自動分類、優先級建議和智能回覆功能。

## ✨ 主要功能

- **智能工單分類**：利用 AI 自動分析工單內容，提供分類建議
- **優先級自動判定**：根據工單描述智能評估優先級（低、中、高、緊急）
- **AI 輔助回覆**：為客服人員生成專業且友善的回覆建議
- **完整工單管理**：建立、追蹤、分配和關閉工單
- **用戶權限管理**：支援多角色用戶系統
- **即時快取**：使用 Redis 提升 AI 服務效能


## 🛠 技術棧

### 後端

- **Django 4.2.16** - Web 框架
- **Django REST Framework** - API 開發
- **Ollama** - 本地 AI 模型服務
- **Redis** - 快取系統
- **SQLite** - 預設資料庫
- **JWT** - 身份驗證


### 前端

- **React 18** - 用戶介面框架
- **Ant Design** - UI 元件庫
- **Axios** - HTTP 請求處理
- **React Router** - 路由管理


### AI 整合

- **Ollama 本地部署**
- **LLaMA 3.2:3b** - 預設語言模型
- **智能快取機制**


## 📁 專案結構

```
ai-ticket-demo/
├── smart_helpdesk/          # Django 主要設定
│   ├── settings.py          # 專案設定檔
│   ├── urls.py             # URL 路由
│   └── wsgi.py             # WSGI 設定
├── tickets/                 # 工單應用程式
│   ├── models.py           # 資料模型
│   ├── services.py         # AI 服務整合
│   ├── views.py            # API 視圖
│   └── serializers.py      # 資料序列化
├── ticket-frontend/         # React 前端應用
│   ├── src/                # 原始碼
│   ├── package.json        # 依賴管理
│   └── public/             # 靜態資源
├── requirements.txt         # Python 依賴
├── manage.py               # Django 管理工具
└── .env                    # 環境變數設定
```


## 🚀 快速開始

### 1. 環境準備

確保系統已安裝：

- Python 3.8+
- Node.js 16+
- Redis
- Ollama


### 2. 安裝 Ollama 並下載模型

```bash
# 安裝 Ollama（依作業系統而異）
# Windows/macOS: 下載官方安裝程式
# Linux: curl -fsSL https://ollama.ai/install.sh | sh

# 下載並執行 LLaMA 模型
ollama pull llama3.2:3b
ollama serve
```


### 3. 後端設定

```bash
# 克隆專案
git clone https://github.com/civic881027/ai-ticket-demo.git
cd ai-ticket-demo

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝 Python 依賴
pip install -r requirements.txt

# 設定環境變數
cp .env.example .env  # 並修改相關設定

# 資料庫遷移
python manage.py migrate

# 建立超級用戶
python manage.py createsuperuser

# 啟動開發伺服器
python manage.py runserver
```


### 4. 前端設定

```bash
# 進入前端目錄
cd ticket-frontend

# 安裝 Node.js 依賴
npm install

# 啟動開發伺服器
npm start
```


### 5. 啟動 Redis

```bash
# 啟動 Redis 服務
redis-server
```


## ⚙️ 環境變數設定

在 `.env` 檔案中設定以下變數：

```env
SECRET_KEY=your-very-secret-key-here
DEBUG=True
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
REDIS_URL=redis://localhost:6379/1
```


## 🎯 主要功能模組

### 工單管理 (Ticket)

- **建立工單**：用戶可建立包含標題、描述、分類的工單
- **狀態追蹤**：開啟 → 處理中 → 已解決 → 已關閉
- **分配機制**：將工單分配給特定處理人員


### AI 智能服務 (OllamaService)

- **自動分類**：技術問題、帳戶問題、產品諮詢、投訴建議
- **優先級判定**：低、中、高、緊急四個等級
- **智能回覆**：生成專業客服回覆建議
- **快取優化**：避免重複 AI 計算，提升響應速度


### 用戶權限系統

- **角色區分**：管理員、客服人員、一般用戶
- **權限管理**：基於角色的存取控制
- **JWT 認證**：安全的身份驗證機制


## 🧪 測試

```bash
# 執行後端測試
python manage.py test

# 或使用 pytest
pytest

# 執行前端測試
cd ticket-frontend
npm test
```


## 📊 API 端點

主要 API 路由：

- `GET /api/tickets/` - 取得工單列表
- `POST /api/tickets/` - 建立新工單
- `GET /api/tickets/{id}/` - 取得特定工單
- `PUT /api/tickets/{id}/` - 更新工單
- `POST /api/tickets/{id}/ai-response/` - 生成 AI 回覆
- `POST /api/auth/login/` - 用戶登入
- `POST /api/auth/register/` - 用戶註冊


## 🤝 貢獻指南

1. Fork 此專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📝 授權條款

此專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 🆘 支援與問題回報

如有任何問題或建議，請透過以下方式聯繫：

- 建立 [GitHub Issue](https://github.com/civic881027/ai-ticket-demo/issues)
- 電子郵件：[您的聯繫郵箱]


## 🔄 版本歷史

- **v0.1.0** - 初始版本發布
    - 基本工單管理功能
    - Ollama AI 整合
    - React 前端介面

**注意**：此專案需要本地運行 Ollama 服務才能完整使用 AI 功能。請確保 Ollama 正確安裝並運行 LLaMA 3.2:3b 模型。

<div style="text-align: center">⁂</div>

[^1]: https://github.com/civic881027/ai-ticket-demo/tree/main

[^2]: https://github.com/civic881027/ai-ticket-demo/tree/main

[^3]: https://github.com/civic881027/ai-ticket-demo/blob/main/requirements.txt

[^4]: https://github.com/civic881027/ai-ticket-demo/blob/main/manage.py

[^5]: https://github.com/civic881027/ai-ticket-demo/blob/main/smart_helpdesk/settings.py

[^6]: https://github.com/civic881027/ai-ticket-demo/blob/main/tickets/models.py

[^7]: https://github.com/civic881027/ai-ticket-demo/blob/main/tickets/services.py

[^8]: https://github.com/civic881027/ai-ticket-demo/blob/main/ticket-frontend/package.json

[^9]: https://github.com/civic881027/ai-ticket-demo/blob/main/.env

