export const AppConstants = {
  // Use your hosted URL here (e.g., 'https://judgement-production.up.railway.app')
  // If empty, the build script will prompt for it.
  productionUrl: '', 
  
  apiBaseUrl: 'http://10.10.214.178:8000',
  wsBaseUrl: 'ws://10.10.214.178:8000',

  storageKeys: {
    username: 'player_username',
  },

  limits: {
    roomCodeLength: 6,
    maxUsernameLength: 16,
  },
};
