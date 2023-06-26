from applications import create_app, db
from config import Config


# creating the application
app, celery = create_app(Config)

#Registers a function to be run before the first request to this instance of the application
@app.before_first_request
def create_all():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
