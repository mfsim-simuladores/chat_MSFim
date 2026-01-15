GFC700_WIZARD = {
    "id": "gfc700_install",
    "title": "Instalação do GFC700",
    "trigger": ["instalação gfc700", "instalar gfc700", "iniciar gfc700"],
    "mode": "wizard",
    "steps": [
        {
            "id": "start",
            "message": (
                "Olá, Comandante! Vamos começar a instalação do GFC700. "
                "Está preparado?"
            ),
            "type": "confirmation"
        },
        {
            "id": "copy_plugins",
            "message": (
                "1° Passo: Copiar o plugin correspondente para "
                "'Resources/plugins' do X-Plane. "
                "Deseja que eu faça isso automaticamente?"
            ),
            "type": "confirmation",
            "action": "copiar_plugins_gfc700"
        },
        {
            "id": "simulador",
            "message": (
            "Para o próximo passo vou inicializar o simulador "
            "para que você coloque um aviao na pista! "
            "Posso executar o simulador?"
            ),
            "type": "confirmation",
            "action": "start_sim"
        },
        {
            "id": "run_connector",
            "message": (
                "2° Passo: Executar o conector MFSim GFC700 conforme "
                "o simulador instalado. Deseja que eu faça isso?"
            ),
            "type": "confirmation",
            "action": "executar_conector_gfc700_csharp"
        },
        {
            "id": "wait_connection",
            "message": (
                "3° Passo: No conector, selecione a porta COM do GFC700 "
                "e clique em 'Conectar'. "
                "Quando a conexão for realizada, digite OK."
            ),
            "type": "wait_ok"
        },
        {
            "id": "pin_app",
            "message": (
                "Deseja colocar o aplicativo GFC700 na área de trabalho "
                "para acesso rápido?"
            ),
            "type": "confirmation",
            "action": "fixar_gfc700_taskbar_csharp"
        },
        {
            "id": "finish",
            "message": (
                "Instalação finalizada com sucesso, Comandante. "
                "Sistema pronto para voo!"
            ),
            "type": "final"
        }
    ]
}
