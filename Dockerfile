FROM tensorflow/tensorflow:latest


RUN pip install Flask

RUN apt-get update

RUN apt-get install -y libsm6 libxext6 libxrender-dev  

RUN pip install opencv-python

WORKDIR /guessmynumber

COPY . .

ENV FLASK_APP api.py

CMD ["flask", "run","--host","0.0.0.0"]

EXPOSE 5000