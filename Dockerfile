FROM python:3.8-slim-buster

WORKDIR /app

COPY static/ static/
COPY subnetter/ subnetter/
COPY templates/ templates/
COPY app.py app.py
COPY config.py config.py
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8001"]
