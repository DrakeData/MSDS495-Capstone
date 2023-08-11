FROM python:3.11-slim
EXPOSE 8080
RUN pip install -U pip
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
WORKDIR  /app
COPY . ./
ENTRYPOINT [ "streamlit", "run", "homepage.py", "--server.port=8080", "--server.address=0.0.0.0"]