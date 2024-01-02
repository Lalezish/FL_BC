from web3 import Web3

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

def add_collaborator(account_address):
    tx_hash = contract.functions.addCollaborator(account_address).transact({
        'from': web3.eth.accounts[0]  # First account is contract owner
    })
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Collaborator {account_address} added.")

if __name__ == "__main__":
    # Add collaborators
    collaborator_addresses = [web3.eth.accounts[1], web3.eth.accounts[2], web3.eth.accounts[3]]
    for address in collaborator_addresses:
        add_collaborator(address)
