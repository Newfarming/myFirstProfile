FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN sed -i 's/http:\/\/httpredir\.debian\.org\/debian\//http:\/\/mirrors\.163\.com\/debian\//g' /etc/apt/sources.list
RUN apt-get update && apt-get install -y gcc g++ python-software-properties libpq-dev git libmysqlclient-dev build-essential 
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install git+https://github.com/runforever/django-notifications.git 
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
ADD . /code/
