
# Python
import json
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# Fast API
from fastapi import FastAPI
from fastapi import status
from fastapi import Body 

app = FastAPI()

# Models

class PasswordMixin(BaseModel):
    password : str = Field(...,min_length=8,max_length=64)

class UserBase(BaseModel):
    user_id : UUID = Field(...)
    email : EmailStr = Field(...)


class User(UserBase):
    first_name : str = Field(
            ...,
            min_length=1,
            max_length=50
            )
    last_name : str = Field(
            ...,
            min_length=1,
            max_length=50
            )
    birth_date : Optional[date] = Field(default=None)


class UserLogin(PasswordMixin,UserBase):
    pass


class UserRegister(PasswordMixin,User):
    pass


class Tweet(BaseModel):
    tweet_id : UUID = Field(...)
    content : str = Field(..., 
            min_length=1,
            max_length=256
            )
    created_at : datetime = Field(default=datetime.now())
    updated_at : Optional[datetime] = Field(default=None)
    by : User = Field(...)

@app.get(
        path="/",
        summary="Check if services it's alive",
        tags=["Home"]
        )
def home():
    return {"Twitter Api" : "is Working"}


## Users
@app.post(
        path="/signup",
        response_model=User,
        status_code=status.HTTP_201_CREATED,
        summary="Register a User",
        tags=["Users"]
        )
def signup(user : UserRegister = Body(...)):
    """
    Signup

    This path operations register a user in the app.

    Parameters:
    - Request body parameter
        - user : UserRegister
    
    Returns a json with the basic user info:
    - user_id : UUID
    - email : EmailStr
    - first_name : str
    - last_name : str
    - birth_date : date
    """
    with open("users.json","r+",encoding="utf-8") as f:
        res = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"]) 
        user_dict["birth_date"] = str(user_dict["birth_date"])
        res.append(user_dict)
        f.seek(0)
        f.write(json.dumps(res))
    return user



@app.post(
        path="/login",
        response_model=User,
        status_code=status.HTTP_200_OK,
        summary="Login a User",
        tags=["Users"]
        )
def login():
    pass


@app.get(
        path="/users",
        response_model=List[User],
        status_code=status.HTTP_200_OK,
        summary="Show all users",
        tags=["Users"]
        )
def show_all_users():
    """
    Show all Users

    This path operation show all the users in the app.
    
    Parameters:
    - None

    Returns a json list with all users of type User
    """
    with open("users.json","r",encoding="utf-8") as f:
        return json.loads(f.read())


@app.get(
        path="/users/{user_id}",
        response_model=User,
        status_code=status.HTTP_200_OK,
        summary="Show a user",
        tags=["Users"]
        )
def show_a_user():
    pass


@app.delete(
        path="/users/{user_id}",
        response_model=User,
        status_code=status.HTTP_200_OK,
        summary="Delete a user",
        tags=["Users"]
        )
def delete_a_user():
    pass


@app.put(
        path="/users/{user_id}",
        response_model=User,
        status_code=status.HTTP_200_OK,
        summary="Update a user",
        tags=["Users"]
        )
def update_a_user():
    pass


## Tweets
@app.get(
        path="/tweets",
        response_model=List[Tweet],
        status_code=status.HTTP_200_OK,
        summary="Show all tweets",
        tags=["Tweets"]
        )
def show_all_tweets():
    pass


@app.post(
        path="/post",
        response_model=Tweet,
        status_code=status.HTTP_201_CREATED,
        summary="Post a tweet",
        tags=["Tweets"]
        )
def post(tweet : Tweet = Body(...)):
    """
    Post a tweet

    This path operations post a tweet in the app.

    Parameters:
    - Request body parameter
        - tweet : Tweet
    
    Returns a json with the basic tweet info:
    - tweet_id : UUID
    - content: str
    - created_at : datetime
    - updated_at : Optional[datetime] 
    - by : User
    """
    with open("tweets.json","r+",encoding="utf-8") as f:
        res = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"]) 
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        if tweet_dict["updated_at"] is not None:
            tweet_dict["updated_at"] = str(tweet_dict["updated_at"]) 
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"]) 
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        res.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(res))
    return tweet


@app.get(
        path="/tweets/{tweets_id}",
        response_model=Tweet,
        status_code=status.HTTP_200_OK,
        summary="Show a tweet",
        tags=["Tweets"]
        )
def show_a_tweet():
    pass


@app.delete(
        path="/tweets/{tweets_id}",
        response_model=Tweet,
        status_code=status.HTTP_200_OK,
        summary="Delete a tweet",
        tags=["Tweets"]
        )
def delete_a_tweet():
    pass


@app.put(
        path="/tweets/{tweets_id}",
        response_model=Tweet,
        status_code=status.HTTP_200_OK,
        summary="Update a tweet",
        tags=["Tweets"]
        )
def update_a_tweet():
    pass








