from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')

from auth import views
from manage import utils
from manage import generator

@app.route("/")
def Home():
    return "Home"

if __name__ == "__main__":
    app.run(debug=True)