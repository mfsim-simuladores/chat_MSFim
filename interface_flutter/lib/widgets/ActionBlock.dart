import 'package:flutter/material.dart';

class ActionBlock extends StatelessWidget{
  final String title;
  final List<String> items;
  final String? footer;
  final Color accerntColor;
  final IconData icon;

  const ActionBlock({
    super.key,
    required this.title,
    required this.items,
    this.footer,
    this.accerntColor = const Color(0xFF8E6B00),
    this.icon = Icons.warning_amber_rounded,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: const Color(0xFF8E6B00),
          borderRadius: BorderRadius.circular(14),
          border: Border.all(
            color: accerntColor.withOpacity(0.5),
            width: 1,
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: accerntColor, size: 18),
                const SizedBox(width: 8),
                Text(
                  title,
                  style: TextStyle(

                    color: accerntColor,
                    fontSize: 14,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),

            ...items.map(
              (item) => Padding(
                padding: const EdgeInsets.only(bottom: 6),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      "• ",
                      style: TextStyle(color: Colors.white70),
                    ),
                    Expanded(child: Text(
                      item,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 14,
                      ),
                    ),
                    ),
                  ],
                ), 
              ),
            ),
            if (footer != null) ...[
              const Divider(height: 20, color: Colors.white24),
              Text(
                footer!,
                style: const TextStyle(
                  color: Colors.white70,
                  fontSize: 13,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}