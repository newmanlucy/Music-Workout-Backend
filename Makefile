venv/bin/python:
	virtualenv --python=python3 venv
	venv/bin/pip install -r requirements.txt

run: 
	venv/bin/python -m server.app

db: 
	venv/bin/python -m server.db

test: clean venv/bin/python
	@echo "no tests added yet"

clean:
	rm -rf venv
	rm -f *.pyc
