# 知否知否 · Zhihu MBTI

> AI 驱动的知乎人格画像引擎 — 基于用户行为数据的 LLM 深度推理，为你生成 16 种赛博人设标签

**知否知否** 是一款基于知乎开放平台构建的 AI 人格分析应用。它通过 OAuth2 获取用户的知乎关注动态（Moments Feed），利用大语言模型对用户的行为模式和内容偏好进行深度语义分析，最终将用户精准归类到 16 种预设的「赛博人设标签」中。

## AI 核心架构

### 整体流水线

```
知乎 OpenAPI (Moments Feed)
        │
        ▼
  ┌─────────────┐
  │  数据采集层   │  ← OAuth2 鉴权 → /user/moments
  └──────┬──────┘
         │  JSON (action_text / target.title / target.excerpt)
         ▼
  ┌─────────────┐
  │  LLM 推理层  │  ← Structured Prompt + JSON Mode
  └──────┬──────┘
         │  persona_name / confidence_score / reasoning
         ▼
  ┌─────────────┐
  │  结果持久层   │  ← SQLite (SQLModel ORM)
  └─────────────┘
```

### AI Prompt Engineering

系统 Prompt 采用 **结构化角色扮演 + 规则映射 + CoT 推理工作流** 三段式设计：

| 模块 | 设计思路 |
|------|---------|
| **Role Definition** | 赋予 LLM 「赛博心理学分析师 & 社交图谱分类专家」角色，激活深度分析能力 |
| **Mapping Rules** | 18 种人设标签，每种标签定义了行为特征（action_text 频次分布）+ 内容特征（title/excerpt 关键词）双维度判定规则 |
| **Analysis Workflow** | 强制 4 步推理链：数据清洗 → 词频提取 → 动作统计 → 综合匹配，确保推理可追溯 |
| **JSON Mode** | 启用 `response_format={'type': 'json_object'}` 强制结构化输出，输出包含 persona_name / confidence_score / extracted_keywords / behavior_summary / reasoning 五个字段 |

## 16 种赛博人设标签

| # | 人设标签 | 行为画像 |
|---|---------|---------|
| 1 | 赛博电子仓鼠 / 幻觉型卷王 | 疯狂收藏干货教程，永远在"提升自己"的路上 |
| 2 | 全职吃瓜猹 | 追热点比记者还快，塌房反转一个不落 |
| 3 | 野生纯血杠精 | 专挑争议问题，逻辑链比论文还长 |
| 4 | 纯血内耗圣体 | 凌晨三点还在刷"25岁存款多少正常" |
| 5 | 精神年薪百万 | 关注的全是保时捷和阶层跨越，现实月入八千 |
| 6 | 无效硬核学霸 | 量子力学和地缘政治信手拈来，但跟生活毫无关系 |
| 7 | 顶级赛博街溜子 | 上一秒拿破仑，下一秒猫咪吃塑料，无规律可言 |
| 8 | 佛系摸鱼吗喽 | 专搜带薪拉屎和躺平攻略的反内卷斗士 |
| 9 | 知识区捧哏大王 | 只赞同从不回答，万字长文最佳观众 |
| 10 | 盐言爽文重度毒贩 | 真假千金霸总复仇，网文胃口深不见底 |
| 11 | 互联网大清遗老 | 怀念贴吧和早期知乎的时代眼泪收集者 |
| 12 | 互联网透明小透明 | 数据极度稀疏，几乎不产生交互 |
| 13 | 评论区外交官 | 分享高情商内容，人际关系学民间博士 |
| 14 | 谢邀型表演艺术家 | "谢邀，人在美国"，表演型回答达人 |
| 15 | 活体赛博菩萨 | 冷门求助帖的救世主，主动输出无怨无悔 |
| 16 | 无痕冲浪祖师爷 | 数据为空或极度久远，互联网幽灵 |



## 技术栈

