import 'dart:convert';
class ChatEvent {
  final String type;   
  final String? severity;
  final String? group;      
  final String? title;
  final String message;
  final DateTime timestamp;

  ChatEvent({
    required this.type,
    required this.message,
    this.title,
    this.severity,
    this.group,
    DateTime? timestamp,
  }) : timestamp = timestamp ?? DateTime.now();

  factory ChatEvent.fromJson(dynamic data) {
    if (data is String) data = jsonDecode(data);

    return ChatEvent(
      type: data["type"] ?? "log",
      severity: data["severity"],
      group: data["group"],
      title: data["title"],
      message: data["message"] ?? "",
      timestamp: DateTime.tryParse(data["timestamp"] ?? "") ?? DateTime.now(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "type": type,
      "title": title,
      "message": message,
      "timestamp": timestamp.toIso8601String(),
    };
  }
}
