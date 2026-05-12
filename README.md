# Zhihu Labeler

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
| `ZHIHU_AUTH_URL` | 知乎oauth授权页 |
| `ZHIHU_TOKEN_URL` | 知乎access token api |
| `ZHIHU_API_BASE` | 知乎开放平台api base |
| `APP_BASE_URL` | 应用部署地址（默认 http://localhost:8080） |

## 部署到 Vercel

1. 推送代码到 GitHub
2. 在 Vercel 导入项目
3. 在 Vercel 项目设置中配置环境变量
4. 部署

## 功能

- 知乎 OAuth2 登录
- 获取关注列表
- 自定义标签分类
- 按标签筛选
