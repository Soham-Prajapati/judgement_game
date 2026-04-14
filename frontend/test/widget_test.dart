import 'package:flutter_test/flutter_test.dart';
import 'package:judgement_client/main.dart';

void main() {
  testWidgets('Home screen renders core labels', (WidgetTester tester) async {
    await tester.pumpWidget(const JudgementApp());

    expect(find.text('Judgement'), findsOneWidget);
    expect(find.text('Create Room'), findsOneWidget);
    expect(find.text('Join Room'), findsOneWidget);
    expect(find.textContaining('API:'), findsOneWidget);
    expect(find.textContaining('WS:'), findsOneWidget);
  });
}
