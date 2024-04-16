import { Keypair } from 'stellar-sdk';
class SimplifiedEnvConfig {
    static getUserKeypair(config) {
        return Keypair.fromSecret(config.userSecretKey);
    }
}
// This function now correctly expects a user's secret key along with the network as parameters
export const api_config = (network, userSecretKey) => {
    const config = { network, userSecretKey };
    return SimplifiedEnvConfig.getUserKeypair(config);
};