| 层级 | 技术 |
|------|------|
| **Web 框架** | FastAPI (Python 3.11+) |
| **AI/LLM** | OpenAI SDK (兼容任意 OpenAI API 格式的 LLM 服务，默认 Kimi K2.6) |
| **数据库** | SQLite + SQLModel ORM |
| **模板引擎** | Jinja2 (SSR) |
| **HTTP Client** | httpx + tenacity (指数退避重试 + Jitter 防惊群) |
| **包管理** | uv |
| **容器化** | Docker + docker-compose |


## 项目结构

```
zhihu-mbti/
├── app/
│   ├── main.py                  # FastAPI 入口，生命周期管理
│   ├── api/
│   │   ├── deps.py              # 依赖注入 (DB Session / 当前用户)
│   │   └── routers/
│   │       ├── auth.py          # OAuth2 登录/回调/登出 + LLM 后台推理
│   │       ├── search.py        # 实时 LLM 人格分析接口
│   │       ├── quiz.py          # 问卷鉴定接口 (WIP)
│   │       ├── db.py            # 数据管理 & LLM 调试接口
│   │       └── index.py         # 首页 SSR 渲染
│   ├── db/
│   │   ├── user.py              # User 表模型
│   │   └── session.py           # UserSession 表模型
│   ├── models/
│   │   └── user.py              # Pydantic 请求模型
│   ├── templates/
│   │   └── index.html           # 单页应用 (含 16 人设卡片 / 结果页 / 动画)
│   └── utils/
│       ├── http_client.py       # 同步/异步 HTTP 客户端 (自动重试)
│       ├── tools.py             # 签名生成 / 时间戳工具
│       └── log.py               # 日志配置
├── data/
│   └── database.db              # SQLite 数据文件
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── .env.example
```

## 快速开始

### 环境准备

```bash
# 克隆仓库
git clone https://github.com/zhihu-hackathon/zhihu-mbti.git
cd zhihu-mbti

# 安装依赖 (需要 Python 3.11+)
uv sync

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入相关配置
```

### 环境变量

| 变量名 | 说明 |
|--------|------|
| `ZHIHU_CLIENT_ID` | 知乎开放平台 Client ID |
| `ZHIHU_CLIENT_SECRET` | 知乎开放平台 Client Secret |
| `ZHIHU_BASE_URL` | 知乎开放平台 API Base URL |
| `ZHIHU_DATA_BASE_URL` | 知乎数据平台 Base URL |
| `ZHIHU_USER_SECRET` | 知乎用户签名密钥 |
| `APP_BASE_URL` | 应用部署地址 (默认 `http://localhost:8080`) |
| `LLM_BASE_URL` | LLM 服务 API Base URL (兼容 OpenAI API 格式) |
| `LLM_API_KEY` | LLM 服务 API Key |

### 本地开发

```bash
fastapi run app/main.py --host 0.0.0.0 --port 8080
```

### Docker 部署

```bash
docker-compose up -d
```

## AI 设计细节

### Prompt 架构

系统 Prompt 是整个 AI 推理的核心，采用以下设计模式：

- **角色锚定 (Role Anchoring)** — 明确 LLM 的角色为「赛博心理学分析师」，限定分析范围和输出风格
- **双维度映射 (Dual-Dimension Mapping)** — 每种人设标签定义了 `行为特征` (action_text 频次分布) 和 `内容特征` (title/excerpt 关键词) 两个判定维度，避免单一维度误判
- **强制推理链 (Chain-of-Thought)** — 通过 4 步 Analysis Workflow 强制 LLM 进行结构化推理，而非直接输出结论
- **结构化输出 (Structured Output)** — 启用 JSON Mode，输出格式严格约束为包含 confidence_score 和 reasoning 的 JSON 对象，便于下游消费

### LLM 兼容性

项目使用 OpenAI SDK，通过 `LLM_BASE_URL` 和 `LLM_API_KEY` 环境变量配置，兼容所有符合 OpenAI Chat Completions API 格式的 LLM 服务：

- Moonshot Kimi (默认: `kimi-k2.6`)
- DeepSeek
- 通义千问
- OpenAI GPT 系列
- 任何兼容 OpenAI API 格式的本地/云端模型
