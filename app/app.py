from os import environ
from typing import List

import aiofiles
import uvicorn
from fastapi import FastAPI, UploadFile
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from functions import *
from schemas import *
from database import *
from models import User, FollowersAndFollowing, Tweet, Like, Media

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel("DEBUG")

app = FastAPI()

testing = environ.get("TESTING")


@app.get("/ping")
def pong():
    return {"ping": "pong!"}


@app.post("/api/users", response_model=UsersBase)
async def add_user(user: UsersCreate, api_key: str = Header(None)):
    """The function adds a new user to the database."""
    await check_api_key(api_key)
    new_user = User(**user.model_dump())
    try:
        async with session.begin():
            session.add(new_user)
            await session.commit()
    except IntegrityError:
        logger.error(f"This user already exist.")

    return new_user


@app.get("/api/users", response_model=List[DataUser])
async def get_all_users(api_key: str = Header(None)) -> List[UsersBase]:
    """The function shows all users in the database."""
    await check_api_key(api_key)
    async with session.begin():
        query = select(User.id, User.name, User.user_api_key)
        users = await session.execute(query)
        return users.all()


@app.get("/api/users/me")
async def get_users_profile(api_key: str = Header(None)):
    """The function shows the information about the user."""
    exec_result = False
    await check_api_key(api_key)
    user_id = await get_user_id(api_key)

    data = await get_user_data(user_id)

    if data:
        exec_result = True

    return {"result": exec_result, "user": data}


@app.get("/api/users/{id}", response_model=UserDataOut)
async def get_users_profile(id: int, api_key: str = Header(None)):
    """The function shows the information about the user."""
    exec_result = False
    await check_api_key(api_key)
    user_id = await get_user_by_id(id)
    if user_id is None:
        logger.error(f"The user ID {id} not found.")
        return {"result": exec_result, "user": {}}

    data = await get_user_data(user_id)

    if data:
        exec_result = True

    return {"result": exec_result, "user": data}


@app.post("/api/users/{id}/follow", response_model=ExecutionResult)
async def add_new_follower(id: int, api_key: str = Header(None)):
    exec_result = False
    await check_api_key(api_key)
    follower_id = await get_user_id(api_key)
    following_id = await get_user_by_id(id)
    if follower_id and following_id:
        if follower_id == following_id:
            logger.info(
                f"The user id: {following_id} is trying to subscribe to himself."
            )
            return {"result": exec_result}

        try:
            new_follower = FollowersAndFollowing(
                follower_id=follower_id, following_id=following_id
            )
            async with session.begin():
                session.add(new_follower)
                await session.commit()
                exec_result = True
                logger.info(
                    f"The user id: {following_id} subscribed to user id: {follower_id}"
                )
        except IntegrityError:
            logger.error(
                f"The user id: {following_id} is already subscribed to user id: {follower_id}"
            )

        finally:
            return {"result": exec_result}

    logger.error(f"The user id: {id} not found.")
    return {"result": exec_result}


@app.delete("/api/users/{id}/follow", response_model=ExecutionResult)
async def delete_follower(id: int, api_key: str = Header(None)):
    exec_result = False
    await check_api_key(api_key)
    follower_id = await get_user_id(api_key)
    following_id = await get_user_by_id(id)
    if follower_id and following_id:
        try:
            async with session.begin():
                data = select(FollowersAndFollowing).where(
                    FollowersAndFollowing.follower_id == int(follower_id)
                    and FollowersAndFollowing.following_id == following_id
                )
                entry = await session.execute(data)
                entry = entry.scalar()
                await session.delete(entry)
                await session.commit()
                exec_result = True
                logger.info(
                    f"The user id: {following_id} unsubscribed to user id: {follower_id}"
                )
        except UnmappedInstanceError:
            logger.error(
                f"The user id: {following_id} is not subscribed to user id: {follower_id}"
            )

        finally:
            return {"result": exec_result}

    logger.error(f"The user id: {id} not found.")
    return {"result": exec_result}


@app.post("/api/tweets", response_model=ResultAddedTweet)
async def add_new_tweet(new_tweet: AddTweet, api_key: str = Header(None)):
    """The function adds a new tweet to the database."""
    exec_result = False
    await check_api_key(api_key)
    author = await get_user_id(api_key)
    data = {
        "content": new_tweet.tweet_data,
        "attachments": new_tweet.tweet_media_ids,
        "author": author,
    }
    tweet = Tweet(**data)

    async with session.begin():
        session.add(tweet)
        await session.commit()

    async with session.begin():
        query = select(Tweet).order_by(desc(Tweet.id))
        result = await session.execute(query)
        last_tweet = result.scalars().first()

    if last_tweet:
        logger.info("The tweet added successfully.")
        exec_result = True
        return {"result": exec_result, "tweet_id": last_tweet.id}
    else:
        logger.error("The tweet didn't add.")
        return {"result": exec_result, "tweet_id": None}


