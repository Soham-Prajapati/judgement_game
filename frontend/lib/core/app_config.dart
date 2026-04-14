class AppConfig {
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000',
  );

  static const String wsBaseUrl = String.fromEnvironment(
    'WS_BASE_URL',
    defaultValue: 'ws://10.0.2.2:8000',
  );

  static String roomCreateUrl() => '$apiBaseUrl/room/create';

  static String roomExistsUrl(String roomCode) =>
      '$apiBaseUrl/room/${roomCode.toUpperCase()}/exists';

  static String roomWebSocketUrl(String roomCode, String username) =>
      '$wsBaseUrl/ws/${roomCode.toUpperCase()}/$username';
}