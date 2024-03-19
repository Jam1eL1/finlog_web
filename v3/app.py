import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
# set up client (represents the cluster you set up)
    client = MongoClient('mongodb+srv://test_user:LtcatrLRt7RCJY4N@cluster0.ckfhg1z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    # set up db
    app.db = client.finlog
# dbs = client.list_database_names() to see dbs existing inside the cluster
    entries = []

    @app.route("/", methods=["GET", "POST"])
    def home():
        # print(dbs)
        # print([e for e in app.db.entries.find({})])
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date =  datetime.datetime.today().strftime("%Y-%m-%d")
            # print(entry_content, formatted_date)
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
        
        entries_with_date = [ 
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d") 
            )
                for entry in app.db.entries.find({})
        ]
        
        return render_template("home.html", entries = entries_with_date)
        
    # if __name__ == "__main__":
    #     # if receiving user data
    #     app.run(debug=True)
    return app