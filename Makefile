setup:
	virtualenv --python=python3 venv
	venv/bin/pip install -r requirements.txt

run: 
	venv/bin/python -m server.app

db: 
	venv/bin/python -m server.db

test-one:
	venv/bin/python -m tests.test_$(test)

clean:
	rm -rf venv
	rm -f *.pyc
