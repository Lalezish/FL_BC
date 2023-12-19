module.exports = {
    networks: {
        development: {
            host: "127.0.0.1",     // Localhost (default: none)
            port: 7545,            // Standard Ethereum port (default: none)
            network_id: "*",       // Any network (default: none)
            from: "0x47B0f144C67E8db884e7dcE01B0253F01D6bA714",
        },
    },
    compilers: {
        solc: {
            version: "0.8.0",    // Fetch exact version
        }
    },

    // Other configurations...
};
