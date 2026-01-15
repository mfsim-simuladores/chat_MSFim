import 'package:flutter/material.dart';
import 'package:mfsim_assistente/models/message.dart';
import 'package:mfsim_assistente/widgets/ActionBlock.dart';
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
      itemBuilder: (context, index){
        final msg = messages[index];

        switch(msg.kind){
          case MessageKind.user:
            return UserMessageBubble(text: msg.text!);

          case MessageKind.system:
           return SystemMessageBubble(text: msg.text!);

          case MessageKind.actionBlock:
            return ActionBlock(title: msg.title!, items: msg.items!, footer: msg.footer,);
        }
      },
      
    );
  }
}
