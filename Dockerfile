FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

WORKDIR /code/workbench

COPY requirements.txt /code/requirements.txt
RUN pip3 install --upgrade pip
RUN pip install -r /code/requirements.txt
RUN pip3 install Pillow psycopg2

COPY . /code/workbench

EXPOSE 8000

COPY ./docker-entrypoint.sh /code/workbench/docker-entrypoint.sh

RUN chmod +x /code/workbench/docker-entrypoint.sh

CMD ["/code/workbench/docker-entrypoint.sh"]

