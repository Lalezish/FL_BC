module.exports = {
    networks: {
        development: {
            host: "127.0.0.1",
            port: 7545,
            network_id: "*",
            from: "0xbA248d267d591a886800503E8517778165148e8a",
        },
    },
    compilers: {
        solc: {
            version: "0.8.0",
        }
    },
};
