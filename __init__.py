from api import app, db
import routes
import documents


if __name__ == "__main__":
    app.run(debug=True)
    db.disconnect()