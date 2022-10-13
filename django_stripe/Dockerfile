FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /django_stripe
WORKDIR /django_stripe

COPY requirements.txt /django_stripe/
COPY entrypoint.sh /django_stripe/
RUN chmod +x ./entrypoint.sh

RUN pip install --upgrade pip && pip install -r requirements.txt

ADD . /django_stripe

ENTRYPOINT ["sh", "./entrypoint.sh"]