from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from pytz import timezone
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

#migrate = Migrate(app, db)

app_tz = timezone(app.config.get('SERVER_TIMEZONE', 'Etc/UTC'))
if __name__ == "__main__":
    app.run()


from model import model
import views
