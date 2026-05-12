# Zhihu MBTI

给你的知乎关注列表打标签，轻松管理关注的人。

## 快速开始

```bash
# 安装依赖
npm install

# 配置环境变量
cp .env.example .env.local
# 编辑 .env.local 填入知乎开放平台的 Client ID 和 Secret

# 启动开发服务器
npm run dev
```

## 环境变量

| 变量名 | 说明 |
|--------|------|
| `ZHIHU_CLIENT_ID` | 知乎开放平台 Client ID |
| `ZHIHU_CLIENT_SECRET` | 知乎开放平台 Client Secret |
| `ZHIHU_BASE_URL` | 知乎开放平台 base url |
| `ZHIHU_DATA_BASE_URL` | 知乎数据平台 base url |
| `APP_BASE_URL` | 应用部署地址（默认 http://localhost:8080） |

## 功能

- 知乎 OAuth2 登录
- 获取关注列表
- 自定义标签分类
- 按标签筛选
