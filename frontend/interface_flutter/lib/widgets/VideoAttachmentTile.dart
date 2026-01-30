import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';

class VideoAttachmentTile extends StatefulWidget {
  final String title;
  final String url;

  const VideoAttachmentTile({
    super.key,
    required this.title,
    required this.url,
  });

  @override
  State<VideoAttachmentTile> createState() => _VideoAttachmentTileState();
}

class _VideoAttachmentTileState extends State<VideoAttachmentTile> {
  late final Player _player;
  late final VideoController _controller;

  @override
  void initState() {
    super.initState();

    _player = Player();
    _controller = VideoController(_player);

    _player.open(Media(widget.url));
  }

  @override
  void dispose() {
    _player.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Center(
        child: Container(
          width: 420, // 🔹 CONTROLE DO TAMANHO AQUI
          decoration: BoxDecoration(
            color: const Color(0xFF0D1B2A),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: const Color(0xFF1A2536)),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // 🎬 VÍDEO
              AspectRatio(
                aspectRatio: 16 / 9,
                child: Video(
                  controller: _controller,
                  controls: AdaptiveVideoControls,
                ),
              ),

              // 🏷️ LABEL
              if (widget.title.isNotEmpty)
                Padding(
                  padding: const EdgeInsets.all(8),
                  child: Text(
                    widget.title,
                    style: const TextStyle(
                      color: Colors.white70,
                      fontSize: 13,
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
