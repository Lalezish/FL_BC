import os

from web3 import Web3
import ipfshttpclient
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import roc_auc_score
from preprocessing import x_test, y_test

# Connect to Ganache
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Smart Contract Details
contract_address = '0x2fcfAe11b277157c27B12B182FE61c53D6fd1691'  # Replace with your contract address
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
def load_weights_from_ipfs(model, weights_hash):
    client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
    client.get(weights_hash)
    print(f"Downloaded {weights_hash}")

    downloaded_file_path = f"./{weights_hash}"
    renamed_file_path = f"./{weights_hash}.h5"

    # Rename the file to add .h5 extension
    if os.path.exists(downloaded_file_path):
        os.rename(downloaded_file_path, renamed_file_path)
        print(f"File renamed to {renamed_file_path}")

        # Load the weights from the renamed file
        model.load_weights(renamed_file_path)
        print(f"Weights loaded from {renamed_file_path}")
    else:
        print(f"File not found: {downloaded_file_path}")

def test_model(model, x_test, y_test):
    # Predict probabilities for the test set
    y_pred_probs = model.predict(x_test)

    # Calculate AUC
    auc = roc_auc_score(y_test, y_pred_probs)
    return auc

if __name__ == "__main__":
    input_shape = x_test.shape[1]  # Assuming x_test is a 2D array
    model = build_model(input_shape)

    # Retrieve the IPFS hash of the aggregated model's weights
    aggregated_weights_hash = contract.functions.getAggregatedWeightsHash().call()

    # Load the aggregated weights into the model
    load_weights_from_ipfs(model, aggregated_weights_hash)

    # Use the aggregated model to predict and evaluate on the test set
    auc_score = test_model(model, x_test, y_test)
    print(f"Aggregated Model AUC on Test Set: {auc_score}")

    # Print node 1 model for comparison
    #weights_hash = contract.functions.getNodeWeightsHash(1).call()
    #load_weights_from_ipfs(model, weights_hash)
    #auc_score = test_model(model, x_test, y_test)
    #print(f"Node 1 AUC on Test Set: {auc_score}")
