# Dockerfile, Image, Container
FROM python:3.9.0
EXPOSE 8080
WORKDIR  /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . /app
CMD streamlit run --server.port 8080 --server.enableCORS false 1_homepage.py