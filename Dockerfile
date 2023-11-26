FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y --no-install-recommends gdal-bin
RUN apt-get install -y mime-support
WORKDIR /code/WorkBench

COPY requirements.txt /code/requirements.txt
RUN pip3 install --upgrade pip
RUN pip install -r /code/requirements.txt
RUN pip3 install Pillow psycopg2

COPY . /code/WorkBench

EXPOSE 8000
# Copy source code

COPY . /code/WorkBench
COPY ./docker-entrypoint.sh ./docker-entrypoint.sh


RUN chmod +x /code/WorkBench/docker-entrypoint.sh
CMD ["/code/WorkBench/docker-entrypoint.sh"]


