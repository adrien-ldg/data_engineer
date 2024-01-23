from flask import Flask, render_template, request, jsonify
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


@app.route("/top10", methods=["GET", "POST"])
def top10():

    teams_nba = collection.distinct("team")

    if request.method == "POST":
        selected_option_stats = request.form['selected_option_stats']
        selected_option_teams = request.form['selected_option_teams']

        
        if selected_option_stats == '':
            return jsonify({'head': "", 'body': ""})
        else:
            if selected_option_teams == "all":
                filter_condition = {"MJ": {'$gte': 15}}
            else:
                filter_condition = {"team": selected_option_teams, "MJ": {'$gte': 15}}

            if selected_option_stats == '1':
                top_players = collection.find(filter_condition).sort("MJ", -1).limit(10)
            if selected_option_stats == '2':
                top_players = collection.find(filter_condition).sort("minutes", -1).limit(10)
            if selected_option_stats == '3':
                top_players = collection.find(filter_condition).sort("tir", -1).limit(10)
            if selected_option_stats == '4':
                top_players = collection.find(filter_condition).sort("tir_3_pts", -1).limit(10)
            if selected_option_stats == '5':
                top_players = collection.find(filter_condition).sort("lf", -1).limit(10)
            if selected_option_stats == '6':
                top_players = collection.find(filter_condition).sort("rb_off", -1).limit(10)
            if selected_option_stats == '7':
                top_players = collection.find(filter_condition).sort("rb_df", -1).limit(10)
            if selected_option_stats == '8':
                top_players = collection.find(filter_condition).sort("rb", -1).limit(10)
            if selected_option_stats == '9':
                top_players = collection.find(filter_condition).sort("pd", -1).limit(10)
            if selected_option_stats == '10':
                top_players = collection.find(filter_condition).sort("bp", -1).limit(10)
            if selected_option_stats == '11':
                top_players = collection.find(filter_condition).sort("inter", -1).limit(10)
            if selected_option_stats == '12':
                top_players = collection.find(filter_condition).sort("ct", -1).limit(10)
            if selected_option_stats == '13':
                top_players = collection.find(filter_condition).sort("fte", -1).limit(10)
            if selected_option_stats == '14':
                top_players = collection.find(filter_condition).sort("pts", -1).limit(10)

        top_players_data = [(player["player"], player["MJ"], player["minutes"], player["tir"], player["tir_3_pts"], player["lf"], player["rb_off"], player["rb_df"], player["rb"], player["pd"], player["bp"], player["inter"], player["ct"], player["fte"], player["pts"]) for player in top_players]

        table_head_html = f"<tr><th>Rang</th><th>Joueur</th><th>MJ</th><th>Min</th><th>Tirs</th><th>3pts</th><th>LF</th><th>RebOff</th><th>RebDef</th><th>Reb</th><th>Pd</th><th>Bp</th><th>Int</th><th>Ct</th><th>Fte</th><th>Pts</th></tr>"
        table_body_html = ""
        for i, (player, MJ, min, tir, tir3, lf, rboff, rbdef, rb, pd, bp, inter, ct, fte, pts) in enumerate(top_players_data, start=1):
            table_body_html += "<tr>"
            for j, value in enumerate([i, player, MJ, min, tir, tir3, lf, rboff, rbdef, rb, pd, bp, inter, ct, fte, pts]):
                
                if j == int(selected_option_stats) + 1:
                    table_body_html += f"<td class='selected'>{value}</td>"
                else:
                    table_body_html += f"<td>{value}</td>"
            table_body_html += "</tr>"

        return jsonify({'head': table_head_html, 'body': table_body_html})

    return render_template("classement.html", teams_nba=teams_nba)


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
    app.run(debug=True, host="0.0.0.0")