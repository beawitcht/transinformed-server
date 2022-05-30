FROM python:3.9.6-alpine


WORKDIR /home/site/wwwroot
COPY . .
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["gunicorn","-w 4", "-b", "0.0.0.0:8000", "main:app"] 