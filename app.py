from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    mongodb_uri = os.getenv("MONGODB_URI")
# set up client (represents the cluster you set up)
    client = MongoClient(mongodb_uri)
    # set up db
    app.db = client.finlog
    # finlog is set up as database on mongodb project
# dbs = client.list_database_names() to see dbs existing inside the cluster
    # 'entries' is collection name from finlog database
    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
                action = request.form.get("action")
                
                if action == "add":
                    entry_content = request.form.get("content")
                    formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
                    app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
                
                elif action == "delete":
                    entry_id = request.form.get("entry_id")
                    # Convert entry_id to ObjectId
                    object_id = ObjectId(entry_id)
                    # Delete the entry from the database
                    app.db.entries.delete_one({"_id": object_id})

                elif action == "save":
                    entry_id = request.form.get("entry_id")
                    new_content = request.form.get("content")
                    formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
                    app.db.entries.update_one({"_id": ObjectId(entry_id)}, {"$set": {"content": new_content, "date": formatted_date}})

        entries_with_date = [ 
            (
                str(entry["_id"]),
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d") 
            )
                # organize by recently created date 
                for entry in app.db.entries.find({}).sort("date", -1)
        ]
        
        return render_template("home.html", entries = entries_with_date)
    
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404
    return app
    

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)