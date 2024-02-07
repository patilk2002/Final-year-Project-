# app.py

from flask import Flask, render_template, request, redirect, url_for
import csv
import json
import matplotlib.pyplot as plt 
import os 
from random import choice  # Import choice from the random module
from datetime import datetime

app = Flask(__name__)

questions = [
    {'id': 1, 'question': 'Do you like Flask?'},
]

responses = []
labels=[]
image_name=""


@app.route('/')
def index():
    # question = questions[0]['question']
    images = [image for image in os.listdir(os.path.join(app.static_folder, 'images')) if image.endswith(('.png', '.jpg', '.jpeg'))]
    random_image = choice(images) if images else None
    image_name=random_image[:-6]
    question= "Do you think this image representing "+random_image[:-10]+" ?"

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

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')


    folder_path = os.path.join("static", "graphs", label)
    os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist

    cor_x = [point["x"] for point in mouse_data_list]
    cor_y = [point["y"] for point in mouse_data_list]

    plt.plot(cor_x, cor_y)
    plt.title("Mouse Tracking")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.xlim([0, 1600])
    plt.ylim([0, 700])
    graph_path = os.path.join(folder_path, f"{label}_{timestamp}_graph.png")
    plt.savefig(graph_path)
    plt.show()
    plt.close()





    for i in mouse_data_list:
        cor_x.append(i["x"])
        cor_y.append(i["y"])

    print(cor_x)
    print(cor_y)

    plt.plot(cor_x, cor_y) 
    plt.xlim([0, 1600])
    plt.ylim([0, 700])
    # plt.show()
    plt.close()

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