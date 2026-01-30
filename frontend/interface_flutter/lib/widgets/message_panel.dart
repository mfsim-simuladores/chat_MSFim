import 'package:flutter/material.dart';

class MessagePanel extends StatelessWidget {
  final String text;
  final bool isUser;
  final bool showHeader;

  final String? type;
  final String? title;

  const MessagePanel({
    super.key,
    required this.text,
    required this.isUser,
    this.showHeader = true,
    this.type,
    this.title,
  });


  Color _bubbleColor() {
    if (isUser) return const Color(0xFF1A2332);
    switch (type) {
      case "action":
        return const Color(0xFF0D47A1);
      case "log":
        return const Color(0xFF1B2635); 
      case "warning":
        return const Color(0xFF8E6B00); 
      case "finished":
        return const Color(0xFF1B5E20); 
      default:
        return const Color(0xFF112030); 
    }
  }

  IconData _iconForType() {
    switch (type) {
      case "action":
        return Icons.play_arrow_rounded;
      case "log":
        return Icons.notes_rounded;
      case "warning":
        return Icons.warning_amber_rounded;
      case "error":
        return Icons.error_rounded;
      case "finished":
        return Icons.check_circle_rounded;
      default:
        return Icons.smart_toy_rounded; 
    }
  }

  String _labelForType() {
    switch (type) {
      case "action":
        return "Ação";
      case "log":
        return "Log";
      case "warning":
        return "Aviso";
      case "error":
        return "Erro";
      case "finished":
        return "Concluído";
      default:
        return "Assistente";
    }
  }


  @override
  Widget build(BuildContext context) {
    final bubbleColor = _bubbleColor();

    return Padding(
      padding: EdgeInsets.only(
        left: isUser ? 60 : 10,
        right: isUser ? 10 : 60,
        top: showHeader ? 10 : 4,
      ),
      child: Column(
        crossAxisAlignment:
            isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
        children: [
          if (showHeader)
            Padding(
              padding: const EdgeInsets.only(bottom: 4),
              child: Row(
                mainAxisAlignment: isUser
                    ? MainAxisAlignment.end
                    : MainAxisAlignment.start,
                children: [
                  if (!isUser)
                    Icon(_iconForType(),
                        size: 16, color: Colors.white.withOpacity(0.7)),
                  const SizedBox(width: 6),
                  Text(
                    isUser ? "Você" : _labelForType(),
                    style: TextStyle(
                      color: Colors.white.withOpacity(0.65),
                      fontSize: 12,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ],
              ),
            ),

          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: bubbleColor,
              borderRadius: BorderRadius.circular(14),
              border: Border.all(
                color: Colors.white.withOpacity(0.06),
                width: 1,
              ),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (title != null && title!.isNotEmpty)
                  Text(
                    title!,
                    style: const TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.w700,
                      fontSize: 15,
                    ),
                  ),
                if (title != null && title!.isNotEmpty)
                  const SizedBox(height: 6),

                Text(
                  text,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 14,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
