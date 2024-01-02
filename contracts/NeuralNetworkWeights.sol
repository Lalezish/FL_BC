pragma solidity ^0.8.0;

contract NeuralNetworkWeights {
    address public owner;
    mapping(address => bool) public collaborators;
    mapping(uint => string) public nodeWeightsHashes; // Mapping to store IPFS hashes of each individual node (1, 2, 3)
    string public aggregatedWeightsHash; // Variable to store IPFS hash of the aggregated model

    event CollaboratorAdded(address indexed collaborator);
    event CollaboratorRemoved(address indexed collaborator);
    event WeightsStored(uint indexed nodeId, string weightsHash);
    event AggregatedWeightsStored(string weightsHash); // Should run script | node1_receiver.py

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function.");
        _;
    }

    modifier onlyCollaborator() {
        require(collaborators[msg.sender], "Only a collaborator can call this function.");
        _;
    }

    function addCollaborator(address collaborator) public onlyOwner {
        collaborators[collaborator] = true;
        emit CollaboratorAdded(collaborator);
    }

    function removeCollaborator(address collaborator) public onlyOwner {
        collaborators[collaborator] = false;
        emit CollaboratorRemoved(collaborator);
    }

    function storeNodeWeights(uint nodeId, string memory weightsHash) public onlyCollaborator {
        nodeWeightsHashes[nodeId] = weightsHash;
        emit WeightsStored(nodeId, weightsHash);
    }

    function getNodeWeightsHash(uint nodeId) public view returns (string memory) {
        return nodeWeightsHashes[nodeId];
    }

    function storeAggregatedWeights(string memory weightsHash) public onlyOwner {
        aggregatedWeightsHash = weightsHash;
        emit AggregatedWeightsStored(weightsHash);
    }

    function getAggregatedWeightsHash() public view returns (string memory) {
        return aggregatedWeightsHash;
    }
}
