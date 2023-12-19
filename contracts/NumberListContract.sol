// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract NumberListContract {
    address public owner;
    uint[] private numbers;
    mapping(address => bool) public collaborators;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can perform this action.");
        _;
    }

    modifier onlyCollaborator() {
        require(collaborators[msg.sender], "Only a collaborator can perform this action.");
        _;
    }

    function addCollaborator(address collaborator) public onlyOwner {
        collaborators[collaborator] = true;
    }

    function removeCollaborator(address collaborator) public onlyOwner {
        collaborators[collaborator] = false;
    }

    function addNumber(uint number) public onlyCollaborator {
        numbers.push(number);
    }

    function deleteNumber(uint index) public onlyOwner {
        require(index < numbers.length, "Index out of bounds");
        numbers[index] = numbers[numbers.length - 1];
        numbers.pop();
    }

    function getNumbers() public view returns (uint[] memory) {
        return numbers;
    }
}
