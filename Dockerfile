FROM python:3.8.1-slim-buster

WORKDIR /app/

ADD requirements.txt .

RUN pip install --upgrade pip && pip install 

ADD main_app .

CMD ["uvicorn", "main:app --reload"]