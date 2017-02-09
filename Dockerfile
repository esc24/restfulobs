FROM ubuntu:14.04
MAINTAINER Ed Campbell <email@email.com>
RUN apt-get update && apt-get install -y python-pip python-dev
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN mkdir /opt/app
COPY ./server.py ./jwtauth.py /opt/app/
WORKDIR /opt/app
EXPOSE 5000
ENV FLASK_APP="server.py"
ENTRYPOINT ["flask", "run"]
CMD ["--host=0.0.0.0", "--with-threads"]
