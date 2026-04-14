import 'dart:async';
import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:web_socket_channel/io.dart';

import 'core/app_config.dart';
import 'core/card_asset_path.dart';

void main() {
  runApp(const JudgementApp());
}

class JudgementApp extends StatelessWidget {
  const JudgementApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Judgement',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF115E59)),
        useMaterial3: true,
      ),
      home: const GameClientScreen(),
    );
  }
}

enum UiPhase { home, lobby, game, gameOver }

class GameClientScreen extends StatefulWidget {
  const GameClientScreen({super.key});

  @override
  State<GameClientScreen> createState() => _GameClientScreenState();
}

class _GameClientScreenState extends State<GameClientScreen> {
  final Dio _dio = Dio();
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _roomCodeController = TextEditingController();

  IOWebSocketChannel? _channel;
  StreamSubscription<dynamic>? _socketSubscription;

  UiPhase _phase = UiPhase.home;
  bool _busy = false;
  bool _roundEnded = false;
  String _status = 'Set username and create or join a room.';

  String _roomCode = '';
  String _host = '';
  String? _winner;
  List<String> _players = [];
  Map<String, int> _bids = {};
  Map<String, int> _roundScores = {};
  Map<String, List<int>> _cumulativeScores = {};
  List<Map<String, dynamic>> _hand = [];
  List<Map<String, dynamic>> _trickSoFar = [];
  String? _currentBidder;
  String? _currentPlayer;
  String? _trumpSuit;
  int _roundNum = 0;
  int _totalCards = 0;
  int? _illegalBid;

  String get _username => _usernameController.text.trim();
  bool get _isHost => _username.isNotEmpty && _username == _host;

  @override
  void initState() {
    super.initState();
    _loadUsername();
  }

  @override
  void dispose() {
    _socketSubscription?.cancel();
    _channel?.sink.close();
    _usernameController.dispose();
    _roomCodeController.dispose();
    super.dispose();
  }

  Future<void> _loadUsername() async {
    final prefs = await SharedPreferences.getInstance();
    final stored = prefs.getString('player_username');
    if (stored != null && stored.isNotEmpty) {
      setState(() {
        _usernameController.text = stored;
      });
    }
  }

