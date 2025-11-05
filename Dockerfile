FROM python:3
EXPOSE 80

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py migrate

CMD ["sh", "./start.sh"]