FROM python:3
COPY . .
RUN pip3 install requests
RUN pip3 install translate
RUN pip3 install djangorestframework
RUN pip3 install django
EXPOSE 8000/tcp
CMD python3 manage.py runserver