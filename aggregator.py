from web3 import Web3
import numpy as np
import tensorflow as tf
import os
import ipfshttpclient
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import roc_auc_score
from preprocessing import x_test, y_test

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

def average_weights(weights_list):
    # Suboptimal, but sufficent method of merging models
    # Average the weights from different models
    avg_weights = []
    for weights in zip(*weights_list):
        layer_mean = np.mean(np.array(weights), axis=0)
        avg_weights.append(layer_mean)
    return avg_weights

def save_and_upload_weights_to_ipfs(model):
    # Save model weights to a file
    model.save_weights("aggregated_model_weights.h5")

    # Connect to IPFS
    client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

    # Add file to IPFS
    res = client.add("aggregated_model_weights.h5")
    weights_hash = res['Hash']
    print("Uploaded aggregated weights to IPFS with hash:", weights_hash)
    return weights_hash

if __name__ == "__main__":
    input_shape = x_test.shape[1]  # Assuming x_test is a 2D array
    model = build_model(input_shape)

    all_weights = []  # List to store weights from each node

    for node_id in range(1, 4):  # 3 Nodes
        weights_hash = contract.functions.getNodeWeightsHash(node_id).call()
        load_weights_from_ipfs(model, weights_hash)
        all_weights.append(model.get_weights())

    # Average the weights
    averaged_weights = average_weights(all_weights)
    model.set_weights(averaged_weights)  # Set the averaged weights to the model

    # Save and upload the aggregated weights to IPFS
    aggregated_weights_hash = save_and_upload_weights_to_ipfs(model)

    # Store the IPFS hash of the aggregated weights in the blockchain
    tx_hash = contract.functions.storeAggregatedWeights(aggregated_weights_hash).transact({
        'from': web3.eth.accounts[0]
    })
    web3.eth.wait_for_transaction_receipt(tx_hash)

    # Test the combined model
    combined_auc_score = test_model(model, x_test, y_test)
    print(f"Combined Model AUC: {combined_auc_score}")
