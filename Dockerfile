FROM python:3.10

RUN apt-get update
RUN apt-get install -y --no-install-recommends gdal-bin
RUN apt-get install -y mime-support

WORKDIR /code/workbench

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /code/workbench/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /code/workbench/requirements.txt
RUN pip3 install Pillow psycopg2

COPY . /code/workbench

EXPOSE 8000

COPY ./docker-entrypoint.sh /code/workbench/docker-entrypoint.sh

RUN chmod +x /code/workbench/docker-entrypoint.sh

CMD ["/code/workbench/docker-entrypoint.sh"]

