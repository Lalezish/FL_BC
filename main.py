import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam

# Suppress warnings and additional information

import os
import tensorflow as tf
import warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logging
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)  # Suppress TensorFlow v1.x warnings
warnings.filterwarnings('ignore')  # Ignore Python warnings


# Data loading
dataPath = "data"
dataBottom = pd.read_csv(dataPath + "/output_bottom.csv")
dataLeft = pd.read_csv(dataPath + "/output_left.csv")
dataRight = pd.read_csv(dataPath + "/output_right.csv")

### DATA PREPROCESSING

# Assigning column names
column_names = ["sAddress",
           "rAddress",
           "sMACs",
           "rMACs",
           "sIPs",
           "rIPs",
           "protocol",
           "startDate",
           "endDate",
           "start",
           "end",
           "startOffset",
           "endOffset",
           "duration",
           "sPackets",
           "rPackets",
           "sBytesSum",
           "rBytesSum",
           "sBytesMax",
           "rBytesMax",
           "sBytesMin",
           "rBytesMin",
           "sBytesAvg",
           "rBytesAvg",
           "sLoad",
           "rLoad",
           "sPayloadSum",
           "rPayloadSum",
           "sPayloadMax",
           "rPayloadMax",
           "sPayloadMin",
           "rPayloadMin",
           "sPayloadAvg",
           "rPayloadAvg",
           "sInterPacketAvg",
           "rInterPacketAvg",
           "sttl",
           "rttl",
           "sAckRate",
           "rAckRate",
           "sUrgRate",
           "rUrgRate",
           "sFinRate",
           "rFinRate",
           "sPshRate",
           "rPshRate",
           "sSynRate",
           "rSynRate",
           "sRstRate",
           "rRstRate",
           "sWinTCP",
           "rWinTCP",
           "sFragmentRate",
           "rFragmentRate",
           "sAckDelayMax",
           "rAckDelayMax",
           "sAckDelayMin",
           "rAckDelayMin",
           "sAckDelayAvg",
           "rAckDelayAvg",
           "IT_B_Label",
           "IT_M_Label",
           "NST_B_Label",
           "NST_M_Label"
           ]
dataBottom.columns = column_names
dataLeft.columns = column_names
dataRight.columns = column_names

# Removing unusable column
remove_columns = ["startDate", "endDate", "start", "end", "startOffset", "endOffset",
                  "sAddress", "rAddress", "sMACs", "rMACs", "sIPs", "rIPs",
                  "IT_B_Label", "IT_M_Label", "NST_B_Label"] # Other labels not used
dataBottom = dataBottom.drop(columns = remove_columns)
dataLeft = dataLeft.drop(columns = remove_columns)
dataRight = dataRight.drop(columns = remove_columns)

# Filling empty cells
dataBottom = dataBottom.replace([np.inf, -np.inf], -1)
dataLeft = dataLeft.replace([np.inf, -np.inf], -1)
dataRight = dataRight.replace([np.inf, -np.inf], -1)
dataBottom = dataBottom.replace(np.nan, -1)
dataLeft = dataLeft.replace(np.nan, -1)
dataRight = dataRight.replace(np.nan, -1)

# GOOD-SSH -> Normal
indr = dataRight["NST_M_Label"] == 'GOOD-SSH'
dataRight.loc[indr, "NST_M_Label"] = 'Normal'
indl = dataLeft["NST_M_Label"] == 'GOOD-SSH'
dataLeft.loc[indl, "NST_M_Label"] = 'Normal'
indb = dataBottom["NST_M_Label"] == 'GOOD-SSH'
dataBottom.loc[indb, "NST_M_Label"] = 'Normal'

# Extracting label column
boty = dataBottom["NST_M_Label"]
botx = dataBottom.drop(columns=["NST_M_Label"], axis = 1)
lefty = dataLeft["NST_M_Label"]
leftx = dataLeft.drop(columns=["NST_M_Label"], axis = 1)
righty = dataRight["NST_M_Label"]
rightx = dataRight.drop(columns=["NST_M_Label"], axis = 1)

# Attack detection without classification
boty = np.where(boty == "Normal", 0, 1)
lefty = np.where(lefty == "Normal", 0, 1)
righty = np.where(righty == "Normal", 0, 1)

# Encoding protocol column
label_encoder = LabelEncoder()
protocols = pd.concat([leftx['protocol'], botx['protocol'], rightx['protocol']])
label_encoder.fit(protocols)

botx['protocol'] = label_encoder.transform(botx['protocol'])
botxn = botx.values

leftx['protocol'] = label_encoder.transform(leftx['protocol'])
leftxn = leftx.values

rightx['protocol'] = label_encoder.transform(rightx['protocol'])
rightxn = rightx.values

# Splitting the dataset
# Train =  70%, Validate = 10%, Test = 20%
x_train_bottom, x_rest_bottom, y_train_bottom, y_rest_bottom = train_test_split(botxn, boty, test_size = 0.3, stratify=boty, random_state=42)
x_validate_bottom, x_test_bottom, y_validate_bottom, y_test_bottom = train_test_split(x_rest_bottom, y_rest_bottom, test_size = 0.67, stratify=y_rest_bottom, random_state=42)

