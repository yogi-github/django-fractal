# flask-fractal

**Goal**

Build a Flask web site using a Docker container, managed using docker-compose.  The web site will:
•	Connect to a sqllite db using Flask-SQLAlchemy.  
•	Use flask-migrate to create and upgrade the database. 
•	Flask-SQLAlchemy is to be used to define model relationships.
•	Serialize and write to the DB using Flask-Serialize.
•	Utilize volumes, Docker and docker-compose to make the DB persistent.
•	Use Pytest to create unittests which have full coverage.


**Setting up docker and running the service**

docker-compose up --build
