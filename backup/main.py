from flask import Flask, render_template
from scrapper import steam


app = Flask(__name__)
CURRENT_PASSWORD = "Test"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/v1/<password>/steam")
def steam_giveaway(password):
    if password == CURRENT_PASSWORD:
        giveaways = steam()
        return giveaways if len(giveaways) > 0 else "No ongoing giveaways"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
