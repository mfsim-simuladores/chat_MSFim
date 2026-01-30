import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

class ActionBlock extends StatelessWidget {
  final String title;
  final List<String> items;
  final String? footer;

  const ActionBlock({
    super.key,
    required this.title,
    required this.items,
    this.footer,
  });

  Future<void> _openLink(BuildContext context) async {
    if (footer == null) return;

    final uri = Uri.tryParse(footer!);
    if (uri == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Link inválido")),
      );
      return;
    }

    if (!await launchUrl(
      uri,
      mode: LaunchMode.externalApplication,
    )) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Não foi possível abrir o arquivo")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: const Color(0xFF0D1B2A),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: const Color(0xFF1A2536)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // 🔹 TÍTULO
          Text(
            title,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 15,
              fontWeight: FontWeight.w600,
            ),
          ),

          const SizedBox(height: 8),

          // 🔹 ITENS
          for (final item in items)
            Padding(
              padding: const EdgeInsets.only(bottom: 4),
              child: Text(
                "• $item",
                style: const TextStyle(
                  color: Colors.white70,
                  fontSize: 14,
                ),
              ),
            ),

          // 🔹 FOOTER / LINK PDF
          if (footer != null) ...[
            const SizedBox(height: 10),
            GestureDetector(
              onTap: () => _openLink(context),
              child: Row(
                children: const [
                  Icon(Icons.picture_as_pdf,
                      color: Colors.redAccent, size: 18),
                  SizedBox(width: 6),
                  Text(
                    "Abrir manual em PDF",
                    style: TextStyle(
                      color: Colors.lightBlueAccent,
                      decoration: TextDecoration.underline,
                      fontSize: 13,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }
}
