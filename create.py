# create.py hanya dirun sekali 
from application import db, app
from application.models import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
