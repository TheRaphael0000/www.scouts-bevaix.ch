FROM python:3
EXPOSE 80

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py migrate
RUN python manage.py collectstatic --no-input

CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:80", "scoutsbevaix.wsgi:application"]