FROM python:3.9.5-slim-buster
ENV PYTHONUNBUFFERED 1

COPY requirements-lock.txt /requirements.txt
RUN pip3 install --no-cache-dir pip --upgrade\
    && pip3 install --no-cache-dir -r /requirements.txt

EXPOSE 8080

WORKDIR /app
ADD . /app

CMD ["gunicorn", "-w", "2", "-b", ":8080", "app.main:app"]

