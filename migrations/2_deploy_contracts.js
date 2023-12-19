const NumberListContract = artifacts.require("NumberListContract");

module.exports = function (deployer) {
    deployer.deploy(NumberListContract);
};
