FROM python:3.10


WORKDIR /stock

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY . /requirements.txt /stock/
RUN pip install -r requirements.txt

COPY . /stock

#COPY ./entrypoint.sh /stock/
#RUN chmod u+x ./entrypoint.sh
#ENTRYPOINT ["./entrypoint.sh"]
#EXPOSE 5000
CMD ["python", "main.py"]