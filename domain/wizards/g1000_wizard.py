G1000_WIZARD = {
    "id": "g1000_install",
    "title": "Instalação do G1000",
    "trigger": [
        "instalação g1000",
        "instalar g1000",
        "iniciar g1000"
    ],
    "mode": "wizard",
    "steps": [
        {
            #Verificar se a tela ja abriu/executou
            "id": "start",
            "message": (
                "Olá, Comandante! Vamos iniciar a instalação completa do G1000 MFSim. "
                "Está preparado para começar?"
            ),
            "type": "confirmation"
        },
        {
            "id": "copy_plugins",
            "message": (
                "1° Passo: Copiar os plugins do G1000 para a pasta "
                "'Resources/plugins' do X-Plane. "
                "Deseja que eu faça isso automaticamente?"
            ),
            "type": "confirmation",
            "action": "copiar_plugins_g1000"
        },
        {
            "id": "copy_joystick_files",
            "message": (
                "2° Passo: Copiar os arquivos de configuração do joystick "
                "para o X-Plane. "
                "Deseja que eu faça isso automaticamente?"
            ),
            "type": "confirmation",
            "action": "copiar_arquivos_joystick_g1000"
        },
        {
            "id": "open_xplane",
            "message": (
                "3° Passo: Abrir o X-Plane. "
                "Deseja que eu inicie o simulador automaticamente agora?"
            ),
            "type": "confirmation",
            "action": "start_sim"
        },
        {
            "id": "run_connector",
            "message": (
                "4° Passo: Executar o conector MFSim G1000. "
                "Deseja que eu abra o conector automaticamente?"
            ),
            "type": "confirmation",
            "action": "executar_conector_g1000"
        },
        {
            "id": "adjust_screens",
            "message": (
                "5° Passo: Ajustar as telas do G1000 no X-Plane. "
                "Vou orientar o ajuste de resolução e posicionamento. "
                "Quando estiver pronto para continuar, digite OK."
            ),
            "type": "wait_ok"
        },
        {
            "id": "adjust_instruments",
            "message": (
                "5° Passo: Inserir os instrumentos do G1000 na aeronave "
                "e ajustar corretamente o posicionamento na tela. "
                "Realize os ajustes conforme orientação. "
                "Quando finalizar, digite OK."
            ),
            "type": "wait_ok"
        },
        {
            "id": "save_preferences",
            "message": (
                "6° Passo: Salvar as configurações do X-Plane. "
                "Vou copiar a pasta:\n"
                "X-Plane 12/Output/preferences\n"
                "para: "
                "X-Plane 12/Output/RESET\n"
                "Deseja que eu faça isso automaticamente?"
            ),
            "type": "confirmation",
            "action": "salvar_configuracoes_g1000"
        },
        {
            "id": "pin_apps",
            "message": (
                "7° Passo: Criar atalhos do G1000 na área de trabalho "
                "para acesso rápido. "
                "Deseja que eu faça isso agora?"
            ),
            "type": "confirmation",
            "action": "fixar_g1000_area_trabalho"
        },
        {
            "id": "finish",
            "message": (
                "Instalação do G1000 concluída com sucesso, Comandante. "
                "O sistema está pronto para operação. "
                "Bons voos!"
            ),
            "type": "final"
        }
    ]
}
