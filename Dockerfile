FROM python:3.8-slim

WORKDIR /usr/cardgame

COPY pyproject.toml .

RUN pip install poetry && poetry config virtualenvs.create false --local && poetry install

COPY . ./

EXPOSE 8000

CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8000"]