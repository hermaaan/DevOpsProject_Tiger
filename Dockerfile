FROM python:3.11

ARG API_KEY
ENV API_KEY=${API_KEY}

COPY requirements.txt /app/
COPY . /app/
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
