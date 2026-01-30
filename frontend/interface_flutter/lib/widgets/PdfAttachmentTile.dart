import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import 'package:open_filex/open_filex.dart';

class PdfAttachmentTile extends StatelessWidget {
  final String title;
  final String text;
  final String url;

  const PdfAttachmentTile({
    super.key,
    required this.title,
    required this.text,
    required this.url,
  });

  Future<void> _downloadAndOpen(BuildContext context) async {
    try {
      final uri = Uri.parse(
        url.startsWith('http')
            ? url
            : 'http://127.0.0.1:8000$url',
      );

      final response = await http.get(uri);
      if (response.statusCode != 200) {
        throw Exception("Erro ao baixar PDF");
      }

      final dir = await getApplicationDocumentsDirectory();
      final file = File("${dir.path}/${uri.pathSegments.last}");
      await file.writeAsBytes(response.bodyBytes);

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: const Text("📄 Manual baixado com sucesso"),
          action: SnackBarAction(
            label: "Abrir",
            onPressed: () {
              OpenFilex.open(file.path);
            },
          ),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("❌ Falha ao baixar o manual"),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () => _downloadAndOpen(context),
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 6),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: const Color(0xFF1B263B),
          borderRadius: BorderRadius.circular(10),
        ),
        child: Row(
          children: [
            const Icon(Icons.picture_as_pdf, color: Colors.redAccent),
            const SizedBox(width: 10),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title,
                      style: const TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.w600)),
                  Text(text,
                      style: const TextStyle(
                          color: Colors.white54,
                          fontSize: 12)),
                ],
              ),
            ),
            const Icon(Icons.download_rounded, color: Colors.white54),
          ],
        ),
      ),
    );
  }
}
