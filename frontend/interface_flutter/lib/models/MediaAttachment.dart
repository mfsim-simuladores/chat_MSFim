class MediaAttachment {
  final String type; // video | image
  final String label;
  final String url;

  MediaAttachment({
    required this.type,
    required this.label,
    required this.url,
  });

  factory MediaAttachment.fromJson(Map<String, dynamic> json) {
    return MediaAttachment(
      type: json['type'],
      label: json['label'] ?? '',
      url: json['url'],
    );
  }
}