x_train_left, x_rest_left, y_train_left, y_rest_left = train_test_split(leftxn, lefty, test_size = 0.3, stratify=lefty, random_state=42)
x_validate_left, x_test_left, y_validate_left, y_test_left = train_test_split(x_rest_left, y_rest_left, test_size = 0.67, stratify=y_rest_left, random_state=42)

x_train_right, x_rest_right, y_train_right, y_rest_right = train_test_split(rightxn, righty, test_size = 0.3, stratify=righty, random_state=42)
x_validate_right, x_test_right, y_validate_right, y_test_right = train_test_split(x_rest_right, y_rest_right, test_size = 0.67, stratify=y_rest_right, random_state=42)

# Normalizing in order to prevent "large value"-features to have greater importance.
min_max_scaler = MinMaxScaler().fit(x_train_bottom)
min_max_scaler = MinMaxScaler().fit(x_train_left)
min_max_scaler = MinMaxScaler().fit(x_train_right)

x_train_bottom = min_max_scaler.transform(x_train_bottom)
x_validate_bottom = min_max_scaler.transform(x_validate_bottom)
x_test_bottom = min_max_scaler.transform(x_test_bottom)
x_train_left = min_max_scaler.transform(x_train_left)
x_validate_left = min_max_scaler.transform(x_validate_left)
x_test_left = min_max_scaler.transform(x_test_left)
x_train_right = min_max_scaler.transform(x_train_right)
x_validate_right = min_max_scaler.transform(x_validate_right)
x_test_right = min_max_scaler.transform(x_test_right)

### END OF DATA PREPROCESSING

# Final test-set used for all experiments
x_test = np.concatenate([x_test_bottom, x_test_left, x_test_right])
y_test = np.concatenate([y_test_bottom, y_test_left, y_test_right])

# Concatenated training and validation-set used for Non-FL
x_train = np.concatenate([x_train_bottom, x_train_left, x_train_right])
y_train = np.concatenate([y_train_bottom, y_train_left, y_train_right])
x_validate = np.concatenate([x_validate_bottom, x_validate_left, x_validate_right])
y_validate = np.concatenate([y_validate_bottom, y_validate_left, y_validate_right])

# Clients data dictionary
clients = {
    "left": {"train": {"x": x_train_left, "y": y_train_left}, "validate": {"x": x_validate_left, "y": y_validate_left}, "test": {"x": x_test_left, "y": y_test_left}},
    "right": {"train": {"x": x_train_right, "y": y_train_right}, "validate": {"x": x_validate_right, "y": y_validate_right}, "test": {"x": x_test_right, "y": y_test_right}},
    "bottom": {"train": {"x": x_train_bottom, "y": y_train_bottom}, "validate": {"x": x_validate_bottom, "y": y_validate_bottom}, "test": {"x": x_test_bottom, "y": y_test_bottom}}
}

def build_model(input_shape):
    model = Sequential()
    model.add(Dense(64, input_shape=(input_shape,), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer=Adam(learning_rate=0.001),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model

# Function to train a model on a specific dataset
def train_model_on_client(data, epochs=10, batch_size=64):
    x_train, y_train = data['train']['x'], data['train']['y']
    x_validate, y_validate = data['validate']['x'], data['validate']['y']

    model = build_model(x_train.shape[1])
    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_validate, y_validate),
              verbose=0)
    return model

# Averaging weights for Federated Learning
def average_weights(models):
    weights = [model.get_weights() for model in models.values()]
    new_weights = []

    for weights_list_tuple in zip(*weights):
        new_weights.append(np.mean(np.array(weights_list_tuple), axis=0))

    return new_weights

# Train a model on each dataset
models = {}
for client, data in clients.items():
    model = train_model_on_client(data)
    models[client] = model

averaged_weights = average_weights(models)

# Apply averaged weights to a new model
federated_model = build_model(x_train.shape[1])
federated_model.set_weights(averaged_weights)

# Evaluating the Federated Learning model
federated_predictions = federated_model.predict(x_test)
federated_auc_score = roc_auc_score(y_test, federated_predictions)

print('--------------------------------------------------------------------------------------')
print('Federated Learning Model AUC: ' + str(federated_auc_score))
print('--------------------------------------------------------------------------------------')

# Training the Neural Network on combined dataset
epochs = 10
batch_size = 64
nn_model = build_model(x_train.shape[1])
nn_model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_validate, y_validate), verbose=0)

# Evaluating the model trained on combined dataset
nn_predictions = nn_model.predict(x_test)
nn_auc_score = roc_auc_score(y_test, nn_predictions)

# Print Neural Network AUC for the combined dataset
print('--------------------------------------------------------------------------------------')
print('Neural Network AUC on Combined Data: ' + str(nn_auc_score))
print('--------------------------------------------------------------------------------------')