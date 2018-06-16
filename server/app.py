from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return "Music workout app API"


if __name__ == "__main__":
    app.run()
