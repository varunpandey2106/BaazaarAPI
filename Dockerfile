FROM python:3.11.1

EXPOSE 8000

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt 

COPY . /app 

ENTRYPOINT ["python3"] 

CMD ["manage.py","runserver", "0.0.0.0:8000"]









