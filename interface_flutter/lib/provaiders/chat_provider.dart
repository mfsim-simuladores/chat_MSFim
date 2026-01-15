import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:mfsim_assistente/models/message.dart';

const apiUrl = "http://127.0.0.1:8000";

class ChatProvider extends ChangeNotifier {
  final List<Message> _messages = [];
  List<Message> get messages => List.unmodifiable(_messages);


  bool _typing = false;
  bool get isTyping => _typing;

  void _setTyping(bool v) {
    _typing = v;
    notifyListeners();
  }

  void _addUser(String text) {
    _messages.add(Message.user(text));
    notifyListeners();
  }

  void _addBot(String text, {String type = "log"}) {
    _messages.add(Message.system(text));
    notifyListeners();
  }

  Future<void> sendMessage(String text) async {
    if (text.trim().isEmpty) return;

    _addUser(text);
    _setTyping(true);

    await _startSSE(text);

    _setTyping(false);
  }


  Future<void> _startSSE(String text) async {
    final client = http.Client();
    final uri = Uri.parse("$apiUrl/sse/run?text=${Uri.encodeComponent(text)}");

    try {
      final req = http.Request("GET", uri);
      final resp = await client.send(req);

      final stream = resp.stream
          .transform(utf8.decoder)
          .transform(const LineSplitter());

      await for (final line in stream) {
        if (!line.startsWith("data:")) continue;

        final raw = line.substring(5).trim();
        if (raw.isEmpty) continue;

        final event = jsonDecode(raw);

        final message = event["message"];
        if (message != null && message.toString().isNotEmpty) {
          _addBot(message, type: event["type"] ?? "log");
        }
      }
    } catch (e) {
      _addBot("Erro SSE: $e", type: "error");
    } finally {
      client.close();
    }
  }

}
