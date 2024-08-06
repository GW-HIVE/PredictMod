# docker build -t predictmod:mm-backend .
FROM predictmod:backend-mm-base

COPY . /backend
WORKDIR /backend

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--access-logfile", "/var/log/gunicorn/dev.log", "mm_wsgi:app"]
# CMD ["gunicorn", "-c", "gunicorn_conf.py"]
