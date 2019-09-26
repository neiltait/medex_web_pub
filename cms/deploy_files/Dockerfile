FROM python:3
ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY 'secret key ... '
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN python manage.py compilescss
RUN python manage.py collectstatic --ignore=*.scss

RUN chmod +x ./deploy_files/docker-entrypoint.sh

#ENTRYPOINT ["./deploy_files/docker-entrypoint.sh"]