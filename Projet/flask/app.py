from flask import Flask, render_template
from flask_pymongo import PyMongo
import plotly.express as px
from io import BytesIO

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/basket"
mongo = PyMongo(app).db.nba_player

@app.route("/")
def home():
    return render_template("home.html", image = "/static/images/image1.jpg")


@app.route("/top5")
def top5():
    top_pts__players = mongo.find().sort("pts", -1).limit(5)
    top_pts_players_data = [(player["player"], player["pts"]) for player in top_pts__players]

    top_pd__players = mongo.find().sort("pd", -1).limit(5)
    top_pd_players_data = [(player["player"], player["pd"]) for player in top_pd__players]

    return render_template("classement.html", top_pts_players=top_pts_players_data, top_pd_players=top_pd_players_data)


@app.route("/graph")
def user():
    results = mongo.aggregate([
        {
            "$group": {
                "_id": "$team",
                "nb": {"$sum": {"$cond": [{"$gte": ["$pts", 20]}, 1, 0]}}
            }
        }
    ])

    categories = []
    counts = []

    for result in results:
        categories.append(result["_id"])
        counts.append(result["nb"])

    # Create a bar chart using Plotly Express
    fig = px.bar(x=categories, y=counts)
    fig.update_traces(marker_color="#0487B5")
    fig.update_layout(
        title="Barplot du nombre de joueurs ayant plus de 20pts par franchise",
        xaxis_title="Franchise",
        yaxis_title="Nombre",
        title_x=0.5,
    )

    graph_html = fig.to_html(full_html=False)

    return render_template('chart.html', graph_html=graph_html)


if __name__ == "__main__":
    app.run(debug=True)