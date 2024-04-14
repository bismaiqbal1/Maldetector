import schedule
import os
from app import app
def delete():
    files = os.listdir("static/images")
    for f in files:
        os.remove(f"static/images/{f}")

if __name__ == "__main__":
    schedule.every().day.at("10:30").do(delete)
    app.run( debug=True)