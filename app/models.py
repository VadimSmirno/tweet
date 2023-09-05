from typing import Dict, Any

from sqlalchemy import Column, ForeignKey, Integer, String, ARRAY, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base


class FollowersAndFollowings(Base):
    __tablename__ = "followers_and_followings"
    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
    following_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=True)

    follower = relationship('Users', back_populates='follower_id', foreign_keys=[follower_id])
    following = relationship('Users', back_populates='following_id', foreign_keys=[following_id])

    __table_args__ = (UniqueConstraint(follower_id, following_id, name='_follower_following_uc'),)

    def to_json(self) -> Dict[str, Any]:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    user_api_key = Column(String(255), nullable=False, unique=True, index=True)

    follower_id = relationship(
        'FollowersAndFollowings',
        back_populates='follower',
        foreign_keys=[FollowersAndFollowings.follower_id]
    )
    following_id = relationship(
        'FollowersAndFollowings',
        back_populates='following',
        foreign_keys=[FollowersAndFollowings.following_id]
    )
    tweet = relationship('Tweets', back_populates='user')
    like = relationship('Likes', back_populates='user')

    def to_json(self) -> Dict[str, Any]:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Tweets(Base):
    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(1000), nullable=False)
    attachments = Column(ARRAY(Integer), nullable=True)
    author = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=True)

    user = relationship('Users', back_populates='tweet')
    like = relationship('Likes', back_populates='tweet')

    def to_json(self) -> Dict[str, Any]:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Likes(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
    tweet_id = Column(Integer, ForeignKey('tweets.id', ondelete="CASCADE"), nullable=True)

    user = relationship('Users', back_populates='like')
    tweet = relationship("Tweets", back_populates='like')

    def to_json(self) -> Dict[str, Any]:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Medias(Base):
    __tablename__ = "medias"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
