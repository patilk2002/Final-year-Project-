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
import pandas as pd 
from random import sample


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

random_images = []
random_videos = []



# Force Matplotlib to use non-interactive backend
matplotlib.use('Agg')

def plot_mouse_tracking(label, mouse_data_list, timestamp):
    cor_x = [point["x"] for point in mouse_data_list]
    cor_y = [700-point["y"] for point in mouse_data_list]

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


def write_mouse_tracking_to_csv(userId, initialEmotion, age, gender, occupation, computerOpSkill, label, response, responseTime, currentEmotion, mouse_data_list, no_of_clicks, mouse_clicks_list, mouse_downtimes_list):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
    # Plotting in a separate thread to avoid Matplotlib warning
    plot_thread = Thread(target=plot_mouse_tracking, args=(label, mouse_data_list, timestamp))
    plot_thread.start()

    cor_x = [point["x"] for point in mouse_data_list]
    cor_y = [700-point["y"] for point in mouse_data_list]

    for i in mouse_data_list:
        cor_x.append(i["x"])
        cor_y.append(i["y"])

    graph_name = label+"_"+timestamp+"_graph.png"

    with open('mouse_tracking.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([userId, initialEmotion, age, gender, occupation, computerOpSkill, label, response, responseTime, currentEmotion] + cor_x + cor_y)

    with open('mouse_tracking_new.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Add the label as the first element in the row
        writer.writerow([userId, initialEmotion, age, gender, occupation, computerOpSkill, label, response, responseTime, currentEmotion,mouse_data_list, no_of_clicks, mouse_clicks_list, mouse_downtimes_list])


    # File path of the CSV file
    csv_file_path = 'mouse_tracking_final.csv'

    # Field names (header)
    header = ['User_ID', 'Initial_Emotion', 'Age', 'Gender', 'Occupation', 'Computer_Operating_Skill', 'Label', 'Response', 'Response_Time', 'Current_Emotion', 'Mouse_Data', 'Mouse_Clicks', 'Mouse_Clicks_List', 'Mouse_Downtime_List', 'Graph_file']

    # Check if the file already exists and is not empty
    file_exists = os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0

    # Writing data to the CSV file with a header if it doesn't already exist
    with open(csv_file_path, mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)

        # Write the header only if the file is empty
        if not file_exists:
            writer.writerow(header)
            
        # Add the label as the first element in the row
        writer.writerow([userId, initialEmotion, age, gender, occupation, computerOpSkill, label, response, responseTime, currentEmotion, mouse_data_list, no_of_clicks, mouse_clicks_list, mouse_downtimes_list, graph_name])





@app.route('/')
def index():
    # images = [image for image in os.listdir(os.path.join(app.static_folder, 'images')) if
    #           image.endswith(('.png', '.jpg', '.jpeg'))]
    # random_image = choice(images) if images else None

    # Define the paths to your image and video datasets
    image_folder = 'Image_dataset'
    video_folder = 'Video_dataset'

    # Function to get a list of random files from a folder
    def get_random_files(folder, num_files):
        files = [f for f in os.listdir(folder)]
        return sample(files, min(num_files, len(files)))

    # Select 6 random images and 4 random videos
    random_images = get_random_files(os.path.join(app.static_folder, 'images/Image_dataset'), 5)
    random_videos = get_random_files(os.path.join(app.static_folder, 'images/Video_dataset'), 5)

    # Create the final list alternating between images and videos
    final_list = []
    for i in range(5):
        final_list.append(random_images[i])
        final_list.append(random_videos[i])

    global count
    count = len(responses)
    random_image = final_list[count-1]
    print(count)
    print(random_image)
    
    
    # count+=1

    image_emotion=random_image[:-10]
    image_emotion_type=''
    if image_emotion not in ['amusement', 'awe', 'contentment', 'excitement'] :
        image_emotion_type = '-negative'

    # question= "Do you think this image representing "+random_image[:-10]+" ?"
    # debugging 
    # Specify the file path
    csv_file_path = 'static/questions/MMPI_questions.csv'

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    df.columns = ['Sr','Question','ans1','ans2','ans3','ans4','ans5']
    # print("\n")
    # print("\n")
    random_row = df.sample(n=1)
    # print(random_row)
    question = random_row['Question'].values[0]
    return render_template('index.html', question=question, randomImage=random_image, imageEmotionType=image_emotion_type)



@app.route('/submit', methods=['POST'])
def submit():
    global userId, age, gender, occupation, computerOpSkill, initialEmotion
    if userId=="":
        userId = request.form['userId']
        age = request.form['age']
        gender = request.form['gender']
        occupation = request.form['occupation']
        computerOpSkill = request.form['computerOpSkill']
        initialEmotion = request.form['initialEmotion']

    # print("age : ", age)
    # print("userId : ", userId)

    response = request.form['response']
    responses.append(response)

    label = request.form['label']
    labels.append(label)

    # Get mouse tracking data
    mouse_data = request.form['mouse_data']
    mouse_clicks = request.form['mouse_clicks']
    mouse_downtimes = request.form['mouse_downtimes']
    mouse_downtimes_list = mouse_downtimes[1:-1].split(",")
    no_of_clicks = len(mouse_downtimes_list)

    responseTime = request.form['responseTime']
    responseTimes.append(responseTime)

    currentEmotion = request.form['currentEmotion']
    currentEmotions.append(currentEmotion)

    # Get mouse tracking data
    mouse_data = request.form['mouse_data']

    # print("\n")

    print("mouse downtimes")
    print(mouse_downtimes)
    print(no_of_clicks)
    # print("mouse data")
    # print(mouse_data)
    
    # print("\n")
    # print("response")
    # print(response)

    # Get the label from the form
    label = request.form['label']

    try:
        mouse_data_list = json.loads(mouse_data)
    except json.JSONDecodeError:
        mouse_data_list = []
    
    try:
        mouse_clicks_list = json.loads(mouse_clicks)
    except json.JSONDecodeError:
        mouse_clicks_list = []                       

    # Add mouse tracking data to CSV file with the label
    write_mouse_tracking_to_csv(userId, initialEmotion, age, gender, occupation, computerOpSkill, label, response, responseTime, currentEmotion, mouse_data_list, no_of_clicks, mouse_clicks_list, mouse_downtimes_list)

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