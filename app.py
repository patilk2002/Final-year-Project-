# app.py
import math
import random
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

stimuli_list = []
random_images = []
random_videos = []

user_number = 0
emotions_list = ['amusement','anger','contentment','disgust','excitement','fear','awe','sadness']

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


def write_mouse_tracking_to_csv(userId, initialEmotion, age, gender, occupation, computerOpSkill, label, stimulus, response, responseTime, currentEmotion, mouse_data_list, no_of_clicks, mouse_clicks_list, mouse_downtimes_list, click_moments_list, speed, velocity):
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
    header = ['User_ID', 'Initial_Emotion', 'Age', 'Gender', 'Occupation', 'Computer_Operating_Skill', 'Label', 'Stimulus', 'Response', 'Response_Time', 'Current_Emotion', 'Mouse_Data', 'Mouse_Clicks', 'Mouse_Clicks_List', 'Mouse_Downtime_List', 'Click_Moments_List', 'Speed', 'Velocity', 'Graph_file']

    # Check if the file already exists and is not empty
    file_exists = os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0

    # Writing data to the CSV file with a header if it doesn't already exist
    with open(csv_file_path, mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)

        # Write the header only if the file is empty
        if not file_exists:
            writer.writerow(header)
            
        # Add the label as the first element in the row
        writer.writerow([userId, initialEmotion, age, gender, occupation, computerOpSkill, label, stimulus, response, responseTime, currentEmotion, mouse_data_list, no_of_clicks, mouse_clicks_list, mouse_downtimes_list, click_moments_list, speed, velocity, graph_name])


# Function to calculate Euclidean distance between two points
def euclidean_distance(point1, point2):
    return math.sqrt((point2['x'] - point1['x'])**2 + (point2['y'] - point1['y'])**2)


