import 'package:flutter/material.dart';

ThemeData buildMFSimTheme() {
  return ThemeData(
    brightness: Brightness.dark,

    scaffoldBackgroundColor: const Color(0xFF0B1220), 

    textTheme: const TextTheme(
      bodyMedium: TextStyle(
        color: Color(0xFFE8E8F2), 
        fontSize: 15,
        height: 1.46,
      ),
    ),

    appBarTheme: const AppBarTheme(
      backgroundColor: Color(0xFF0D1B2A),
      elevation: 0,
      iconTheme: IconThemeData(color: Color(0xFFE8E8F2)),
      titleTextStyle: TextStyle(
        color: Color(0xFFE8E8F2),
        fontSize: 17,
        fontWeight: FontWeight.w600,
      ),
    ),

    dividerColor: const Color(0xFF1A2536),

    inputDecorationTheme: const InputDecorationTheme(
      border: InputBorder.none,
      hintStyle: TextStyle(
        color: Colors.white38,
        fontSize: 15,
      ),
    ),

    iconTheme: const IconThemeData(
      color: Color(0xFFE8E8F2),
    ),
  );
}
