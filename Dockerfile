FROM django:latest

WORKDIR ./
COPY . .

EXPOSE 8000
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]
