export const AppConstants = {
  // Use your hosted URL here (e.g., 'https://judgement-production.up.railway.app')
  // If empty, the build script will prompt for it.
  productionUrl: '', 
  
  apiBaseUrl: 'judgementgame-production.up.railway.app',
  wsBaseUrl: 'ws://judgementgame-production.up.railway.app',

  storageKeys: {
    username: 'player_username',
  },

  limits: {
    roomCodeLength: 6,
    maxUsernameLength: 16,
  },
};
