FROM django:latest

WORKDIR ./
VOLUME /db
COPY Maintenance /Maintenance
COPY PM /PM
COPY manage.py /manage.py

EXPOSE 8080
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8080"]
