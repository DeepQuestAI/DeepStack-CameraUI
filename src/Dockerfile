FROM python:3.8
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
EXPOSE 8501
COPY . /app
ENTRYPOINT ["streamlit","run"]
CMD ["app.py"]