import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http; 
import 'package:mfsim_assistente/models/attachment.dart';
import 'package:mfsim_assistente/models/MediaAttachment.dart';
import 'package:mfsim_assistente/models/message.dart';
import 'package:mfsim_assistente/widgets/timeline_panel.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:path_provider/path_provider.dart';
import 'package:uuid/uuid.dart';

const apiUrl = "http://127.0.0.1:8000";

class ChatPage extends StatefulWidget {
  const ChatPage({super.key});

  @override
  State<ChatPage> createState() => _ChatPageState();
}

// STATE

class _ChatPageState extends State<ChatPage> {
  final TextEditingController _controller = TextEditingController();

  final uuid = const Uuid();
  List<Map<String, dynamic>> _conversas = [];
  List<Message> _messages = [];
  String? _conversaAtualId;

  bool _showHomeCards = true;

  late List<Widget> _cards;
  late List<Widget> _loopedCards;

  final int repeticao = 12;
  PageController? _pageController;
  final ScrollController _scrollController = ScrollController();

  bool _isTyping = false;

  // INIT

  @override
  void initState() {
    super.initState();
    _carregarConversas();

    _cards = [
      _buildFeatureCard(
        title: "Instalação GFC700",
        description: "Guia interativo MFSim.",
        icon: Icons.memory_rounded,
        message: "iniciar instalação gfc700",
      ),
      _buildFeatureCard(
        title: "Abrir X-Plane",
        description: "Start automático + verificação.",
        icon: Icons.flight_takeoff_rounded,
        message: "abrir xplane",
      ),
      _buildFeatureCard(
        title: "Instalação G1000",
        description: "Guia interativo Mfsim.",
        icon: Icons.extension_rounded,
        message: "instalação g1000",
      ),
      _buildFeatureCard(
        title: "Diagnóstico Motor",
        description: "Executa testes automáticos.",
        icon: Icons.engineering_rounded,
        message: "diagnosticar motor",
      ),
      _buildFeatureCard(
        title: "Pré-Voo",
        description: "Checklist MFSim completo.",
        icon: Icons.check_circle_outline_rounded,
        message: "preparar voo",
      ),
    ];

    _loopedCards = List.generate(repeticao, (_) => _cards).expand((x) => x).toList();

    _pageController = PageController(
      viewportFraction: 1.0,
      initialPage: _cards.length * (repeticao ~/ 2),
    );

    _pageController!.addListener(_handleScroll);

    WidgetsBinding.instance.addPostFrameCallback((_) {
      final w = MediaQuery.of(context).size.width;
      final vp = _viewportFraction(w);
      final oldPage = _pageController!.page?.round() ?? 0;

      setState(() {
        _pageController!.dispose();
        _pageController = PageController(
          viewportFraction: vp,
          initialPage: oldPage,
        );
        _pageController!.addListener(_handleScroll);
      });
    });
  }

  double _viewportFraction(double width) {
    if (width < 600) return 0.85;
    if (width < 1000) return 0.45;
    if (width < 1400) return 0.33;
    return 0.25;
  }

  void _handleScroll() {
    if (!_pageController!.hasClients) return;
    final page = _pageController!.page;
    if (page == null) return;

    final total = _loopedCards.length;
    final meio = _cards.length * (repeticao ~/ 2);
    final current = page.round();

    if (current <= _cards.length) {
      _pageController!.jumpToPage(current + meio);
    } else if (current >= total - _cards.length) {
      _pageController!.jumpToPage(current - meio);
    }
  }

  Future<Directory> _getDir() async {
    final dir = await getApplicationDocumentsDirectory();
    final cdir = Directory("${dir.path}/conversas");
    if (!cdir.existsSync()) cdir.createSync(recursive: true);
    return cdir;
  }

  void _atualizarTituloSeNecessario(String textoUsuario) {
    if (_conversaAtualId == null) return;

    final idx = _conversas.indexWhere(
      (c) => c["id"] == _conversaAtualId,
    );

    if (idx == -1) return;

    if (_conversas[idx]["titulo"] == "Nova conversa") {
      _conversas[idx]["titulo"] =
          textoUsuario.length > 32
              ? "${textoUsuario.substring(0, 32)}..."
              : textoUsuario;

      _salvarConversas();
      setState(() {});
    }
  }

