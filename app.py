# app.py

from flask import Flask, render_template, request, redirect, url_for
import csv
import json
import matplotlib.pyplot as plt 
import os 
from random import choice  # Import choice from the random module


app = Flask(__name__)

questions = [
    {'id': 1, 'question': 'Do you like Flask?'},
    # Add more questions as needed
]

responses = []
labels=[]

@app.route('/')
def index():
    question = questions[0]['question']
    images = [image for image in os.listdir(os.path.join(app.static_folder, 'images')) if image.endswith(('.png', '.jpg', '.jpeg'))]
    random_image = choice(images) if images else None
    return render_template('index.html', question=question, randomImage=random_image)

@app.route('/submit', methods=['POST'])
def submit():
    response = request.form['response']
    responses.append(response)

    label = request.form['label']
    labels.append(label)

    


    # Get mouse tracking data
    mouse_data = request.form['mouse_data']

    # Get the label from the form
    label = request.form['label']

    try:
        mouse_data_list = json.loads(mouse_data)
    except json.JSONDecodeError:
        mouse_data_list = []

    # Add mouse tracking data to CSV file with the label
    write_mouse_tracking_to_csv(label, response, mouse_data_list)

    # Move to the next question or show results when all questions are answered
    next_question_index = len(responses)
    if next_question_index < len(questions):
        question = questions[next_question_index]['question']
        return render_template('index.html', question=question)
    else:
        return redirect(url_for('results'))


# def write_mouse_tracking_to_csv(response, mouse_data_list):
#     cor_x=[]
#     cor_y=[]

#     for i in mouse_data_list:
#         print("hello")
#         print(type(i))
#         cor_x.append(i["x"])
#         cor_y.append(i["y"])
def write_mouse_tracking_to_csv(label, response, mouse_data_list):
    cor_x = []
    cor_y = []

    for i in mouse_data_list:
        cor_x.append(i["x"])
        cor_y.append(i["y"])


    print(cor_x)
    print(cor_y)

    plt.plot(cor_x, cor_y) 
    plt.show()


    # with open('mouse_tracking.csv', mode='a', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow([response, mouse_data_list])


    with open('mouse_tracking.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Add the label as the first element in the row
        writer.writerow([label, response] + cor_x + cor_y)



@app.route('/results')
def results():
    # Display survey results
    zipped_data = zip(responses, labels)
    return render_template('results.html', responses=responses,zipped_data=zipped_data)

if __name__ == '__main__':
    app.run(debug=True)