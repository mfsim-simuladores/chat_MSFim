import 'package:mfsim_assistente/models/MediaAttachment.dart';
import 'package:mfsim_assistente/models/attachment.dart';

enum MessageKind {
  user,
  system,
  actionBlock,
}

class Message {
  final MessageKind kind;
  final String? text;
  final String? title;
  final List<String>? items;
  final String? footer;
  final List<Attachment>? attachments;
  final MediaAttachment? media; 

  Message._({
    required this.kind,
    this.text,
    this.title,
    this.items,
    this.footer,
    this.attachments,
    this.media,
  });

  factory Message.user(String text) {
    return Message._(
      kind: MessageKind.user,
      text: text,
    );
  }

  factory Message.system(
    String text, {
    List<Attachment>? attachments,
    MediaAttachment? media,
  }) {
    return Message._(
      kind: MessageKind.system,
      text: text,
      attachments: attachments,
      media: media, 
    );
  }

  factory Message.actionBlock({
    required String title,
    required List<String> items,
    String? footer,
    List<Attachment>? attachments,
  }) {
    return Message._(
      kind: MessageKind.actionBlock,
      title: title,
      items: items,
      footer: footer,
      attachments: attachments,
    );
  }
}
