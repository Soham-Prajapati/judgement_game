import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() {
  runApp(const ProviderScope(child: JudgementApp()));
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
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Judgement')),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                'Multiplayer Kachuful',
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.headlineSmall,
              ),
              const SizedBox(height: 24),
              FilledButton(
                onPressed: null,
                child: const Text('Create Room (next step)'),
              ),
              const SizedBox(height: 12),
              OutlinedButton(
                onPressed: null,
                child: const Text('Join Room (next step)'),
              ),
              const SizedBox(height: 24),
              Text(
                'Backend WS protocol is implemented. UI selection remains deferred by plan.',
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.bodySmall,
              ),
            ],
          ),
        ),
      ),
    );
  }
}