@app.route('/')
def index():
    global user_number, responses, stimuli_list, random_videos, random_images, userId, age, gender, occupation, computerOpSkill, initialEmotion,labels, image_name, responseTimes, currentEmotions
    if(len(responses)>=8):
        user_number+=1
        stimuli_list=[]
        random_images=[]
        random_videos=[]
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
        emotions=[]
        
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

    # Function to get a list of random files from a folder that start with a specific prefix
    def get_random_files_with_prefix(folder, prefix, num_files):
        files = [f for f in os.listdir(folder) if f.startswith(prefix)]
        return sample(files, min(num_files, len(files)))


    
    emotion=['amusement', 'anger' ,'contentment', 'disgust', 'excitement', 'fear', 'awe', 'sadness']

    Videos={'amusement':'<iframe width="560" height="315" src="https://www.youtube.com/embed/oAJLKDMihnU?si=1LI1icnTSl6m3gZk&amp;controls=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>', 
    'anger':'<iframe width="560" height="315" src="https://www.youtube.com/embed/guVlUIt-eP4?si=ThXOTkgF7BjIoLul&amp;controls=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>' ,
    'contentment':'<iframe width="560" height="315" src="https://www.youtube.com/embed/RP4abiHdQpc?si=6ZevSq63NlAb_cHD&amp;controls=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>', 
    'disgust': '<iframe width="560" height="315" src="https://www.youtube.com/embed/yekWI59YWTg?si=rFBYReNokzbpMk9K&amp;controls=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>', 
    'excitement': '<iframe width="560" height="315" src="https://www.youtube.com/embed/8L3QSt6f3dM?si=mrFR2SI6JKjeJuj_&amp;controls=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>', 
    'fear':'<iframe width="560" height="315" src="https://www.youtube.com/embed/gbWE47w2oLE?si=QUj_WuoXZ3nDE-N2&amp;controls=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>', 'awe':'<iframe width="560" height="315" src="https://www.youtube.com/embed/kzZQYnvw-6E?si=bE1QX98n522tmRkR&amp;controls=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>', 
    'sadness':'<iframe width="560" height="315" src="https://www.youtube.com/embed/IpNG4ohSUkI?si=Auz1TNKwXXKYEDys&amp;controls=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'}

    count = len(responses)


    if(len(stimuli_list)==0 or count==0):
        # Select 6 random images and 4 random videos
        random.shuffle(emotion)

    print("/n/n/n check emotions :")
    print(emotion)

    print("/n/n/n")


    print(emotion)
    stimuli_list=[]
    stimuli_list.append(get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Image_dataset'), emotion[0], 1)[0])
    stimuli_list.append(get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Image_dataset'), emotion[1], 1)[0])
    stimuli_list.append(get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Image_dataset'), emotion[2], 1)[0])
    stimuli_list.append(get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Image_dataset'), emotion[3], 1)[0])

    stimuli_list.append(Videos[emotion[4]])
    stimuli_list.append(Videos[emotion[5]])
    stimuli_list.append(Videos[emotion[6]])
    stimuli_list.append(Videos[emotion[7]])


        # random_images = get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Image_dataset'), emotion[0], 1)
        # random_images.append (get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Image_dataset'), emotion[1], 1)[0])
        # random_images.append (get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Image_dataset'), emotion[2], 1)[0])
        # random_images.append (get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Image_dataset'), emotion[3], 1)[0])

        # random_videos = get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Video_dataset'),emotion[4], 1)
        # random_videos.append(get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Video_dataset'),emotion[5], 1)[0])
        # random_videos.append(get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Video_dataset'),emotion[6], 1)[0])
        # random_videos.append(get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Video_dataset'),emotion[7], 1)[0])
        
        
        # random_videos = []
        # random_videos.append(Videos[emotion[4]])
        # random_videos.append(Videos[emotion[5]])
        # random_videos.append(Videos[emotion[6]])
        # random_videos.append(Videos[emotion[7]])
                                                                                                                                                        
        # random_videos = get_random_files(os.path.join(app.static_folder, 'images/Video_dataset'), 5)

        # if(user_number%2):
        #     # pattern 1
        #     random_images = get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Image_dataset'), 'amusement', 1)
        #     random_images.append(get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Image_dataset'), 'anger', 1)[0])
        #     random_images.append(get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Image_dataset'), 'contentment', 1)[0])
        #     random_images.append(get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Image_dataset'), 'disgust', 1)[0])

        #     random_videos = get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Video_dataset'),'excitement', 1)
        #     random_videos.append(get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Video_dataset'),'fear', 1)[0])
        #     random_videos.append(get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Video_dataset'),'awe', 1)[0])
        #     random_videos.append(get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Video_dataset'),'sadness', 1)[0])
        # else:
        #     # pattern 2
        #     random_images = get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Image_dataset'), 'excitement', 1)
        #     random_images.append(get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Image_dataset'), 'fear', 1)[0])
        #     random_images.append(get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Image_dataset'), 'awe', 1)[0])
        #     random_images.append(get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Image_dataset'), 'sadness', 1)[0])

        #     random_videos = get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Video_dataset'),'amusement', 1)
        #     random_videos.append(get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Video_dataset'),'anger', 1)[0])
        #     random_videos.append(get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Video_dataset'),'contentment', 1)[0])
        #     random_videos.append(get_random_files_with_prefix(os.path.join(app.static_folder, 'images/Video_dataset'),'disgust', 1)[0])

        # for i in range(4):
        #     stimuli_list.append(random_images[i])
        #9     stimuli_list.append(random_videos[i])
        
        # random.shuffle(stimuli_list)

    print("Stimuli List ----->")

    print(stimuli_list)
    print(emotion)

    # random_image = final_list[count-1]
    # randInt=random.randint(0, 7)

    
    random_stimulus = stimuli_list[count]

    # print(count)
    # print(random_image)
    
    EmoLabel=emotion[count]
    print(EmoLabel)
    # count+=1

    image_emotion=random_stimulus[:-10]
    image_emotion_type=''
    if image_emotion not in ['amusement', 'awe', 'contentment', 'excitement'] :
        image_emotion_type = '-negative'


    # question= "Do you think this image representing "+random_image[:-10]+" ?"
    # debugging 
    # Specify the file path
    csv_file_path = 'static/questions/survey_questions_fyp.csv'

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    df.columns = ['Sr','Question']

    random_row = df.sample(n=1)
    # print(random_row)
    question = random_row['Question'].values[0]
    return render_template('index.html', question=question, randomImage=random_stimulus, imageEmotionType=image_emotion_type, EmoLabel=EmoLabel)



@app.route('/submit', methods=['POST'])
def submit():
    global userId, age, gender, occupation, computerOpSkill, initialEmotion
    # if userId=="":
    userId = request.form['userId']
    age = request.form['age']
    gender = request.form['gender']
    occupation = request.form['occupation']
    computerOpSkill = request.form['computerOpSkill']
    initialEmotion = request.form['initialEmotion']

    response = request.form['response']
    responses.append(response)

    label = request.form['label']
    stimulus = request.form['stimulus']
    labels.append(label)

    # Get mouse tracking data
    mouse_data = request.form['mouse_data']
    mouse_clicks = request.form['mouse_clicks']
    mouse_downtimes = request.form['mouse_downtimes']
    mouse_downtimes_list = [ int(i) for i in mouse_downtimes[1:-1].split(",") ]
    no_of_clicks = len(mouse_downtimes_list)
    click_moments = request.form['click_moments']
    click_moments_list = [ int(i) for i in click_moments[1:-1].split(",") ]

    responseTime = request.form['responseTime']
    responseTimes.append(responseTime)

    currentEmotion = request.form['currentEmotion']
    currentEmotions.append(currentEmotion)

    # Get mouse tracking data
    mouse_data = request.form['mouse_data']

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
   
    # Calculate Euclidean distance between consecutive coordinates and sum to get total distance
    distance = sum(euclidean_distance(mouse_data_list[i], mouse_data_list[i+1]) for i in range(len(mouse_data_list)-1))
    speed = distance * 1000 / float(responseTime)

    displacement = euclidean_distance(mouse_data_list[0], mouse_data_list[-1])
    velocity = displacement * 1000 / float(responseTime)

    # Add mouse tracking data to CSV file with the label
    write_mouse_tracking_to_csv(userId, initialEmotion, age, gender, occupation, computerOpSkill, label, stimulus, response, responseTime, currentEmotion, mouse_data_list, no_of_clicks, mouse_clicks_list, mouse_downtimes_list, click_moments_list, speed, velocity)

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