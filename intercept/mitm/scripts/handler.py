import asyncio
import redis.asyncio as redis
from sqlalchemy import select, update
from datetime import datetime


from db import redis_pool, async_db_session
from model import TencentNewsArticle, TencentNewsComment


async def articles_handler(client_ip: str, json_data: dict):
    article_obj = TencentNewsArticle(
        data_created_time=datetime.now(), article_id=json_data["id"], title=json_data["title"],
        category=json_data.get("news_category_name", None),
        cate1_name=json_data["category_unified"]["cate1_name"],
        cate2_name=json_data["category_unified"]["cate2_name"],
        article_source=json_data["source"], article_publish_location=json_data["userAddress"],
        article_content=json_data["content"]["text"]
    )

    async with async_db_session() as db_session, db_session.begin(), redis.Redis.from_pool(redis_pool) as redis_conn:
        if await db_session.scalar(select(TencentNewsArticle)
                                .where(TencentNewsArticle.article_id == json_data["id"])) is None:
            article_obj.client_mac = await redis_conn.get(f"ip:{client_ip}")
            db_session.add(article_obj)


async def comments_handler(client_ip: str, comments_data: list[dict]):
    article_id = comments_data[0][0]["article_id"]
    await asyncio.sleep(3)
    async with async_db_session() as db_session, db_session.begin():
        if await db_session.scalar(select(TencentNewsArticle)
                                   .where(TencentNewsArticle.article_id == article_id)) is None: return

    comment_list: dict[int, TencentNewsComment] = {}
    for comment in comments_data:
        comment = comment[0]
        comment_obj = TencentNewsComment(
            comment_post_time=datetime.fromtimestamp(comment["pub_time"]),
            reply_id=comment["reply_id"], referer_article_id=comment["article_id"],
            comment_content=comment["reply_content"], agree_count=comment.get("agree_count", 0),
            user_name=comment["nick"], user_location=comment["province_city"][:-2]
        )
        comment_list[comment["reply_id"]] = comment_obj
        if "reply_list" in comment:
            for reply in comment["reply_list"]:
                reply = reply[0]
                reply_obj = TencentNewsComment(
                    comment_post_time=datetime.fromtimestamp(reply["pub_time"]),
                    reply_id=reply["reply_id"], referer_article_id=reply["article_id"],
                    comment_content=reply["reply_content"], agree_count=reply.get("agree_count", 0),
                    user_name=reply["nick"], user_location=reply["province_city"][:-2]
                )
                reply_obj.reply_parent_id = reply["parentid"]
                comment_list[reply["reply_id"]] = reply_obj

    async with async_db_session() as db_session, db_session.begin(), redis.Redis.from_pool(redis_pool) as redis_conn:
        for comment in [comment_list.get(i) for i in comment_list]:
            if await db_session.scalar(select(TencentNewsComment)
                                    .where(TencentNewsComment.reply_id == comment.reply_id)) is None:
                comment.client_mac = await redis_conn.get(f"ip:{client_ip}")
                db_session.add(comment)
        await db_session.execute(update(TencentNewsArticle)
                                 .where(TencentNewsArticle.article_id == article_id).values(comments_recorded=True))