  void _renomearConversa(Map<String, dynamic> c) {
    final controller = TextEditingController(text: c["titulo"]);

    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        backgroundColor: const Color(0xFF0D1B2A),
        title: const Text("Renomear conversa",
            style: TextStyle(color: Colors.white)),
        content: TextField(
          controller: controller,
          autofocus: true,
          style: const TextStyle(color: Colors.white),
          decoration: const InputDecoration(
            hintText: "Novo nome",
            hintStyle: TextStyle(color: Colors.white54),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text("Cancelar"),
          ),
          ElevatedButton(
            onPressed: () {
              c["titulo"] = controller.text.trim();
              _salvarConversas();
              setState(() {});
              Navigator.pop(context);
            },
            child: const Text("Salvar"),
          ),
        ],
      ),
    );
  }

  Future<void> _carregarConversas() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString("conversas");

    if (raw != null) {
      _conversas = List<Map<String, dynamic>>.from(jsonDecode(raw));
      setState(() {});
    }
  }

  Future<void> _salvarConversas() async {
    final prefs = await SharedPreferences.getInstance();
    prefs.setString("conversas", jsonEncode(_conversas));
  }

  Future<void> _salvarConversaTxt(String id) async {
    final dir = await _getDir();
    final file = File("${dir.path}/conversa_$id.txt");

    final buf = StringBuffer();
    for (final m in _messages){
      switch (m.kind){
        case MessageKind.user:
          buf.writeln("[USER] ${m.text}");
          break;

        case MessageKind.system:
          buf.writeln("[BOT] ${m.text}");
          break;

        case MessageKind.actionBlock:
          buf.writeln("[ACTION] ${m.title}");
          for (final item in m.items!){
            buf.writeln(" - $item");
          }
          if (m.footer != null){
            buf.writeln(" > ${m.footer}");
          }
          break;
      }
    }
    await file.writeAsString(buf.toString());
  }

  Future<List<Message>> _lerConversaTxt(String caminho) async {
    final file = File(caminho);
    if (!file.existsSync()) return [];

    final lines = await file.readAsLines();
    final List<Message> msgs = [];

    for (final i in lines){
      if (i.startsWith("[USER]")){
        msgs.add(Message.user(i.replaceFirst("[USER] ", "")));
      } else if (i.startsWith("[BOT]")){
        msgs.add(Message.system(i.replaceFirst("[BOT] ", "")));
      }
    }
    return msgs;
  }

  void _novaConversa() async {
    final id = uuid.v4();
    final dir = await _getDir();
    final file = File("${dir.path}/conversa_$id.txt");
    await file.create();

    final mapa = {
      "id": id,
      "titulo": "Nova conversa",
      "arquivo": file.path,
      "mensagens": [],
      "data": DateTime.now().toIso8601String(),
    };

    setState(() {
      _conversas.add(mapa);
      _messages.clear();
      _showHomeCards = true;
      _conversaAtualId = id;
    });

    _salvarConversas();
  }

  void _abrirConversa(Map<String, dynamic> c) async {
    final msgs = await _lerConversaTxt(c["arquivo"]);
    setState(() {
      _conversaAtualId = c["id"];
      _messages = msgs;
      _showHomeCards = false;
    });
  }

  Future<void> _apagarConversa(Map<String, dynamic> c) async {
    final file = File(c["arquivo"]);
    if (file.existsSync()) file.deleteSync();

    setState(() {
      _conversas.removeWhere((x) => x["id"] == c["id"]);
      if (_conversaAtualId == c["id"]) {
        _messages.clear();
        _showHomeCards = true;
        _conversaAtualId = null;
      }
    });

    _salvarConversas();
  }

  Future<void> _apagarTudo() async {
    final dir = await _getDir();
    for (final f in dir.listSync()) {
      if (f is File) f.deleteSync();
    }

    setState(() {
      _conversas.clear();
      _messages.clear();
      _conversaAtualId = null;
      _showHomeCards = true;
    });

    SharedPreferences.getInstance().then((p) => p.remove("conversas"));
  }

  Future<void> _sendMessage(String txt) async {
    if (txt.trim().isEmpty) return;
    _atualizarTituloSeNecessario(txt);

    setState(() {
      _messages.add(Message.user(txt));
      _showHomeCards = false;
      _isTyping = true;
    });

    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.jumpTo(0);
      }
    });

    _controller.clear();
    FocusScope.of(context).unfocus();

    await _executarAcaoStream(txt);

    setState(() => _isTyping = false);

    if (_conversaAtualId != null) {
      await _salvarConversaTxt(_conversaAtualId!);
    }
  }

  // SSE STREAM
  Future<void> _executarAcaoStream(String acao) async {
    final client = http.Client();
    final uri = Uri.parse(
      "$apiUrl/sse/run?text=${Uri.encodeComponent(acao)}",
    );

    try {
      final req = http.Request("GET", uri);
      final resp = await client.send(req);

      await for (String line in resp.stream
          .transform(utf8.decoder)
          .transform(const LineSplitter())) {

        if (!line.startsWith("data:")) continue;

        String raw = line;
        while (raw.startsWith("data:")) {
          raw = raw.substring(5).trim();
        }

        if (raw.isEmpty || raw == "[END]") continue;

        Map<String, dynamic> event;
        try {
          event = jsonDecode(raw);
        } catch (_) {
          debugPrint("⚠️ JSON inválido ignorado: $raw");
          continue;
        }

        final String message =
            (event["message"] ?? "").toString().trim();

        List<Attachment>? attachments;
        if (event["attachments"] != null &&
            event["attachments"] is List &&
            (event["attachments"] as List).isNotEmpty) {

          attachments = (event["attachments"] as List)
              .map((e) => Attachment.fromJson(e))
              .toList();
        }

        MediaAttachment? media;
        if (event["media"] != null && event["media"] is Map) {
          media = MediaAttachment.fromJson(
            Map<String, dynamic>.from(event["media"]),
          );
        }

        if (event["items"] != null && event["items"] is List) {
          setState(() {
            _messages.add(
              Message.actionBlock(
                title: event["title"] ?? "Análise",
                items: List<String>.from(event["items"]),
                footer: event["footer"],
              ),
            );
          });
          continue;
        }
        final String title =
              (event["title"] ?? "").toString().trim();
          if (title.toLowerCase() == "interpretando" &&
              message.isEmpty &&
              attachments == null) {
            continue;
          }

          if (message.isNotEmpty ||
              attachments != null ||
              media != null ||
              title.isNotEmpty) {
            setState(() {
              _messages.add(
                Message.system(
                  message.isNotEmpty ? message : title,
                  attachments: attachments,
                  media: media, // ← NOVO
                ),
              );
            });
          }

        WidgetsBinding.instance.addPostFrameCallback((_) {
          if (_scrollController.hasClients) {
            _scrollController.jumpTo(
              _scrollController.position.maxScrollExtent,
            );
          }
        });
      }
    } catch (e) {
      setState(() {
        _messages.add(
          Message.system("Erro de comunicação com o backend."),
        );
      });
    } finally {
      client.close();
    }
  }



  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0B1220),
      drawer: _buildDrawer(),
      appBar: _appBar(),
      body: Column(
        children: [
          if (_showHomeCards) _homeHeader(),
          if (_showHomeCards) _carousel(),
          Expanded(
              child: TimelinePanel(
                messages: _messages,
                controller: _scrollController,
              ),
            ),
          if (_isTyping) _typing(),
          _inputBar(),
        ],
      ),
    );
  }

  Widget _arrowButton({
    required IconData icon,
    required VoidCallback onTap,
  }) {
    return Center(
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: 4),
        decoration: BoxDecoration(
          color: Colors.black.withOpacity(0.35),
          shape: BoxShape.circle,
        ),
        child: IconButton(
          icon: Icon(icon, color: Colors.white),
          iconSize: 34,
          onPressed: onTap,
        ),
      ),
    );
  }

  AppBar _appBar() {
    return AppBar(
      backgroundColor: const Color(0xFF0D1B2A),
      centerTitle: true,
      title: const Text(
        "MFSim Assistant",
        style: TextStyle(color: Colors.white, fontWeight: FontWeight.w600),
      ),
    );
  }

  Widget _homeHeader() {
    return Column(
      children: const [
        SizedBox(height: 20),
        Image(image: AssetImage("assets/robot_mfsim.png"), height: 110),
        SizedBox(height: 12),
        Text("Olá, Comandante!",
            style: TextStyle(color: Colors.white, fontSize: 20)),
        SizedBox(height: 4),
        Text("Como posso ajudar hoje?",
            style: TextStyle(color: Colors.white54, fontSize: 14)),
        SizedBox(height: 20),
      ],
    );
  }

  Widget _carousel() {
  if (_pageController == null) {
    return const SizedBox(
      height: 210,
      child: Center(
        child: CircularProgressIndicator(color: Colors.white),
      ),
    );
  }

  return SizedBox(
    height: 210,
    child: Stack(
      children: [
        PageView.builder(
          controller: _pageController!,
          itemCount: _loopedCards.length,
          itemBuilder: (_, i) => _loopedCards[i],
        ),

        // ⬅️ SETA ESQUERDA
        Positioned(
          left: 0,
          top: 0,
          bottom: 0,
          child: _arrowButton(
            icon: Icons.chevron_left_rounded,
            onTap: () {
              _pageController!.previousPage(
                duration: const Duration(milliseconds: 300),
                curve: Curves.easeOut,
              );
            },
          ),
        ),

        // ➡️ SETA DIREITA
        Positioned(
          right: 0,
          top: 0,
          bottom: 0,
          child: _arrowButton(
            icon: Icons.chevron_right_rounded,
            onTap: () {
              _pageController!.nextPage(
                duration: const Duration(milliseconds: 300),
                curve: Curves.easeOut,
              );
            },
          ),
        ),
      ],
    ),
  );
}

  Widget _typing() => const Padding(
        padding: EdgeInsets.all(10),
        child: SpinKitThreeBounce(size: 18, color: Colors.white),
      );

  Widget _inputBar() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      decoration: const BoxDecoration(
        color: Color(0xFF0D1B2A),
        border: Border(top: BorderSide(color: Color(0xFF1A2536))),
      ),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _controller,
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(
                border: InputBorder.none,
                hintText: "Digite sua mensagem...",
                hintStyle: TextStyle(color: Colors.white54),
              ),
              onSubmitted: _sendMessage,
            ),
          ),
          IconButton(
            icon: const Icon(Icons.send_rounded, color: Colors.white),
            onPressed: () => _sendMessage(_controller.text),
          ),
        ],
      ),
    );
  }

  Widget _buildFeatureCard({
    required String title,
    required String description,
    required IconData icon,
    required String message,
  }) {
    return GestureDetector(
      onTap: () => _sendMessage(message),
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: const Color(0xFF0D1B2A),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: const Color(0xFF1A2536)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, size: 30, color: Colors.white70),
            const SizedBox(height: 10),
            Text(title, style: const TextStyle(color: Colors.white)),
            const SizedBox(height: 6),
            Text(description, style: const TextStyle(color: Colors.white54)),
          ],
        ),
      ),
    );
  }

  Drawer _buildDrawer() {
    return Drawer(
      backgroundColor: const Color(0xFF0D1B2A),
      child: Column(
        children: [
          Image(image: AssetImage("assets/robot_mfsim.png"), height: 110),
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 8, 16, 4),
            child: Align(
              alignment: Alignment.centerLeft,
              child: Text(
                "Conversas",
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ),
          const Divider(
            color: Colors.white24,
            height: 1,
            thickness: 1,
          ),
          ListTile(
            leading: const Icon(Icons.add, color: Colors.white),
            title: const Text("Nova conversa", style: TextStyle(color: Colors.white)),
            onTap: () {
              Navigator.pop(context);
              _novaConversa();
            },
          ),

          ListTile(
            leading: const Icon(Icons.delete_forever, color: Colors.redAccent),
            title: const Text("Apagar todas", style: TextStyle(color: Colors.redAccent)),
            onTap: () {
              Navigator.pop(context);
              _apagarTudo();
            },
          ),

          const Divider(color: Colors.white24),

          Expanded(
            child: ListView.builder(
              itemCount: _conversas.length,
              itemBuilder: (_, i) {
                final c = _conversas[i];
                return ListTile(
                  leading: const Icon(Icons.chat_outlined, color: Colors.white70),
                  title: Text(
                    c["titulo"],
                    style: const TextStyle(color: Colors.white),
                  ),
                  subtitle: Text(
                    c["data"].toString().substring(0, 10),
                    style: const TextStyle(color: Colors.white54),
                  ),
                  trailing: IconButton(
                    icon: const Icon(Icons.delete_outline, color: Colors.redAccent),
                    onPressed: () => _apagarConversa(c),
                  ),
                  onTap: () {
                    Navigator.pop(context);
                    _abrirConversa(c);
                  },
                  onLongPress: () => _renomearConversa(c), 
                );
              },
            ),
          )
        ],
      ),
    );
  }
}
