import 'package:flutter/material.dart';
import 'package:mfsim_assistente/models/MediaAttachment.dart';

class ImageAttachmentTile extends StatelessWidget {
  final MediaAttachment media;

  const ImageAttachmentTile({
    super.key,
    required this.media,
  });

  @override
  Widget build(BuildContext context) {
    final url = media.url.startsWith('http')
        ? media.url
        : 'http://127.0.0.1:8000${media.url}';

    return Container(
      margin: const EdgeInsets.symmetric(vertical: 6),
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: const Color(0xFF1B263B),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // LABEL
          if (media.label.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(bottom: 6),
              child: Text(
                media.label,
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),

          // IMAGE
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: Image.network(
              url,
              fit: BoxFit.contain,
              loadingBuilder: (context, child, progress) {
                if (progress == null) return child;
                return const SizedBox(
                  height: 180,
                  child: Center(
                    child: CircularProgressIndicator(
                      color: Colors.white,
                    ),
                  ),
                );
              },
              errorBuilder: (_, __, ___) => const SizedBox(
                height: 180,
                child: Center(
                  child: Icon(
                    Icons.broken_image,
                    color: Colors.white54,
                    size: 40,
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
