FROM python:3.9.5-slim-buster
ENV PYTHONUNBUFFERED 1

COPY requirements-lock.txt /requirements.txt
RUN pip3 install --no-cache-dir pip==21.3.1\
    && pip3 install --no-cache-dir -r /requirements.txt

EXPOSE 8080

WORKDIR /app

RUN addgroup --system app && adduser --system --group app
USER app

COPY . /app

CMD ["gunicorn", "-w", "2", "-b", ":8080", "app.main:app"]

