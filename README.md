To run the server:

    make run

To test one test file, run `make test-one test=name` where `name` is the name of the test, while the server is running in another terminal. For example, if the test file is `tests/test_user.py`, then `name` is `user`.

To clean and build the virtual environment:

    make clean setup