import json
from flask import Flask, render_template, request, redirect, flash, url_for


#le with ouvre le fichier clubs.json en mode lecture et le charge avec json.load
#le json.load lit le contenu du fichier et le convertit en un objet Python (ici, un dictionnaire)
#ensuite on accede a la cle "clubs" du dictionnaire pour obtenir la liste des clubs
def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs 
    


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


def saveClubs(clubs):
    with open("clubs.json", "w") as f:
        json.dump({"clubs": clubs}, f)


def saveCompetitions(competitions):
    with open("competitions.json", "w") as f:
        json.dump({"competitions": competitions}, f)

app = Flask(__name__)# création de l'application Flask
app.secret_key = "something_special"
# clé secrète utilisée par Flask pour sécuriser les sessions et les cookies

competitions = loadCompetitions()#  chargement des compétitions contienues dans le fichier competitions.json
clubs = loadClubs()# chargement des clubs contenus dans le fichier clubs.json


@app.route("/")# route principale de l'application
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])# route pour afficher le résumé des compétitions et des clubs
def showSummary():
    # club = [club for club in clubs if club["email"] == request.form["email"]][0]
    # return render_template("welcome.html", club=club, competitions=competitions)

    matching_clubs = [club for club in clubs if club["email"] == request.form["email"]]# liste des clubs dont l'email correspond à celui soumis dans le formulaire
    if matching_clubs:
        club = matching_clubs[0]
        return render_template("welcome.html", club=club, competitions=competitions)
    else:

        return render_template("Erreur_Email.html")


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Nous rencontrons des difficultés pour trouver le club ou la compétition, veuillez réessayer")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))#redirect


if __name__ == "__main__":
    app.run(debug=True)
