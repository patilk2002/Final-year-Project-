



    #################################################### ML Part start    ###########################################################



    import numpy as np
    import pandas as pd
    from tensorflow.keras.models import load_model
    import os
    os.environ['TF_KERAS'] = '1'
    # Load the trained model
    # model = load_model('RNN.h5')

    import tensorflow as tf

    # Load the trained model using tf.keras
    model = tf.keras.models.load_model('RNN.h5', compile=False)

    # Load the trained model without compiling
    # model = load_model('RNN.h5', compile=False)

    # Sample data for prediction
    sample_data = {
        'Response_Time': [1086.0],
        'Speed': [407.962582],
        'Velocity': [404.318571],
        'maximum_positive_deviation': [5.010363],
        'maximum_negative_deviation': [-15.076637],
        'DTW': [4.337719],
        'Direction_Change_Freq_10': [0.304348],
        'Direction_Change_Freq_30': [0.043478],
        'Direction_Change_Freq_45': [0.0],
        'Direction_Change_Freq_90': [0.0],
        'centroid_mp_dist': [-58.869943],
        'Img_Radius': [278.36248],
        'Slope': [1.740901],
        'Narrowness': [0.001006]
    }

    # Convert sample data to DataFrame
    df = pd.DataFrame(sample_data)

    # Preprocess the data (if necessary)
    # You might need to scale the features, handle missing values, etc.

    # Reshape input data to match the input shape expected by the model
    X_pred = df.values.reshape(1, 1, df.shape[1])

    # Make prediction
    predicted_probability = model.predict(X_pred)

    # Convert predicted probability to class label
    predicted_class = (predicted_probability > 0.5).astype(int)

    print("Predicted Probability:", predicted_probability)
    print("Predicted Class:", predicted_class)




    #################################################### ML Part End  ###########################################################

