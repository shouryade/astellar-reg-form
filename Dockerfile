FROM python:3.10-slim-bullseye

# 
WORKDIR /app

# 
COPY ./requirements.txt /app/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 
COPY . /app/

#
EXPOSE 5010

# 
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5010","--reload"]
