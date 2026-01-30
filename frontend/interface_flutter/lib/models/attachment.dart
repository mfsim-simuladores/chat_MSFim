class Attachment {
  final String type;
  final String label;
  final String url;

  Attachment({
    required this.type,
    required this.label,
    required this.url,
  });

  factory Attachment.fromJson(Map<String, dynamic> json) {
    return Attachment(
      type: json['type'],
      label: json['label'],
      url: json['url'],
    );
  }
}
