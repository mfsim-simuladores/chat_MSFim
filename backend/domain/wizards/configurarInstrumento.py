CONFIG_INSTRU = {
    "id": "instrumento_config",
    "title": "Configuração dos instrumentos MFSim",
    "trigger": [
        "configurar instrumentos",
        "configurar avionicos",
        "arrumar instrumentos",
        "arrumar avionicos",
        "instrumento saiu do lugar"
    ],
    "mode": "wizard",
    "steps": [
        {
            "id": "start",
             "message": (
                "Neste vídeo mostramos todas as formas de ajustar os instrumentos:\n"
                "- Seleção do instrumento\n"
                "- Ajuste por teclado\n"
                "- Ajuste com o mouse\n"
                "- Reset e salvamento\n\n"
                "Use o método que preferir."
            ),
            "media": {
                "type": "video",
                "label": "Tutorial completo de ajuste de instrumentos",
                "url": "/media/manual_instrumentos.mp4"
                },
            "type": "confirmation"
        },
    ]
}
