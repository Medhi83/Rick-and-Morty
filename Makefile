# Some useful rules

install_env: # Create virtualenv and install dependencies
	virtualenv -p python3.9 env
	env/bin/pip install -U pip
	env/bin/pip install -r requirements-lock.txt

lock_requirements: # Lock dependencies versions
	docker build -t rick-n-morty .
	docker run --name rick-n-morty -d rick-n-morty sleep 3600
	docker exec rick-n-morty pip install -r requirements.txt
	docker exec rick-n-morty pip freeze -r requirements.txt > requirements-lock.txt
	docker rm -f rick-n-morty

check_security: # Checks dependencies for known security vulnerabilities.
	safety check -r requirements-lock.txt

build: # Build the docker image
	docker rm -f rick-n-morty
	docker build -t rick-n-morty .

run: build # Build the new docker image and run it
	docker run -p 8080:8080 --name rick-n-morty -d rick-n-morty
	