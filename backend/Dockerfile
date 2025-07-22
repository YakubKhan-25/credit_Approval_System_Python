FROM python:3.9-slim

# Set environment variables to prevent temporary file creation
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app


COPY requirements.txt /app/

# install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY ./app /app/


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
