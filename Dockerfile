FROM python:3.6-alpine

# Python Dependencies
RUN apk add build-base jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib

# Python Packages
COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /wallpaper_server

RUN mkdir -p /data/backgrounds

WORKDIR /wallpaper_server
ENV PYTHONPATH .
ENTRYPOINT ["python3"]
CMD ["wallpaper_server/server.py"]