from web3 import Web3

# Connect to Ganache
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Smart Contract Details
contract_address = '0x401f2a50C8B4d529f065ECD984dDbC88fd35f73b'
contract_abi = [
    {
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
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
          "name": "number",
          "type": "uint256"
        }
      ],
      "name": "addNumber",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "index",
          "type": "uint256"
        }
      ],
      "name": "deleteNumber",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "getNumbers",
      "outputs": [
        {
          "internalType": "uint256[]",
          "name": "",
          "type": "uint256[]"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    }
]

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def add_collaborator(collaborator_address):
    tx_hash = contract.functions.addCollaborator(collaborator_address).transact({
        'from': web3.eth.accounts[0]  # Explicitly specifying the from address
    })
    web3.eth.wait_for_transaction_receipt(tx_hash)  # Corrected method call

def get_numbers():
    return contract.functions.getNumbers().call()

def delete_number(index):
    tx_hash = contract.functions.deleteNumber(index).transact({
        'from': web3.eth.accounts[0]  # Explicitly specifying the from address
    })
    web3.eth.wait_for_transaction_receipt(tx_hash)  # Corrected method call

def remove_collaborator(collaborator_address):
    tx_hash = contract.functions.removeCollaborator(collaborator_address).transact({
        'from': web3.eth.accounts[0]  # Explicitly specifying the from address
    })
    web3.eth.wait_for_transaction_receipt(tx_hash)  # Corrected method call

if __name__ == "__main__":
    # Add node accounts as collaborators
    node_accounts = [web3.eth.accounts[1], web3.eth.accounts[2], web3.eth.accounts[3]]  # Add other node accounts if necessary
    for account in node_accounts:
        add_collaborator(account)

    remove_collaborator(web3.eth.accounts[1])
    # Retrieve and print the list of numbers
    print("Numbers in the list:", get_numbers())