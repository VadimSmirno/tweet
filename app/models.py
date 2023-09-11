from typing import Dict, Any
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, ARRAY, UniqueConstraint
from sqlalchemy.orm import relationship



Base = declarative_base()
class JsonMixsin():
    @staticmethod
    def to_json(self, table) -> Dict[str, Any]:
        return {column.name: getattr(self, column.name) for column in table.columns}


class FollowersAndFollowing(Base, JsonMixsin):
    __tablename__ = "followers_and_followings"
    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
    following_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=True)

    follower = relationship('User', back_populates='follower_id', foreign_keys=[follower_id])
    following = relationship('User', back_populates='following_id', foreign_keys=[following_id])

    __table_args__ = (UniqueConstraint(follower_id, following_id, name='_follower_following_uc'),)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    user_api_key = Column(String(255), nullable=False, unique=True, index=True)

    follower_id = relationship(
        'FollowersAndFollowings',
        back_populates='follower',
        foreign_keys=[FollowersAndFollowing.follower_id]
    )
    following_id = relationship(
        'FollowersAndFollowings',
        back_populates='following',
        foreign_keys=[FollowersAndFollowing.following_id]
    )
    tweet = relationship('Tweet', back_populates='user')
    like = relationship('Like', back_populates='user')


class Tweet(Base):
    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(1000), nullable=False)
    attachments = Column(ARRAY(Integer), nullable=True)
    author = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=True)

    user = relationship('User', back_populates='tweet')
    like = relationship('Like', back_populates='tweet')


class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
    tweet_id = Column(Integer, ForeignKey('tweets.id', ondelete="CASCADE"), nullable=True)

    user = relationship('User', back_populates='like')
    tweet = relationship("Tweet", back_populates='like')


class Media(Base):
    __tablename__ = "medias"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
