import 'package:flutter/material.dart';
class HeaderMFSim extends StatelessWidget {
  const HeaderMFSim({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 20),
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(0.25),
        border: const Border(
          bottom: BorderSide(color: Colors.cyanAccent, width: 1),
        ),
      ),
      child: const Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.memory_rounded, color: Colors.cyanAccent, size: 26),
          SizedBox(width: 10),
          Text(
            "MFSim Assistant",
            style: TextStyle(
              color: Colors.white,
              fontSize: 20,
              fontWeight: FontWeight.bold,
              letterSpacing: 1.5,
            ),
          ),
        ],
      ),
    );
  }
}