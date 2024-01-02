from sklearn.metrics import roc_auc_score
from web3 import Web3
import numpy as np
import tensorflow as tf
import ipfshttpclient
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from preprocessing import clients, x_test, y_test

# Connect to Ganache
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Smart Contract Details
contract_address = '0x2fcfAe11b277157c27B12B182FE61c53D6fd1691'
contract_abi = [
    {
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "string",
          "name": "weightsHash",
          "type": "string"
        }
      ],
      "name": "AggregatedWeightsStored",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "collaborator",
          "type": "address"
        }
      ],
      "name": "CollaboratorAdded",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "collaborator",
          "type": "address"
        }
      ],
      "name": "CollaboratorRemoved",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "uint256",
          "name": "nodeId",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "weightsHash",
          "type": "string"
        }
      ],
      "name": "WeightsStored",
      "type": "event"
    },
    {
      "inputs": [],
      "name": "aggregatedWeightsHash",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "collaborators",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "nodeWeightsHashes",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [],
      "name": "owner",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "collaborator",
          "type": "address"
        }
      ],
      "name": "addCollaborator",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "collaborator",
          "type": "address"
        }
      ],
      "name": "removeCollaborator",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "nodeId",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "weightsHash",
          "type": "string"
        }
      ],
      "name": "storeNodeWeights",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "nodeId",
          "type": "uint256"
        }
      ],
      "name": "getNodeWeightsHash",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "weightsHash",
          "type": "string"
        }
      ],
      "name": "storeAggregatedWeights",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "getAggregatedWeightsHash",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    }
  ]

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

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
def test_model(model, x_test, y_test):
  # Predict probabilities for the test set
  y_pred_probs = model.predict(x_test)

  # Calculate AUC
  auc = roc_auc_score(y_test, y_pred_probs)
  return auc
# Load dataset
left_client_data = clients["left"]

# Accessing the training splits
x_train = left_client_data["train"]["x"]
y_train = left_client_data["train"]["y"]

# Training the model
model = build_model(x_train.shape[1])
model.fit(x_train, y_train, epochs=10, batch_size=64, verbose=0)

auc_score = test_model(model, x_test, y_test)
print(f"Node 1 Model AUC: {auc_score}")
# Serialize and save model weights
model.save_weights("model_weights.h5")

# Connect to IPFS
client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

# Add file to IPFS
res = client.add("model_weights.h5")
weights_hash = res['Hash']
print("Uploaded to IPFS with hash:", weights_hash)

# Store the IPFS hash in the blockchain
node_id = 1  # Unique identifier for this node
tx_hash = contract.functions.storeNodeWeights(node_id, weights_hash).transact({
    'from': web3.eth.accounts[1]  # Use the appropriate account
})

web3.eth.wait_for_transaction_receipt(tx_hash)
