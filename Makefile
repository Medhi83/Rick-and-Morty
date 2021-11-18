# Some useful rules

install_env: # Create virtualenv and install dependencies
	virtualenv -p python3.9 env
	env/bin/pip install -U pip
	env/bin/pip install -r requirements-lock.txt

lock_requirements: build # Lock dependencies versions
	docker run --name rick-n-morty -d rick-n-morty sleep 3600
	docker exec rick-n-morty pip install -r requirements.txt
	docker exec rick-n-morty pip freeze -r requirements.txt > requirements-lock.txt
	docker rm -f rick-n-morty

check_security: # Checks dependencies for known security vulnerabilities.
	safety check -r requirements-lock.txt

build: # Build the docker image
	docker rm -f rick-n-morty
	docker build -t rick-n-morty .

run: # Run rick-n-morty app and database
	docker-compose up -d
	docker-compose logs -f -t app

stop: # Stop rick-n-morty app and database
	docker-compose down --remove-orphans
	
import_data: # Run script to import data from /json_data/rick_morty-characters_v1.json and /json_data/rick_morty-episodes_v1.json
	cd scripts/ && ../env/bin/python import_data.py