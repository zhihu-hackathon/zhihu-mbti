#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
auth router
'''

import os, secrets, json, time
from fastapi.routing import APIRouter
from sqlmodel import Session
from fastapi import Request, Response
from app.api.deps import DBSessionDep
from app.utils.http_client import SyncHttpClient
from app.db.session import UserSession
from fastapi.responses import RedirectResponse
from sqlmodel import select, update
from app.db.user import User
from app.utils.log import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="",
    tags=["Auth"]
)


# run llm in backend
def run_llm(base_url, sql_engine, uid, access_token):
    json_str = ''
    with SyncHttpClient(
        base_url=base_url,
        headers={'Authorization': f'Bearer {access_token}'}
    ) as client:
        resp = client.get('/user/moments')
        if 'data' in resp:
            json_str = json.dumps(resp['data'], ensure_ascii=False)
    system_prompt = f"""
    # Role: 知乎赛博心理学分析师 & 社交图谱分类专家

    # Objective:
    你现在的任务是接收一份知乎用户的“关注动态（Moments Feed）”的 JSON 数据。你需要深度分析该用户的交互动作（action_text）和浏览内容（target.title / target.excerpt），并基于预设的 18 种“知乎 SBTI 人设标签”，将该用户精准分类到其中 **唯一一个** 最符合的人设标签中。最后以严格的 JSON 格式输出结果。

    # Input Data Context (数据字段说明):
    你将收到的输入数据来源于知乎 OpenAPI，主要包含以下关键维度：
    - `action_text`: 用户的交互动作（如：赞同了回答、收藏了文章、关注了问题、回答了问题等）。反映了用户的**活跃度和行为模式**。
    - `target.title`: 目标内容的标题。反映了用户**关注的领域、热点或精神状态**。
    - `target.excerpt`: 目标内容的摘要。用于辅助判断内容调性（干货、八卦、爽文、情绪发泄等）。

    # 预设人设标签库及判定规则 (Mapping Rules):
    请严格按照以下规则，分析用户的 API 数据特征并进行匹配：

    1. 【赛博电子仓鼠/幻觉型卷王】
    - 行为特征: `action_text` 大量出现“收藏了文章”、“赞同了文章/回答”。
    - 内容特征: `title` 包含“干货、零基础、教程、提升自己、副业、赚钱、时间管理、自律”等关键词。
    2. 【全职吃瓜猹】
    - 行为特征: 频繁“关注了问题”、“赞同了回答”。
    - 内容特征: `title` 包含“如何看待、出轨、塌房、反转、大厂裁员、奇葩经历”等社会热点与八卦。
    3. 【野生纯血杠精】
    - 行为特征: 频繁在极具争议的问题下活动，或有“评论了回答/文章”的高频动作。
    - 内容特征: `title` 包含“为什么有人认为、事实真的是这样吗、打脸、逻辑”等辩论性较强的内容。
    4. 【纯血内耗圣体】
    - 行为特征: 大量阅读和赞同。
    - 内容特征: `title` 包含“迷茫、焦虑、抑郁、25岁/30岁、存款、失败、普通人、辞职”等情绪词汇。
    5. 【精神年薪百万】
    - 行为特征: 赞同和关注。
    - 内容特征: `title` 包含“年入百万、保时捷、阶层跨越、中产阶级、奢侈品、投行、财务自由”等炫富/精英话题。
    6. 【无效硬核学霸】
    - 行为特征: 赞同“文章”和长“回答”。
    - 内容特征: 极度硬核，如“量子力学、宏观经济、地缘政治、C++底层逻辑、航空航天”，常人难以看懂。
    7. 【顶级赛博街溜子】
    - 行为特征: 什么动作都有，数据极度杂乱无章。
    - 内容特征: `title` 极其跳跃，上一条是“如何评价拿破仑”，下一条是“猫咪为什么喜欢吃塑料”，毫无规律可言。
    8. 【佛系摸鱼吗喽】
    - 行为特征: 赞同、喜欢。
    - 内容特征: `title` 包含“摸鱼技巧、不想上班、躺平、牛马、搞笑动图、带薪拉屎”等反内卷内容。
    9. 【知识区捧哏大王】
    - 行为特征: `action_text` 只有“赞同了回答”，且频次极高。
    - 内容特征: 赞同的都是各个领域的万字长文干货，但自己几乎从不“回答”或“发表”。
    10. 【盐言爽文重度毒贩】
        - 行为特征: 赞同或阅读。
        - 内容特征: `title` 和 `excerpt` 明显是小说叙事，包含“真假千金、霸总、复仇、细思极恐、重生、我死后”等网文风格。
    11. 【互联网大清遗老】
        - 行为特征: 关注怀旧类问题。
        - 内容特征: `title` 包含“当年、老网民、贴吧、早期的知乎、一代人的回忆”等时代眼泪话题。
    12. 【互联网透明小透明】
        - 行为特征: 如果传入的 API `data` 数组极度稀疏，只有零星几次“关注”或“赞同”，极度边缘。
    13. 【评论区外交官】
        - 行为特征: `action_text` 包含“分享了回答/文章”，内容偏向高情商、人际交往、心理学科普。
    14. 【谢邀型表演艺术家】
        - 行为特征: `action_text` 包含“回答了问题”，且回答的内容标题偏向“有哪些令人惊艳的经历、分享你的神仙经历”。
    15. 【活体赛博菩萨】
        - 行为特征: `action_text` 中大量出现“回答了问题”。
        - 内容特征: `title` 是非常具体、冷门的求助帖（如“XX软件报错怎么解决”、“XX题目怎么做”），主动输出内容。
    16. 【无痕冲浪祖师爷】
        - 行为特征: 极其罕见！如果传入的 API `data` 数组直接是空的 `[]`，或者数据极少且年代久远，直接判定为此类！
    17. 【反骨型觉醒牛马】
        - 行为特征: 赞同、喜欢。
        - 内容特征: `title` 包含“资本家、剥削、整顿职场、劳动法、00后辞职”等极具攻击性的职场反叛话题。
    18. 【赛博盘串大爷】
        - 行为特征: 赞同传统文化、历史解密类问题。
        - 内容特征: `title` 包含“明朝那些事、历史真相、老规矩、局势分析、养生把玩”等。

    # Analysis Workflow (推理工作流):
    1. 数据清洗：检查传入的 `data` 是否为空。如果是空，直接返回【无痕冲浪祖师爷】。
    2. 词频提取：提取 `target.title` 和 `target.excerpt` 中的高频关键词。
    3. 动作统计：统计 `action_text` 中“赞同”、“收藏”、“回答”的比例。
    4. 综合匹配：将得出的特征与上述 18 个人设的规则进行比对，计算契合度，选出契合度最高的一个。

    # Output Format (输出格式要求):
    请务必只输出一个合法的 JSON 对象，不要包含任何 markdown 标记（如 ```json ），不要包含任何额外的解释文本。
    JSON 的结构必须如下所示：

    {{
    "persona_name": "选出的人设标签名称（必须是预设的18个之一）",
    "confidence_score": 85, // 0-100的置信度分数
    "extracted_keywords": ["提取到的关键词1", "提取到的关键词2"],
    "behavior_summary": "一句话总结该用户的知乎API行为特征",
    "reasoning": "结合API的 action_text 和 title 详细解释为什么将其判定为该人设（50字左右的生动分析，带点知乎幽默感）"
    }}

    # Input Data (用户动态JSON数据):
    {json_str}
    """
    llm_base_url = os.environ.get('LLM_BASE_URL')
    llm_api_key = os.environ.get('LLM_API_KEY')
    from openai import OpenAI

    client = OpenAI(
        api_key=llm_api_key,
        base_url=llm_base_url,
    )
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    res = None
    try:
        response = client.chat.completions.create(
            model="kimi-k2.6",
            messages=messages,
            timeout=500.0,
            response_format={'type': 'json_object'}
        )
        tmp = json.loads(response.choices[0].message.content)
        res = tmp['persona_name']
    except Exception as e:
        logger.error(f'llm error: {e}')
        res = None
    # update db result
    if res:
        with Session(sql_engine) as session:
            session.exec(update(User).where(User.uid == uid).values(tag=res))
            session.commit()

@router.get(
    path="/oauth/callback",
    summary="oauth callback"
)
def callback(request: Request, authorization_code: str, db_session: DBSessionDep, response: Response):
    '''
    handle oauth callback
    '''
    start = time.time()
    if not authorization_code:
        logger.warning('error code not exist')
        return RedirectResponse("/")
    session_id = request.cookies.get('session_id')
    user_session = db_session.exec(select(UserSession).where(UserSession.session_id == session_id)).first()
    if session_id and user_session:
        # logined
        logger.warning('user logged')
        return RedirectResponse("/")
    # get access token
    base_url = os.environ.get('ZHIHU_BASE_URL')
    app_base_url = os.environ.get('APP_BASE_URL')
    app_id = os.environ.get('ZHIHU_CLIENT_ID')
    app_key = os.environ.get('ZHIHU_CLIENT_SECRET')
    redirect_uri = f'{app_base_url}/api/oauth/callback'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    request_body = {
        'app_id': app_id,
        'app_key': app_key,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': authorization_code
    }
    access_token = None
    expires_in = None
    with SyncHttpClient(
        base_url=base_url,
        headers=headers
    ) as client:
        resp = client.post_data(path='/access_token', json=request_body)
        if 'access_token' in resp:
            access_token = resp['access_token']
            expires_in = resp['expires_in']
        else:
            logger.error(f"get access token failed with code: {resp['code']} and data: {resp['data']}")
    if not access_token or not expires_in:
        logger.warning('get access token failed')
        return RedirectResponse('/')
    else:
        # use token to get user info
        # write to db
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        with SyncHttpClient(
            base_url=base_url,
            headers=headers
        ) as client:
            resp = client.get(path='/user')
            if 'code' in resp or 'data' in resp:
                logger.error(f"get user info failed with code: {resp['code']} and data: {resp['data']}")
                return RedirectResponse('/')
            uid = resp['uid']
            # check user in table
            user = db_session.exec(select(User).where(User.uid == uid)).first()
            if not user:
                user = User(
                    uid=resp['uid'],
                    fullname=resp['fullname'],
                    gender=resp['gender'],
                    headline=resp['headline'],
                    description=resp['description'],
                    avatar_path=resp['avatar_path'],
                    phone_no=resp['phone_no'],
                    email=resp['email'],
                    access_token=access_token
                )
                db_session.add(user)
                db_session.commit()
                db_session.refresh(user)
            else:
                # update user access token
                user.access_token = access_token
                db_session.add(user)
                db_session.commit()
                db_session.refresh(user)
        session_id = secrets.token_urlsafe(32)
        # upsert the session info
        uid = user.uid
        user_session = db_session.exec(select(UserSession).where(UserSession.uid == uid)).first()
        if user_session:
            user_session.session_id = session_id
            user_session.expires_in = expires_in
        else:
            user_session = UserSession(
                uid=uid,
                session_id=session_id,
                expires_in=expires_in
            )
        db_session.add(user_session)
        db_session.commit()
        # update user tag
        if not user.tag:
            thread_pool_executor = request.app.state.thread_pool_executor
            sql_engine = request.app.state.sql_engine
            thread_pool_executor.submit(run_llm, base_url, sql_engine, user.uid, user.access_token)
        # save to cookie
        redirect = RedirectResponse(url='/', status_code=302)
        redirect.set_cookie(
            key='session_id',
            value=session_id,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=expires_in,
            path="/"
        )
        logger.warning(f'callback duration: {time.time() - start:.3f}s')
        return redirect

@router.post(
    path="/v1/auth/logout",
    summary="logout"
)
def logout(request: Request, response: Response, db_session: DBSessionDep):
    """logout"""
    # delete data in session
    session_id = request.cookies.get("session_id")
    user_session = db_session.exec(select(UserSession).where(UserSession.session_id == session_id)).first()
    if session_id and user_session:
        # delete session
        logger.warning('logout session is not null')
        db_session.delete(user_session)
        db_session.commit()
    redirect = RedirectResponse(url='/', status_code=302)
    redirect.delete_cookie("session_id")
    return redirect

# get auth status to update front-end
@router.get(
    path="/v1/auth/status",
    summary="check auth status",
    response_model_exclude_none=True
)
def get_auth_status(request: Request, db_session: DBSessionDep):
    session_id = request.cookies.get("session_id")
    logger.warning(f'当前session id is {session_id}')
    user_session = db_session.exec(select(UserSession).where(UserSession.session_id == session_id)).first()
    if session_id and user_session:
       # get user info
       logger.warning(f'当前session id is {session_id} 以及 user session: {user_session}')
       user = db_session.exec(select(User).where(User.uid == user_session.uid)).first()
       if user:
            return {'auth': True, 'user': {
                'id': user.uid,
                'name': user.fullname,
                'gender': user.gender,
                'headline': user.headline,
                'avatar': user.avatar_path,
                'description': user.description,
                'tag': user.tag or ''
            }}
       else:
            logger.warning(f'当前user 为空 结果 session id is {session_id} 以及 user session: {user_session}')
            return {'auth': False, 'user': None}
    logger.warning(f'当前false结果 session id is {session_id} 以及 user session: {user_session}')
    return {'auth': False, 'user': None}