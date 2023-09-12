import random
import string
from app.models import User, FollowersAndFollowing, Tweet, Like, Media
from database import session


def random_string(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def create_users(num_users=10):
    users = []
    for _ in range(num_users):
        name = random_string()
        user_api_key = random_string()
        user = User(name=name, user_api_key=user_api_key)
        users.append(user)
    session.add_all(users)
    session.commit()


def create_followers_and_followings(num_relationships=20):
    followers_and_followings = []
    users = session.query(User).all()
    for _ in range(num_relationships):
        follower = random.choice(users)
        following = random.choice(users)
        relationship = FollowersAndFollowing(follower=follower, following=following)
        followers_and_followings.append(relationship)
    session.add_all(followers_and_followings)
    session.commit()


def create_tweets(num_tweets=30):
    tweets = []
    users = session.query(User).all()
    for _ in range(num_tweets):
        content = random_string(50)
        author = random.choice(users)
        tweet = Tweet(content=content, author=author)
        tweets.append(tweet)
    session.add_all(tweets)
    session.commit()


def create_likes(num_likes=50):
    likes = []
    users = session.query(User).all()
    tweets = session.query(Tweet).all()
    for _ in range(num_likes):
        user = random.choice(users)
        tweet = random.choice(tweets)
        like = Like(user=user, tweet=tweet)
        likes.append(like)
    session.add_all(likes)
    session.commit()


def create_medias(num_medias=10):
    medias = []
    for _ in range(num_medias):
        filename = random_string(8) + ".jpg"
        media = Media(filename=filename)
        medias.append(media)
    session.add_all(medias)
    session.commit()


if __name__ == '__main__':
    create_users()
    create_followers_and_followings()
    create_tweets()
    create_likes()
    create_medias()

    session.close()
