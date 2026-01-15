import 'dart:convert';
import 'dart:async';
import 'package:http/http.dart' as http;
import '../models/chat_event.dart';

class ApiService {
  final String baseUrl;

  ApiService({this.baseUrl = "http://127.0.0.1:8000"});

  Stream<ChatEvent> streamAction(String actionName) async* {
    final client = http.Client();
    final uri = Uri.parse("$baseUrl/sse/run?text=$actionName");

    final req = http.Request("GET", uri);
    final resp = await client.send(req);

    final stream = resp.stream
        .transform(utf8.decoder)
        .transform(const LineSplitter());

    await for (final line in stream) {
      if (!line.startsWith("data:")) continue;

      final raw = line.substring(5).trim();
      if (raw == "[END]") break;

      try {
        yield ChatEvent.fromJson(jsonDecode(raw));
      } catch (_) {
        continue;
      }
    }
    client.close();
  }
}
