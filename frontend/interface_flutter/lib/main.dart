import 'package:flutter/material.dart';
import 'package:mfsim_assistente/pages/chat_page.dart';
import 'package:mfsim_assistente/provaiders/chat_provider.dart';
import 'package:provider/provider.dart';
import 'theme.dart';
import 'package:media_kit/media_kit.dart';

void main() {
  MediaKit.ensureInitialized();
  runApp(const MFSimApp());
}

class MFSimApp extends StatelessWidget {
  const MFSimApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => ChatProvider()),
      ],
      child: MaterialApp(
        debugShowCheckedModeBanner: false,
        theme: buildMFSimTheme(),
        home: const ChatPage(),
      ),
    );
  }
}
