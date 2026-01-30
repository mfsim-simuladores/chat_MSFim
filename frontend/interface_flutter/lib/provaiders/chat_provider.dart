import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'package:mfsim_assistente/models/message.dart';
import 'package:mfsim_assistente/models/attachment.dart';

const apiUrl = "http://127.0.0.1:8000";

class ChatProvider extends ChangeNotifier {
  ChatProvider() {
    print("🚨 CHAT PROVIDER INICIALIZADO 🚨");
  }

  final List<Message> _messages = [];
  List<Message> get messages => List.unmodifiable(_messages);

  bool _typing = false;
  bool get isTyping => _typing;

  void _setTyping(bool value) {
    _typing = value;
    notifyListeners();
  }

  void _add(Message msg) {
    _messages.add(msg);
    notifyListeners();
  }

  Future<void> sendMessage(String text) async {
    print("🟢 sendMessage CHAMADO com: $text");

    _add(Message.user(text));
    _startSSE(text);
  }

  Future<void> _startSSE(String text) async {
    final client = http.Client();
    final uri =
        Uri.parse("$apiUrl/sse/run?text=${Uri.encodeComponent(text)}");

    try {
      final req = http.Request("GET", uri);
      final resp = await client.send(req);

      final stream = resp.stream
          .transform(utf8.decoder)
          .transform(const LineSplitter());

      await for (final line in stream) {
        if (!line.startsWith("data:")) continue;

        final raw = line.substring(5).trim();
        if (raw.isEmpty || raw == "[END]") continue;

        final Map<String, dynamic> event = jsonDecode(raw);

        print("📥 EVENTO SSE:");
        print(event);

        final String message =
            (event["message"] ?? "").toString().trim();

        List<Attachment>? attachments;

        if (event["attachments"] != null &&
            event["attachments"] is List &&
            (event["attachments"] as List).isNotEmpty) {

          print("📎 ATTACHMENTS DETECTADOS");

          attachments = (event["attachments"] as List)
              .map((e) => Attachment.fromJson(e))
              .toList();
        }

        if (message.isNotEmpty || attachments != null) {
          _add(
            Message.system(
              message,
              attachments: attachments,
            ),
          );
        }
      }
    } catch (e) {
      _add(
        Message.system("❌ Erro de comunicação com o backend."),
      );
    } finally {
      client.close();
    }
  }
}
