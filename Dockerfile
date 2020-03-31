FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN apt update && apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib tesseract-ocr -y
RUN pip install -r requirements.txt
CMD ["python", "manage.py", "runserver"]