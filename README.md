
GET request to http://localhost:5000/v1/obs

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

    docker build -t username/jwttut:latest .

Run:

    docker run -p 5000:5000 --env-file .env username/jwttut

