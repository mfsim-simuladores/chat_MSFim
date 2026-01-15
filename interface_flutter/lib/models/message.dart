enum MessageKind{
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

  Message.system(this.text)
    : kind = MessageKind.system,
      title = null,
      items = null,
      footer = null;

  Message.user(this.text)
    : kind = MessageKind.user,
    title = null,
    items = null,
    footer = null;

  Message.actionBlock({
    required this.title,
    required this.items,
    this.footer,
  })  : kind = MessageKind.actionBlock,
        text = null;

}
