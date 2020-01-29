FROM python:3.7.1

WORKDIR /var/www/app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000


ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

CMD ["flask", "run", "--cert=cert.pem", "--key=key.pem"]