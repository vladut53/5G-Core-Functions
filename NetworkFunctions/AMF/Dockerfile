FROM python:latest  

MAINTAINER Vladut ILIE   

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 83

CMD ["python", "amf.py"]
