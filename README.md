
GET request to http://localhost:5000/v1/obs
POST request example:

    curl -H "Content-Type: application/json" -X POST -d '{"weight": 78.0}' http://localhost:5000/v1/obs/




local install
-------------

With conda:

    conda install flask flask-cors
    pip install pyjwt dotenv

Just pip:

    pip install -r requirements.txt


docker
------

Build:

    docker build -t username/restfulobs:latest .

Run:

    docker run --name some-redis -v /docker/volumes/data:/data -d redis:alpine
    docker run --link some-redis:redis -p 5000:5000 --env-file .env username/restfulobs

Debug redis:

    docker run --link some-redis:redis -it redis redis-cli -h redis -p 6379

