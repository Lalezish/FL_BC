const NeuralNetworkWeights = artifacts.require("NeuralNetworkWeights");

module.exports = function (deployer) {
  deployer.deploy(NeuralNetworkWeights);
};