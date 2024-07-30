FROM python:3.12

WORKDIR /app

COPY . .

EXPOSE 3000

RUN pip install -r requirements.txt

CMD ["python" , "app.py"]