@app.delete("/api/tweets/{id}", response_model=ExecutionResult)
async def delete_tweet(id: int, api_key: str = Header(None)):
    exec_result = False
    await check_api_key(api_key)
    author = await get_user_id(api_key)
    tweet_id = await get_tweet_by_id(id)
    print(tweet_id)
    print(author)
    if tweet_id and author:
        try:
            async with session.begin():
                data = select(Tweet).where(
                    Tweet.author == author and Tweet.id == int(tweet_id)
                )
                entry = await session.execute(data)
                entry = entry.scalar()
                await session.delete(entry)
                await session.commit()
                exec_result = True
                logger.info(f"The tweet id: {id} deleted.")
        except UnmappedInstanceError:
            logger.error(f"The user id: {author} can't delete tweet id: {tweet_id}")

        finally:
            return {"result": exec_result}

    logger.error(f"The tweet id: {id} not found.")
    return {"result": exec_result}


@app.post("/api/tweets/{id}/likes", response_model=ExecutionResult)
async def add_new_like(id: int, api_key: str = Header(None)):
    """The function adds a like to the database."""
    exec_result = False
    await check_api_key(api_key)
    user_id = await get_user_id(api_key)
    tweet_id = await get_tweet_by_id(id)
    if user_id and tweet_id:
        new_like = Like(user_id=user_id, tweet_id=tweet_id)
        async with session.begin():
            session.add(new_like)
            await session.commit()
            exec_result = True
            logger.info(f"The user id: {user_id} added a like to tweet id: {tweet_id}")
            return {"result": exec_result}

    logger.error(f"The tweet id: {id} not found.")
    return {"result": exec_result}


@app.delete("/api/tweets/{id}/likes", response_model=ExecutionResult)
async def delete_like(id: int, api_key: str = Header(None)):
    """The function delete a like from the database."""
    exec_result = False
    await check_api_key(api_key)
    user_id = await get_user_id(api_key)
    tweet_id = await get_tweet_by_id(id)
    if user_id and tweet_id:
        async with session.begin():
            try:
                data = select(Like).where(
                    Like.user_id == user_id and Like.tweet_id == int(tweet_id)
                )
                query = await session.execute(data)
                result = query.scalar()
                await session.delete(result)
                await session.commit()
                exec_result = True
                logger.info(
                    f"The user id: {user_id} deleted a like from tweet id: {tweet_id}"
                )
            except UnmappedInstanceError:
                logger.error(
                    f"The tweet id: {tweet_id} doesn't have a like from user id: {user_id}"
                )

            finally:
                return {"result": exec_result}

    logger.error(f"The tweet id: {id} not found.")
    return {"result": exec_result}


@app.get("/api/tweets", response_model=FeedTweets)
async def get_all_tweets(api_key: str = Header(None)):
    """The function delete a like from the database."""
    exec_result = False
    await check_api_key(api_key)

    tweets_list = []
    async with session.begin():
        query = select(Tweet.id, Tweet.content, Tweet.attachments, Tweet.author)
        res = await session.execute(query)
        tweets = res.all()

        if tweets:
            tweets_list = []
            for tweet_id, tweet_content, tweet_attachments, tweet_author in tweets:
                attachments = await check_tweet_attachments(tweet_attachments)
                likes_query = (
                    select(Like.user_id, User.name)
                    .join(User, Like.user_id == User.id)
                    .filter(Like.tweet_id == int(tweet_id))
                )
                likes = await session.execute(likes_query)
                likes = likes.all()
                likes_list = [{"user_id": like[0], "name": like[1]} for like in likes]
                author_query = select(User.id, User.name).filter(
                    User.id == int(tweet_author)
                )
                author = await session.execute(author_query)
                author = author.one()
                author = {"id": author[0], "name": author[1]}

                tweet_data = {
                    "id": tweet_id,
                    "content": tweet_content,
                    "attachments": attachments,
                    "author": author,
                    "likes": likes_list,
                }
                tweets_list.append(tweet_data)
            exec_result = True

    return {"result": exec_result, "tweets": tweets_list}


@app.post("/api/medias", response_model=AddMedias)
async def create_upload_files(file: UploadFile, api_key: str = Header(None)):
    """The function adds media to the file of the app."""
    exec_result = False
    await check_api_key(api_key)
    user_id = await get_user_id(api_key)
    filename = await check_file_extension(user_id=user_id, filename=file.filename)

    if filename:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        print(UPLOAD_FOLDER)
        print(file_path)
        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)

        new_file = Media(filename=file_path)
        async with session.begin():
            session.add(new_file)
            await session.commit()
            exec_result = True
            logger.info(f"The file {filename} added to the database.")

        async with session.begin():
            query = select(Media.id).order_by(desc(Media.id))
            result = await session.execute(query)
            last_file = result.scalars().first()

    return {"result": exec_result, "media_id": last_file}


if __name__ == "__main__":
    uvicorn.run("app:app", port=1111, host="127.0.0.1")
