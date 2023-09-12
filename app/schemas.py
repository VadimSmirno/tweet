from pydantic import BaseModel, Field
from typing import Union


class UsersBase(BaseModel):
    name: str = Field(title="The name of the user.", max_length=255)
    user_api_key: str = Field(title="The api-key for the user.", max_length=255)


class UsersCreate(UsersBase):
    pass


class ItemUser(UsersBase):
    result: bool = Field(title="Query execution result.")
    user_id: int = Field(title="The id of added user.")

    class ConfigDict:
        from_attributes = True


class DataUser(BaseModel):
    id: int = Field(title="An ID of the user.")
    name: str = Field(title="The name of the user.")


class FullDataUser(DataUser):
    followers: list[DataUser] = Field(title="Followers of the user.")
    followings: list[DataUser] = Field(title="Followers of the user.")

    class ConfigDict:
        from_attributes = True


class UserDataOut(BaseModel):
    result: bool = Field(title="Query execution result.")
    user: Union[FullDataUser, dict] = Field(title="The data of the user.")


class ExecutionResult(BaseModel):
    result: bool = Field(title="The result of the function execution.")


class AddTweet(BaseModel):
    tweet_data: str = Field(title="The text of the tweet.", max_length=1000)
    tweet_media_ids: list[int] = Field(title="Media for the tweet.")


class ResultAddedTweet(BaseModel):
    result: bool = Field(title="The result of adding a tweet.")
    tweet_id: int = Field(title="ID of the added tweet.")


class TweetItems(BaseModel):
    id: int = Field(title="An ID of the tweet.")
    content: str = Field(title="A content of the tweet.")
    attachments: list[str] = Field(title="Media files of the tweet.")
    author: dict = Field(title="Data of the author of the tweet.")
    likes: list[dict] = Field(title="Data of the owner of the like.")


class FeedTweets(BaseModel):
    result: bool = Field(title="The result of getting tweets.")
    tweets: list[TweetItems] = Field(title="The list of tweets.")


class AddMedias(BaseModel):
    result: bool = Field(title="The result of adding a file.")
    media_id: int = Field(title="ID of the added file.")
