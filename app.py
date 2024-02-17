# app.py
from flask import Flask, render_template, request, redirect, url_for
import csv
import json
import matplotlib
import matplotlib.pyplot as plt
import os
from random import choice
from datetime import datetime
from threading import Thread

app = Flask(__name__)

questions = [
    {'id': 1, 'question': 'Do you like Flask?'},
]

userId = ""
age = ""
gender = ""
occupation = ""
computerOpSkill = ""
initialEmotion = ""

responses = []
labels = []
image_name = ""
responseTimes = []
currentEmotions = []

# Force Matplotlib to use non-interactive backend
matplotlib.use('Agg')

def plot_mouse_tracking(label, mouse_data_list):
    cor_x = [point["x"] for point in mouse_data_list]
    cor_y = [point["y"] for point in mouse_data_list]

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')

    folder_path = os.path.join("static", "graphs", label)
    os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist

    plt.plot(cor_x, cor_y)
    plt.title("Mouse Tracking")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.xlim([0, 1600])
    plt.ylim([0, 700])
    graph_path = os.path.join(folder_path, f"{label}_{timestamp}_graph.png")
    plt.savefig(graph_path)
    plt.close()


def write_mouse_tracking_to_csv(userId, initialEmotion, age, gender, occupation, computerOpSkill, label, response, responseTime, currentEmotion, mouse_data_list):
    # Plotting in a separate thread to avoid Matplotlib warning
    plot_thread = Thread(target=plot_mouse_tracking, args=(label, mouse_data_list))
    plot_thread.start()

    cor_x = [point["x"] for point in mouse_data_list]
    cor_y = [point["y"] for point in mouse_data_list]

    for i in mouse_data_list:
        cor_x.append(i["x"])
        cor_y.append(i["y"])

    with open('mouse_tracking.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([userId, initialEmotion, age, gender, occupation, computerOpSkill, label, response, responseTime, currentEmotion] + cor_x + cor_y)

    with open('mouse_tracking_new.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Add the label as the first element in the row
        writer.writerow([userId, initialEmotion, age, gender, occupation, computerOpSkill, label, response, responseTime, currentEmotion,mouse_data_list])

@app.route('/')
def index():
    images = [image for image in os.listdir(os.path.join(app.static_folder, 'images')) if
              image.endswith(('.png', '.jpg', '.jpeg'))]
    random_image = choice(images) if images else None
    
    image_emotion=random_image[:-10]
    image_emotion_type=''
    if image_emotion not in ['amusement', 'awe', 'contentment', 'excitement'] :
        image_emotion_type = '-negative'

    question= "Do you think this image representing "+random_image[:-10]+" ?"

    return render_template('index.html', question=question, randomImage=random_image, imageEmotionType=image_emotion_type)



@app.route('/submit', methods=['POST'])
def submit():
    userId = request.form['userId']
    age = request.form['age']
    gender = request.form['gender']
    occupation = request.form['occupation']
    computerOpSkill = request.form['computerOpSkill']
    initialEmotion = request.form['initialEmotion']

    print("age : ", age)
    print("userId : ", userId)

    response = request.form['response']
    responses.append(response)

    label = request.form['label']
    labels.append(label)

    # Get mouse tracking data
    mouse_data = request.form['mouse_data']

    responseTime = request.form['responseTime']
    responseTimes.append(responseTime)

    currentEmotion = request.form['currentEmotion']
    currentEmotions.append(currentEmotion)

    # Get mouse tracking data
    mouse_data = request.form['mouse_data']

    print("\n")

    print("mouse data")
    print(mouse_data)
    
    print("\n")
    print("response")
    print(response)

    # Get the label from the form
    label = request.form['label']

    try:
        mouse_data_list = json.loads(mouse_data)
    except json.JSONDecodeError:
        mouse_data_list = []

    # Add mouse tracking data to CSV file with the label
    write_mouse_tracking_to_csv(userId, initialEmotion, age, gender, occupation, computerOpSkill, label, response, responseTime, currentEmotion, mouse_data_list)

    # Move to the next question or show results when all questions are answered
    next_question_index = len(responses)
    if next_question_index < len(questions):
        question = questions[next_question_index]['question']
        return render_template('index.html', question=question)
    else:
        return redirect(url_for('results'))

@app.route('/results')
def results():
    # Display survey results
    zipped_data = zip(responses, labels, responseTimes, currentEmotions)
    return render_template('results.html', responses=responses, zipped_data=zipped_data)

if __name__ == '__main__':
    app.run(debug=True)