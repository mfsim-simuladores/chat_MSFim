import 'package:flutter/material.dart';
import 'package:mfsim_assistente/models/message.dart';
import 'package:mfsim_assistente/pages/chat_page.dart';
import 'package:mfsim_assistente/widgets/ActionBlock.dart';
import 'package:mfsim_assistente/widgets/PdfAttachmentTile.dart';
import 'package:mfsim_assistente/widgets/VideoAttachmentTile.dart';
import 'package:mfsim_assistente/widgets/ImageAttachmentTile.dart';
import 'package:mfsim_assistente/widgets/UserMessageBubble.dart';
import 'package:mfsim_assistente/widgets/systemMessageBubble.dart';

class TimelinePanel extends StatelessWidget {
  final List<Message> messages;
  final ScrollController controller;

  const TimelinePanel({
    super.key,
    required this.messages,
    required this.controller,
  });

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      controller: controller,
      padding: const EdgeInsets.only(top: 12, bottom: 80),
      itemCount: messages.length,
      itemBuilder: (context, index) {
        final msg = messages[index];

        switch (msg.kind) {
          case MessageKind.user:
            return UserMessageBubble(text: msg.text!);

          case MessageKind.system:
            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // TEXTO
                if ((msg.text ?? "").isNotEmpty)
                  SystemMessageBubble(text: msg.text!),

                // ==========================
                // 📎 PDF ATTACHMENTS
                // ==========================
                if (msg.attachments != null) ...[
                  const SizedBox(height: 6),
                  for (final a in msg.attachments!)
                    if (a.type == 'pdf')
                      PdfAttachmentTile(
                        title: a.label,
                        text: 'Abrir PDF',
                        url: a.url,
                      ),
                ],

                // ==========================
                // 🎥 / 🖼 MEDIA (VIDEO / IMAGE)
                // ==========================
                if (msg.media != null) ...[
                  const SizedBox(height: 8),

                  if (msg.media != null && msg.media!.type == 'video')
                    VideoAttachmentTile(
                      title: msg.media!.label,
                      url: "$apiUrl${msg.media!.url}",
                    ),


                  if (msg.media!.type == 'image')
                    ImageAttachmentTile(
                      media: msg.media!,
                    ),
                ],
              ],
            );

          case MessageKind.actionBlock:
            return ActionBlock(
              title: msg.title!,
              items: msg.items ?? const [],
              footer: msg.footer,
            );
        }
      },
    );
  }
}
