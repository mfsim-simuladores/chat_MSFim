CONFIG_EIXOS = {
    "id": "manche_config",
    "title": "Configuração de Manche e Pedais",
    "trigger": [
        "configurar eixos",
        "configurar manche",
        "configurar pedal",
        "arrumar pedal",
        "manche nao funciona"
    ],
    "mode": "wizard",
    "steps": [
        {
            "id": "start",
            "message": (
                "Olá, Comandante. Vamos iniciar a configuração dos eixos e botões do seu equipamento.\n"
                "Está pronto para começar?"
            ),
            "type": "confirmation"
        },
        {
            "id": "abrir_xplane",
            "message": (
                "1º Passo: Abrir o X-Plane.\n"
                "Deseja que o simulador seja iniciado automaticamente agora?"
            ),
            "type": "confirmation",
            "action": "start_sim"
        },
        {
            "id": "selec_propriedades",
            "message": (
                "2º Passo: No menu principal do X-Plane, selecione a opção *Propriedades*.\n"
                "Caso o voo já esteja iniciado e a aeronave esteja posicionada na pista, "
                "clique no ícone de engrenagem localizado no canto superior direito da tela "
                "(*Painel de Configuração*).\n"
                "Após concluir este passo, digite OK."
            ),
             "media": {
                "type": "video",
                "label": "Abrindo o painel de configuração",
                "url": "/media/manche_p2.mp4"          
            },
            "type": "wait_ok"
        },
        {
            "id": "selec_joystick",
            "message": (
                "3º Passo: Na parte superior da tela, selecione a aba *Joystick*.\n"
                "Após concluir este passo, digite OK."
            ),
                "media": {
                    "type": "video",
                    "label": "Abrindo aba Joystick",
                    "url": "/media/manche_p3.mp4"          
            },
            "type": "wait_ok"
        },
        {
            "id": "selec_equipamento",
            "message": (
                "4º Passo: Na seção *Equipamento*, clique na seta localizada ao lado do botão *Calibrar*.\n"
                "Selecione o módulo correspondente ao equipamento MFSim.\n"
                "Após concluir este passo, digite OK."
            ),
            "type": "wait_ok"
        },
        {
            "id": "selec_caliagora",
            "message": (
                "5º Passo: Clique no botão azul *Calibrar Agora*.\n"
                "Mova cada eixo do equipamento até seus limites máximo e mínimo para realizar a calibração.\n"
                "Após finalizar a calibração, digite OK."
            ),
            "type": "wait_ok"
        },
        {
            "id": "move_equip",
            "message": (
                "6º Passo: Após calibrar todos os eixos (conforme indicado na tela), selecione *Seguinte*.\n"
                "Após concluir este passo, digite OK."
            ),
            "type": "wait_ok"
        },
        {
            "id": "slect_seg",
            "message": (
                "7º Passo: Centralize fisicamente o manche nos eixos de Aileron e Profundor.\n"
                "Em seguida, selecione *Seguinte*.\n"
                "Após concluir este passo, digite OK."
            ),
            "type": "wait_ok"
        },
        {
            "id": "finish_config",
            "message": (
                "8º Passo: Selecione *Finalizar* e, em seguida, *Concluído*.\n"
                "Após concluir este passo, digite OK."
            ),
            "type": "wait_ok"
        },
        {
            "id": "finish",
            "message": (
                "Configuração concluída com sucesso.\n"
                "Os eixos do seu equipamento foram configurados corretamente.\n\n"
                "Caso tenha dúvidas adicionais, consulte o manual em PDF com todas as instruções detalhadas "
                "para configuração de manche e botões.\n\n"
                "Bons voos!"
            ),
            "attachments": [
                {
                    "type": "pdf",
                    "label": "Manual do Manche",
                    "url": "/files/MfsimManualMancheAtualizado.pdf"
                }
            ],
            "type": "final"
        }
    ]
}
