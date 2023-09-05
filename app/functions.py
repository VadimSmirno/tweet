import logging
import os

from sqlalchemy.exc import OperationalError
from sqlalchemy.future import select
from fastapi import HTTPException, Header

from models import Users, Tweets, Medias, FollowersAndFollowings
from database import session


logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel('DEBUG')

UPLOAD_FOLDER = os.path.abspath("static/images")
ALLOWED_EXTENSIONS = ["jpeg", "jpg", "png", "webp"]


async def check_data_in_db(database):
    async with session.begin():
        data = select(database)
        res = await session.execute(data)
        return res.all()


async def check_api_key(api_key: str = Header(None)):
    api_keys_list = []
    users_id_list = []
    async with session.begin():
        users_data = (select(Users.id, Users.user_api_key))
        res = await session.execute(users_data)
        users = res.all()
        for user in users:
            api_keys_list.append(user.user_api_key)
            users_id_list.append(user.id)
    if api_key != "test" and api_key not in api_keys_list:
        raise HTTPException(status_code=403, detail="Invalid API key")


async def get_user_id(api_key: str):
    async with session.begin():
        users_data = (select(Users.id).where(Users.user_api_key == api_key))
        res = await session.execute(users_data)
        users_id = res.one_or_none()
        if users_id:
            return users_id[0]


async def get_user_by_id(user_id: int):
    async with session.begin():
        users_data = select(Users.id).where(Users.id == user_id)
        res = await session.execute(users_data)
        users_id = res.one_or_none()
        return users_id[0]


async def get_tweet_by_id(tweet_id: int):
    async with session.begin():
        users_data = select(Tweets.id).where(Tweets.id == tweet_id)
        res = await session.execute(users_data)
        tweet_id = res.one_or_none()
        if tweet_id:
            return tweet_id[0]


async def check_file_extension(user_id: int, filename: str):
    extension = filename.split(".")[-1]
    if extension in ALLOWED_EXTENSIONS:
        filename = f"user_{user_id}_" + filename
        return filename
    logger.error("Invalid a type of the file.")


async def check_tweet_attachments(attachments: list[int]):
    query = select(Medias.id, Medias.filename)
    res = await session.execute(query)
    medias = res.all()
    result_media_ids = [media[1] for media in medias if media[0] in attachments]
    return result_media_ids


async def get_user_data(user_id: int):
    data = {}

    try:
        async with session.begin():
            query = select(Users.id, Users.name).where(Users.id == user_id)
            users = await session.execute(query)
            user = users.one_or_none()

        if user:
            async with session.begin():
                query = select(FollowersAndFollowings.follower_id, Users.name).\
                    join(Users, FollowersAndFollowings.follower_id == Users.id).\
                    filter(FollowersAndFollowings.following_id == user_id)
                followers_list = []
                res = await session.execute(query)
                followers = res.all()
                for follower in followers:
                    followers_list.append(
                        {
                            "id": follower[0],
                            "name": follower[1],
                        }
                    )

            async with session.begin():
                query = select(FollowersAndFollowings.following_id, Users.name).\
                    join(Users, FollowersAndFollowings.following_id == Users.id).\
                    filter(FollowersAndFollowings.follower_id == user_id)
                followings_list = []
                res = await session.execute(query)
                followings = res.all()
                for following in followings:
                    followings_list.append(
                        {
                            "id": following[0],
                            "name": following[1],
                        }
                    )

            data = {
                "id": user[0],
                "name": user[1],
                "followers": followers_list,
                "followings": followings_list,
            }
        else:
            logger.error(f"The user not found.")
            data = None

    except OperationalError:
        logger.error("The database not found.")
    return data
