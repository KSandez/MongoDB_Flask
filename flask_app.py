# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient

import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/marsDB"
mongo = PyMongo(app)

# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Fetch data from MongoDB
    marsDB = mongo.db.collection.find_one()

    return render_template("index.html", marsDB=marsDB)


# Put scraped data into MongoDB
@app.route("/scrape")
def scrape():
    
    client = MongoClient('localhost', 27017)
    db = client['marsDB']

    if 'collection' in db.list_collection_names():
        db.drop_collection('collection')

    # Run scraped functions
    mars = scrape_mars.scrape()

    # Dictionary for mars scraped data from mission to mars notebook
    marsDB = {
        "title": mars["title"],
        "paragraph": mars["paragraph"],
        "featured_image": mars["featured_image"],
        "weather": mars["weather"],
        "mars_facts": mars["mars_facts"],
        "hemispheres": mars["hemispheres"],
    }

    # Insert dictionary into MongoDB
    mongo.db.collection.insert_one(marsDB)

    # Redirect back to home page
    return redirect("/", code=302)

print("Data Uploaded!")


if __name__ == "__main__":
    app.run(port=5000, debug=True)