# cardgame-api

./cardgame-service/
│
├── app/
│   ├── adapter/
|   |   └── mongo/
|   |       ├── connection.py
|   |       └── db.py
|   |   
│   ├── api/
|   |   ├── api_v1/
|   |   |   ├── endpoints/
|   |   |   |   ├── game.py
|   |   |   |   └── user.py
|   |   |   └── response.py
|   |   └── index.py
|   |
│   ├── model/
|   |   ├── game/
|   |   |   ├── function.py
|   |   |   └── model.py
|   |   ├── score/
|   |   |   ├── function.py
|   |   |   └── model.py
|   |   ├── token/
|   |   |   ├── function.py
|   |   |   └── model.py
|   |   └── user/
|   |       ├── function.py
|   |       └── model.py
|   |
│   ├── util/
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

