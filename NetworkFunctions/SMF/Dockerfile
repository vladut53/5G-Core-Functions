FROM python:latest  

MAINTAINER Vladut ILIE  

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 82

# CMD ["python", "smf.py"]
CMD ["python", "smf_QoS_Update.py"]
