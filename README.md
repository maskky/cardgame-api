# Cardgame-api

## Table of Content
- [Project Stcutrue](#project-structure)
- [Prerequisite](#prerequisite)
  - [Config](#config)
    - [dotenv](#dotenv)
    - [docker-compose](#docker-compose)
- [Run](#run)
  - [Regular](#regular)
  - [Run with docker-compose](#run-with-docker-compose)
- [How to play](#how-to-play)
  - [Register](#register)
  - [Login](#login)
  - [New Game](#new-game)
  - [Current Game](#current-game)
  - [Flip card](#flip-card)

## Project Structure

```
./cardgame-service/
│
├── app/
│   ├── adapter/ # Store all adapter that connect external
|   |   └── mongo/
|   |       ├── connection.py
|   |       └── db.py
|   |
│   ├── api/ # Store all API and endpoint
|   |   ├── api_v1/
|   |   |   ├── endpoints/
|   |   |   |   ├── game.py
|   |   |   |   └── user.py
|   |   |   └── response.py
|   |   └── index.py
|   |
│   ├── model/ # Store all model schema and query
|   |   ├── game/
|   |   |   ├── function.py
|   |   |   └── model.py
|   |   ├── score/
|   |   |   ├── function.py
|   |   |   └── model.py
|   |   ├── token/
|   |   |   ├── function.py
|   |   |   └── model.py
|   |   ├── user/
|   |   |   ├── function.py
|   |   |   └── model.py
|   |   └── custom_schema.py
|   |
│   ├── util/ # Store all utilities that not include business-logic
|   |   ├── config.py
|   |   ├── error.py
|   |   └── index.py
|   |   
│   └── main.py
│
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── index.py
├── pyproject.toml
└── .README.md
```

## Prerequisite
Python version: `3.8.5`
Mongo version: `3.6`
Poetry version: `1.1.6` (Package Manager)

Install denpendencies (If use Docker)
```sh
pip install poetry && poetry install
```

poetry will return name and path of virtual env, then **activate** that virtual env

### Config
#### Dotenv
By default, .env will contains
```
# Mongo database url
MONGODB_URL=mongodb://localhost:27017

# Total card in game and the value must be **even number
TOTAL_CARD=12

# Secret key for encode access token
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7

# Life time of access token
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Docker-compose
```
environment:
  - MONGODB_URL=mongodb://cardgame-mongo:27017 
  - TOTAL_CARD=12
  - SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
  - ACCESS_TOKEN_EXPIRE_MINUTES=30
```
**cardgame-mongo** is the name of mongo container in same network.

### Run
#### Regular
```sh
uvicorn index:app --reload
```
#### Run with docker-compose
```sh
docker-compose up -d
```

and API docuemnts will appear at: `http://localhost:8000/redoc`

### How to play
#### Register
Register with **POST** `/api/v1/register`
```
# Request body
{
    "username": "<username>",
    "password": "<password>"
}
```
#### Login
Login with **POST** `/api/v1/login`
```
# Request body
{
    "username": "<username>",
    "password": "<password>"
}
```
If success, you will get **access_token**
```
# Response body
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer"
}
```
#### New game
**required Authorization**<br>
New game with **POST** `/api/v1/new_game`
**You need to add **Authorization** in headers
examples:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
and you will get
```{
    "username": "maskky", # Your username
    "movement": 0, # flip count
    "cleared": false, # Determine that this game was cleared or not
    "user_best": null, # Your best score. If this is first time play, user_best will be null
    "global_best": null, # Global best score. If no have best score before, global_best will be null
    "board": [ # Board is the list of cards with value and flipped fields.
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        }
    ]
}
```
#### Current Game
**required Authorization**<br>
Get current game with **GET** `/api/v1/continue`
and you will get your current game and continue play.
#### Flip card
**required Authorization**<br>
Flip card with **POST** `/api/v1/flip_card/{card}` **{card}** is index of **board** list.
Examples: 

- Try to flip **0** index by **POST** `/api/v1/flip_card/0`

```
{
    "username": "maskky",
    "movement": 1, # movement will increase by 1
    "cleared": false,
    "user_best": null,
    "global_best": null,
    "board": [
        {
            "value": 2, # value will be show 
            "flipped": true # flipped will be true
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        }
    ]
}
```

- Try to compare **last flip** with **1** index by **POST** `/api/v1/flip_card/1`

```
{
    "username": "maskky",
    "movement": 2, # movement will increase by 1
    "cleared": false,
    "user_best": null,
    "global_best": null,
    "board": [
        {
            "value": 2, # value will be show 
            "flipped": true # flipped will be true
        },
        {
            "value": 4, # value will be show 
            "flipped": true # flipped will be true
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        }
    ]
}
```

Due the compare is **not match**, Last face up card will be face down
- Try to flip **0** index again by **POST** `/api/v1/flip_card/0`


```
{
    "username": "maskky",
    "movement": 3, # movement will increase by 1
    "cleared": false,
    "user_best": null,
    "global_best": null,
    "board": [
        {
            "value": 2, # value will be show 
            "flipped": true # flipped will be true
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        }
    ]
}
```

- Try to compare **last flip** with **9** index by **POST** `/api/v1/flip_card/9`

```
{
    "username": "maskky",
    "movement": 4,
    "cleared": false,
    "user_best": null,
    "global_best": null,
    "board": [
        {
            "value": 2,
            "flipped": true
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        },
        {
            "value": 2,
            "flipped": true
        },
        {
            "flipped": false
        },
        {
            "flipped": false
        }
    ]
}
```

Due the compare is **match**, The 2 of match card will face up.
- Continue playing until the game was cleared, All cards will face up and **user_best** and **global_best** will update.

```
{
    "username": "maskky",
    "movement": 20,
    "cleared": true,
    "user_best": 20,
    "global_best": 20,
    "board": [
        {
            "value": 2,
            "flipped": true
        },
        {
            "value": 4,
            "flipped": true
        },
        {
            "value": 0,
            "flipped": true
        },
        {
            "value": 5,
            "flipped": true
        },
        {
            "value": 3,
            "flipped": true
        },
        {
            "value": 4,
            "flipped": true
        },
        {
            "value": 3,
            "flipped": true
        },
        {
            "value": 1,
            "flipped": true
        },
        {
            "value": 5,
            "flipped": true
        },
        {
            "value": 2,
            "flipped": true
        },
        {
            "value": 0,
            "flipped": true
        },
        {
            "value": 1,
            "flipped": true
        }
    ]
}
```