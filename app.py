# app.py

from flask import Flask, render_template, request, redirect, url_for
import csv
import json

app = Flask(__name__)

questions = [
    {'id': 1, 'question': 'Do you like Flask?'},
    # Add more questions as needed
]

responses = []

@app.route('/')
def index():
    question = questions[0]['question']  # Display the first question
    return render_template('index.html', question=question)


@app.route('/submit', methods=['POST'])
def submit():
    response = request.form['response']
    responses.append(response)

    print(responses)
    
    # Get mouse tracking data
    mouse_data = request.form['mouse_data']

    print('Received Mouse Data:', mouse_data)

    try:
        mouse_data_list = json.loads(mouse_data)
    except json.JSONDecodeError:
        mouse_data_list = []  # Handle the case where JSON decoding fails

    # Add mouse tracking data to CSV file
    write_mouse_tracking_to_csv(response, mouse_data_list)

    # Move to the next question or show results when all questions are answered
    next_question_index = len(responses)
    if next_question_index < len(questions):
        question = questions[next_question_index]['question']
        return render_template('index.html', question=question)
    else:
        return redirect(url_for('results'))


def write_mouse_tracking_to_csv(response, mouse_data_list):
    with open('mouse_tracking.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        for entry in mouse_data_list:
            writer.writerow([response, entry.get('x', ''), entry.get('y', '')])

@app.route('/results')
def results():
    # Display survey results
    return render_template('results.html', responses=responses)

if __name__ == '__main__':
    app.run(debug=True)