  Future<void> _saveUsername() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('player_username', _username);
  }

  Future<void> _createRoom() async {
    if (!_validateUsername()) {
      return;
    }

    setState(() {
      _busy = true;
      _status = 'Creating room...';
    });

    try {
      final response = await _dio.post(AppConfig.roomCreateUrl());
      final roomCode = (response.data['room_code'] as String).toUpperCase();
      await _saveUsername();
      await _connectToRoom(roomCode);
    } catch (_) {
      setState(() {
        _status = 'Room creation failed. Check backend URL and network.';
      });
    } finally {
      setState(() {
        _busy = false;
      });
    }
  }

  Future<void> _joinRoom() async {
    if (!_validateUsername()) {
      return;
    }
    final code = _roomCodeController.text.trim().toUpperCase();
    if (code.length != 6) {
      setState(() {
        _status = 'Room code must be 6 characters.';
      });
      return;
    }

    setState(() {
      _busy = true;
      _status = 'Checking room...';
    });

    try {
      final response = await _dio.get(AppConfig.roomExistsUrl(code));
      final exists = response.data['exists'] == true;
      if (!exists) {
        setState(() {
          _status = 'Room not found.';
        });
        return;
      }

      await _saveUsername();
      await _connectToRoom(code);
    } catch (_) {
      setState(() {
        _status = 'Join failed. Check backend URL and network.';
      });
    } finally {
      setState(() {
        _busy = false;
      });
    }
  }

  Future<void> _connectToRoom(String roomCode) async {
    await _socketSubscription?.cancel();
    await _channel?.sink.close();

    final wsUrl = AppConfig.roomWebSocketUrl(roomCode, _username);
    final channel = IOWebSocketChannel.connect(
      Uri.parse(wsUrl),
      pingInterval: const Duration(seconds: 15),
    );

    _channel = channel;
    _socketSubscription = channel.stream.listen(
      _handleServerEvent,
      onError: (_) {
        if (!mounted) {
          return;
        }
        setState(() {
          _status = 'Socket error. Check WS URL and backend.';
        });
      },
      onDone: () {
        if (!mounted) {
          return;
        }
        setState(() {
          _status = 'Disconnected from server.';
        });
      },
    );

    setState(() {
      _roomCode = roomCode;
      _phase = UiPhase.lobby;
      _status = 'Connected to room $roomCode';
      _winner = null;
      _roundEnded = false;
      _roundScores = {};
      _trickSoFar = [];
    });
  }

  bool _validateUsername() {
    final user = _username;
    if (user.isEmpty || user.length > 16) {
      setState(() {
        _status = 'Username is required (1-16 chars).';
      });
      return false;
    }
    return true;
  }

  void _handleServerEvent(dynamic payload) {
    final Map<String, dynamic> event = jsonDecode(payload as String) as Map<String, dynamic>;
    final type = event['type'] as String?;

    if (!mounted || type == null) {
      return;
    }

    setState(() {
      switch (type) {
        case 'server_room_state':
          _host = (event['host'] ?? '') as String;
          _players = _stringList(event['players']);
          _status = 'Lobby updated (${_players.length} players).';
          break;
        case 'server_deal_cards':
          _phase = UiPhase.game;
          _winner = null;
          _roundEnded = false;
          _roundNum = _toInt(event['round_num']);
          _totalCards = _toInt(event['total_cards']);
          _trumpSuit = event['trump_suit'] as String?;
          _hand = _cardList(event['hand']);
          _trickSoFar = [];
          _status = 'Round $_roundNum started. Trump: ${_trumpSuit ?? '-'}';
          break;
        case 'server_bid_request':
          _currentBidder = event['current_bidder'] as String?;
          _illegalBid = event['illegal_bid'] == null ? null : _toInt(event['illegal_bid']);
          _status = _currentBidder == _username
              ? 'Your turn to bid.'
              : 'Waiting for ${_currentBidder ?? 'player'} to bid.';
          break;
        case 'server_bid_update':
          _bids = _toIntMap(event['bids']);
          break;
        case 'server_turn_update':
          _currentPlayer = event['current_player'] as String?;
          _trickSoFar = _trickList(event['trick_so_far']);
          _status = _currentPlayer == _username
              ? 'Your turn to play.'
              : 'Waiting for ${_currentPlayer ?? 'player'} to play.';
          break;
        case 'server_trick_result':
          _status = 'Trick winner: ${event['winner']}';
          break;
        case 'server_round_end':
          _roundEnded = true;
          _roundScores = _toIntMap(event['scores']);
          _cumulativeScores = _scoreMatrix(event['cumulative_scores']);
          _status = 'Round ended. Host can start next round.';
          break;
        case 'server_game_over':
          _phase = UiPhase.gameOver;
          _winner = event['winner'] as String?;
          _cumulativeScores = _scoreMatrix(event['final_scores']);
          _status = 'Game over. Winner: ${_winner ?? '-'}';
          break;
        case 'server_player_left':
          final leftUser = event['username'] as String?;
          final newHost = event['new_host'] as String?;
          if (newHost != null && newHost.isNotEmpty) {
            _host = newHost;
          }
          _status = '${leftUser ?? 'A player'} disconnected.';
          break;
        case 'server_error':
          _status = '${event['code']}: ${event['message']}';
          break;
      }
    });
  }

  void _sendEvent(Map<String, dynamic> event) {
    _channel?.sink.add(jsonEncode(event));
  }

  void _startGame() {
    _sendEvent({'type': 'client_start_game', 'room_code': _roomCode});
  }

  void _placeBid(int bid) {
    _sendEvent({'type': 'client_place_bid', 'room_code': _roomCode, 'username': _username, 'bid': bid});
  }

  void _playCard(Map<String, dynamic> card) {
    _sendEvent({
      'type': 'client_play_card',
      'room_code': _roomCode,
      'username': _username,
      'card': card,
    });
    setState(() {
      _hand = _hand.where((item) => item.toString() != card.toString()).toList();
    });
  }

  void _nextRound() {
    _sendEvent({'type': 'client_next_round', 'room_code': _roomCode});
  }

  void _rematch() {
    _sendEvent({'type': 'client_rematch', 'room_code': _roomCode});
    setState(() {
      _phase = UiPhase.game;
      _winner = null;
    });
  }

  Future<void> _leaveRoom() async {
    await _socketSubscription?.cancel();
    await _channel?.sink.close();
    if (!mounted) {
      return;
    }
    setState(() {
      _phase = UiPhase.home;
      _roomCode = '';
      _host = '';
      _players = [];
      _bids = {};
      _roundScores = {};
      _cumulativeScores = {};
      _hand = [];
      _trickSoFar = [];
      _currentBidder = null;
      _currentPlayer = null;
      _trumpSuit = null;
      _roundNum = 0;
      _totalCards = 0;
      _illegalBid = null;
      _status = 'Disconnected.';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Judgement'),
        actions: [
          if (_phase != UiPhase.home)
            IconButton(
              onPressed: _leaveRoom,
              icon: const Icon(Icons.logout),
            ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: _buildPhase(),
      ),
    );
  }

  Widget _buildPhase() {
    switch (_phase) {
      case UiPhase.home:
        return _buildHome();
      case UiPhase.lobby:
        return _buildLobby();
      case UiPhase.game:
        return _buildGame();
      case UiPhase.gameOver:
        return _buildGameOver();
    }
  }

  Widget _buildHome() {
    return ListView(
      children: [
        TextField(
          controller: _usernameController,
          decoration: const InputDecoration(labelText: 'Username (1-16 chars)'),
          maxLength: 16,
        ),
        const SizedBox(height: 10),
        FilledButton(
          onPressed: _busy ? null : _createRoom,
          child: const Text('Create Room'),
        ),
        const SizedBox(height: 8),
        TextField(
          controller: _roomCodeController,
          decoration: const InputDecoration(labelText: 'Room code (6 chars)'),
          textCapitalization: TextCapitalization.characters,
          maxLength: 6,
        ),
        OutlinedButton(
          onPressed: _busy ? null : _joinRoom,
          child: const Text('Join Room'),
        ),
        const SizedBox(height: 16),
        SizedBox(height: 80, child: Image.asset(cardBackAsset(2))),
        const SizedBox(height: 8),
        Text('API: ${AppConfig.apiBaseUrl}'),
        Text('WS: ${AppConfig.wsBaseUrl}'),
        const SizedBox(height: 12),
        Text(_status),
      ],
    );
  }

  Widget _buildLobby() {
    return ListView(
      children: [
        Text('Room: $_roomCode', style: Theme.of(context).textTheme.headlineSmall),
        const SizedBox(height: 10),
        Text('Host: ${_host.isEmpty ? '-' : _host}'),
        Text('Players (${_players.length}): ${_players.join(', ')}'),
        const SizedBox(height: 12),
        if (_isHost)
          FilledButton(
            onPressed: _players.length >= 2 ? _startGame : null,
            child: const Text('Start Game'),
          )
        else
          const Text('Waiting for host to start...'),
        const SizedBox(height: 12),
        Text(_status),
      ],
    );
  }

  Widget _buildGame() {
    final isMyBidTurn = _currentBidder == _username;
    final isMyPlayTurn = _currentPlayer == _username;

    return ListView(
      children: [
        Text('Room: $_roomCode'),
        Text('Round: $_roundNum  |  Trump: ${_trumpSuit ?? '-'}'),
        Text('Current bidder: ${_currentBidder ?? '-'}'),
        Text('Current player: ${_currentPlayer ?? '-'}'),
        const SizedBox(height: 10),
        Text('Bids: ${_bids.isEmpty ? '-' : _bids.entries.map((e) => '${e.key}:${e.value}').join(', ')}'),
        const SizedBox(height: 8),
        Text(
          'Trick so far: ${_trickSoFar.isEmpty ? '-' : _trickSoFar.map((e) => '${e['username']}:${_cardLabel((e['card'] as Map<String, dynamic>))}').join(' | ')}',
        ),
        const SizedBox(height: 12),
        if (isMyBidTurn)
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: List<Widget>.generate(_totalCards + 1, (bid) {
              final isIllegal = _illegalBid != null && _illegalBid == bid;
              return ChoiceChip(
                label: Text('Bid $bid'),
                selected: false,
                onSelected: isIllegal ? null : (_) => _placeBid(bid),
              );
            }),
          )
        else
          Text(isMyPlayTurn ? 'Play a card.' : _status),
        const SizedBox(height: 12),
        Text('Your hand (${_hand.length}):'),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: _hand.map((card) {
            return ActionChip(
              onPressed: isMyPlayTurn ? () => _playCard(card) : null,
              label: Text(_cardLabel(card)),
            );
          }).toList(),
        ),
        const SizedBox(height: 14),
        if (_roundEnded && _isHost)
          FilledButton(onPressed: _nextRound, child: const Text('Next Round')),
        if (_roundScores.isNotEmpty) ...[
          const SizedBox(height: 10),
          Text(
            'Round scores: ${_roundScores.entries.map((e) => '${e.key}:${e.value}').join(', ')}',
          ),
        ],
      ],
    );
  }

  Widget _buildGameOver() {
    return ListView(
      children: [
        Text('Game Over', style: Theme.of(context).textTheme.headlineMedium),
        const SizedBox(height: 10),
        Text('Winner: ${_winner ?? '-'}'),
        const SizedBox(height: 8),
        Text('Final matrix:'),
        ..._cumulativeScores.entries.map(
          (entry) => Text('${entry.key}: ${entry.value.join(', ')} (total ${entry.value.fold<int>(0, (a, b) => a + b)})'),
        ),
        const SizedBox(height: 16),
        if (_isHost) FilledButton(onPressed: _rematch, child: const Text('Play Again')), 
        const SizedBox(height: 8),
        OutlinedButton(onPressed: _leaveRoom, child: const Text('Exit to Home')),
      ],
    );
  }

  List<String> _stringList(dynamic value) {
    if (value is! List) {
      return [];
    }
    return value.map((item) => item.toString()).toList();
  }

  int _toInt(dynamic value) {
    if (value is int) {
      return value;
    }
    return int.tryParse(value.toString()) ?? 0;
  }

  Map<String, int> _toIntMap(dynamic value) {
    if (value is! Map) {
      return {};
    }
    return value.map((key, val) => MapEntry(key.toString(), _toInt(val)));
  }

  Map<String, List<int>> _scoreMatrix(dynamic value) {
    if (value is! Map) {
      return {};
    }
    final result = <String, List<int>>{};
    value.forEach((key, val) {
      if (val is List) {
        result[key.toString()] = val.map((entry) => _toInt(entry)).toList();
      }
    });
    return result;
  }

  List<Map<String, dynamic>> _cardList(dynamic value) {
    if (value is! List) {
      return [];
    }
    return value
        .whereType<Map>()
        .map((item) => item.map((key, val) => MapEntry(key.toString(), val)))
        .toList();
  }

  List<Map<String, dynamic>> _trickList(dynamic value) {
    if (value is! List) {
      return [];
    }
    return value
        .whereType<Map>()
        .map((item) => item.map((key, val) => MapEntry(key.toString(), val)))
        .toList();
  }

  String _cardLabel(Map<String, dynamic> card) {
    final suit = (card['suit'] ?? '').toString();
    final value = (card['value'] ?? '').toString();
    return '$value${_suitSymbol(suit)}';
  }

  String _suitSymbol(String suit) {
    switch (suit) {
      case 'spades':
        return '♠';
      case 'hearts':
        return '♥';
      case 'diamonds':
        return '♦';
      case 'clubs':
        return '♣';
      default:
        return '?';
    }
  }
}