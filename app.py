from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Survey question
question = "Do you enjoy using Flask?"

# Survey responses
responses = []


@app.route("/")
def index():
    return render_template("index.html", question=question)


@app.route("/submit", methods=["POST"])
def submit():
    response = request.form.get("response")
    responses.append(response)
    return redirect(url_for("index"))


@app.route("/results")
def results():
    return render_template("results.html", question=question, responses=responses)


if __name__ == "__main__":
    app.run(debug=True)
