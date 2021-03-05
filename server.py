from flask import Flask

from endpoints.indlovu import indlovu

app = Flask(__name__)
app.register_blueprint(indlovu)

app.run(host='127.0.0.1', port='8765')