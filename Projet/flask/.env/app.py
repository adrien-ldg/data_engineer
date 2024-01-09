from flask import Flask, render_template
import pymongo
import plotly.express as px
import os

app = Flask(__name__)
mongo = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = mongo.basket
collection = db.nba_player

@app.route("/")
def home():
    return render_template("home.html", image = "/static/images/image1.jpg")


@app.route("/top5")
def top5():
    top_MJ_players = collection.find().sort("MJ", -1).limit(5)
    top_MJ_players_data = [(player["player"], player["MJ"]) for player in top_MJ_players]

    top_min_players = collection.find().sort("minutes", -1).limit(5)
    top_min_players_data = [(player["player"], player["minutes"]) for player in top_min_players]


    top_tir_players = collection.find({"MJ": {"$gte": 20}}).sort("tir", -1).limit(5)
    top_tir_players_data = [(player["player"], player["tir"]) for player in top_tir_players]

    top_tir3_pts_players = collection.find({"MJ": {"$gte": 20}}).sort("tir_3_pts", -1).limit(5)
    top_tir_3_pts_players_data = [(player["player"], player["tir_3_pts"]) for player in top_tir3_pts_players]

    top_lf_players = collection.find({"MJ": {"$gte": 20}}).sort("lf", -1).limit(5)
    top_lf_players_data = [(player["player"], player["lf"]) for player in top_lf_players]

    top_rb_off_players = collection.find({"MJ": {"$gte": 20}}).sort("rb_off", -1).limit(5)
    top_rb_off_players_data = [(player["player"], player["rb_off"]) for player in top_rb_off_players]

    top_rb_def_players = collection.find({"MJ": {"$gte": 20}}).sort("rb_df", -1).limit(5)
    top_rb_def_players_data = [(player["player"], player["rb_df"]) for player in top_rb_def_players]

    top_rb_players = collection.find({"MJ": {"$gte": 20}}).sort("rb", -1).limit(5)
    top_rb_players_data = [(player["player"], player["rb"]) for player in top_rb_players]

    top_pd_players = collection.find({"MJ": {"$gte": 20}}).sort("pd", -1).limit(5)
    top_pd_players_data = [(player["player"], player["pd"]) for player in top_pd_players]

    top_bp_players = collection.find({"MJ": {"$gte": 20}}).sort("bp", -1).limit(5)
    top_bp_players_data = [(player["player"], player["bp"]) for player in top_bp_players]

    top_inter_players = collection.find({"MJ": {"$gte": 20}}).sort("inter", -1).limit(5)
    top_inter_players_data = [(player["player"], player["inter"]) for player in top_inter_players]

    top_ct_players = collection.find({"MJ": {"$gte": 20}}).sort("ct", -1).limit(5)
    top_ct_players_data = [(player["player"], player["ct"]) for player in top_ct_players]

    top_fte_players = collection.find({"MJ": {"$gte": 20}}).sort("fte", -1).limit(5)
    top_fte_players_data = [(player["player"], player["fte"]) for player in top_fte_players]

    top_pts_players = collection.find({"MJ": {"$gte": 20}}).sort("pts", -1).limit(5)
    top_pts_players_data = [(player["player"], player["pts"]) for player in top_pts_players]

    return render_template("classement.html", top_MJ_players=top_MJ_players_data,
                           top_min_players=top_min_players_data, top_tir_players=top_tir_players_data,
                           top_tir_3_pts_players=top_tir_3_pts_players_data, top_lf_players=top_lf_players_data,
                           top_rb_off_players=top_rb_off_players_data, top_rb_def_players=top_rb_def_players_data,
                           top_rb_players=top_rb_players_data, top_pd_players=top_pd_players_data,
                           top_bp_players=top_bp_players_data, top_inter_players=top_inter_players_data,
                           top_ct_players=top_ct_players_data, top_fte_players=top_fte_players_data,
                           top_pts_players=top_pts_players_data)


@app.route("/graphs")
def user():

    results = collection.aggregate([
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

    fig = px.bar(x=categories, y=counts)
    fig.update_traces(marker_color="#0487B5")
    fig.update_layout(
        title="Nombre de joueurs ayant plus de 20pts par franchise",
        xaxis_title="Franchise",
        yaxis_title="Nombre",
        title_x=0.5
    )

    graph_1 = fig.to_html(full_html=False)

    cur = list(collection.find())

    minj = []
    pts = []

    for result in cur:
        minj.append(result["minutes"])
        pts.append(result["pts"])

    fig = px.scatter(x=minj, y=pts)
    fig.update_traces(marker_color="#0487B5")
    fig.update_layout(
        title="Nombre de points marqués en fonction du temps de jeu",
        xaxis_title="temps de jeu",
        yaxis_title="Points",
        title_x=0.5
    )

    graph_2 = fig.to_html(full_html=False)


    size = [result["size"] for result in cur]

    fig = px.histogram(x=size, nbins=15)
    fig.update_traces(marker_color="#0487B5", opacity=0.7, marker_line_color='black', marker_line_width=0.5)
    fig.update_layout(
        title="Tailles des joueurs en 2023-2024",
        title_x=0.5,
        xaxis_title="Tailles",
        yaxis_title="Nombre",
        bargap=0.1,
        barmode='overlay'
    )

    graph_3 = fig.to_html(full_html=False)


    weight = [result["weight"] for result in cur]

    fig = px.histogram(x=weight, nbins=15)
    fig.update_traces(marker_color="#0487B5", opacity=0.7, marker_line_color='black', marker_line_width=0.5)
    fig.update_layout(
        title="Poids des joueurs en 2023-2024",
        title_x=0.5,
        xaxis_title="Poids",
        yaxis_title="Nombre",
        bargap=0.1,
        barmode='overlay'
    )

    graph_4 = fig.to_html(full_html=False)


    nationality = [entry.strip() for result in cur for entry in result["nationality"]]

    fig = px.pie(names=nationality)
    fig.update_traces(opacity=0.7, textinfo='none', hovertemplate='%{label}: %{percent:.1%}')
    fig.update_layout(
        title="Répartition de la nationalité des joueurs en 2023-2024",
        title_x=0.5,
        legend_title_text='Nationalité: '
    )

    graph_5 = fig.to_html(full_html=False)

    return render_template('chart.html', graph_1=graph_1, graph_2=graph_2, graph_3=graph_3,
                           graph_4=graph_4, graph_5=graph_5)


if __name__ == "__main__":
    app.run(debug=True)