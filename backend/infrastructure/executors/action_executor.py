import os
import shutil
import socket
import subprocess
import time
import win32com.client as win32
from domain.xplane.services.tcp_client import XPlaneTCPClient
from domain.logging.sse_events import SSEEvent
from domain.actions.registry import ACTIONS_REGISTRY
from domain.state.conversation_state import conversation_state
from domain.xplane.exceptions import (
    XplaneConnectionError,
    XplaneEmptyResponse
)

class ActionExecutor:

    def __init__(self, feedback_callback=None):
        self.feedback = feedback_callback or (lambda x: None)
        self.tcp = XPlaneTCPClient()

    def set_feedback(self, cb):
        self.feedback = cb

    def execute(self, action_name: str, payload=None):
        print(f"🔥 Executor recebeu ação: {action_name}")

        action = ACTIONS_REGISTRY.get(action_name)

        if not action:
            self.feedback(
                SSEEvent.error(
                    title="Ação desconhecida",
                    message=f"Ação '{action_name}' não está registrada."
                )
            )
            return

        try:
            result = action.execute(self, payload or {})

            if isinstance(result, str) and result.strip():
                self.feedback(
                    SSEEvent.log(
                        result,
                        title="Assistente"
                    )
                )

        except Exception as e:
            self.feedback(
                SSEEvent.error(
                    title="Erro na ação",
                    message=str(e)
                )
            )


    def log_info(self, title, message, action=None):
        self.feedback(SSEEvent.action(title, message, action))

    def log_success(self, title, message, action=None):
        self.feedback(SSEEvent.finished(action or title, message))

    def log_warning(self, title, message, action=None):
        self.feedback(SSEEvent.build("warning", title, message, action))

    def log_error(self, title, message, action=None):
        self.feedback(SSEEvent.error(title, message))

    def log_progress(self, title, message, progress, action=None):
        self.feedback(SSEEvent.progress(title, message, progress, action))

    def responder_texto(self):
        if isinstance(payload, dict):
            return payload.get("texto", "")
        return payload

    def varredura_xplane(self):
        self.log_info("Varredura", "Procurando X-Plane nos discos...", "varredura_xplane")

        for drive in ["C:\\", "D:\\"]:
            for root, _, files in os.walk(drive):
                if "X-Plane.exe" in files:
                    caminho = os.path.join(root, "X-Plane.exe")

                    self.log_success(
                        "X-Plane encontrado",
                        f"Localizado em: {caminho}",
                        "varredura_xplane"
                    )
                    return caminho

        self.log_error(
            "X-Plane não encontrado",
            "Nenhuma instalação foi encontrada.",
            "varredura_xplane"
        )
        return None

    def abrir_xplane(self):
        caminho = self.varredura_xplane()
        if not caminho:
            return

        try:
            self.log_info("Abrindo X-Plane", "Preparando execução...", "start_sim")
            os.startfile(caminho)
            time.sleep(2)

            self.log_success("X-Plane iniciado", "O simulador foi iniciado com sucesso.", "start_sim")

        except Exception as e:
            self.log_error("Falha ao iniciar X-Plane", str(e), "start_sim")

    def verificar_instalacao_xplane(self):
        caminho = self.varredura_xplane()
        if not caminho:
            return

        versao = "12" if "12" in caminho else "11"

        self.log_success(
            "Instalação detectada",
            f"X-Plane {versao} encontrado.",
            "verificar_insxplane"
        )

    def plugins_xplane(self, pasta_origem="D:\\plugins _originais"):
        xplane = self.varredura_xplane()
        if not xplane:
            return

        destino = os.path.join(os.path.dirname(xplane), "Resources", "plugins")

        if not os.path.exists(destino):
            self.log_error("Destino inválido", "Pasta Resources/plugins não encontrada.", "plugins_xplane")
            return

        self.log_info("Sincronização", "Copiando plugins...", "plugins_xplane")

        for item in os.listdir(pasta_origem):
            origem = os.path.join(pasta_origem, item)
            destino_item = os.path.join(destino, item)

            if os.path.exists(destino_item):
                self.log_info("Ignorando", f"Já existe: {item}", "plugins_xplane")
                continue

            if os.path.isdir(origem):
                shutil.copytree(origem, destino_item)
            else:
                shutil.copy2(origem, destino_item)

            self.log_success("Copiado", f"{item}", "plugins_xplane")

        self.log_success("Concluído", "Plugins sincronizados com sucesso.", "plugins_xplane")

    def _get_status(self):

        status = self.tcp.get_status()
        if not status:
            self.feedback("❌ Sem resposta do plugin MFSim_TCP.")
        return status

    def diagnosticar_bussola(self):
        status = self._get_status()
        if not status:
            return

        erros = []

        bateria = status.get_bool("BATTERY")
        avionic = status.get_bool("AVIONIC")
        magneto = status.get_int("MAGNETO") == 3

        if bateria and avionic and magneto:
            self.feedback("✅ Bússola e sistemas elétricos OK.")
            return

        self.feedback("⚠️ Problemas detectados na bússola:")
        if not bateria: erros.append("🔋 Bateria desligada")
        if not avionic: erros.append("📟 Aviônicos desligados")
        if not magneto: erros.append("🔑 Magnetos fora de BOTH")

        if not erros:
            self.feedback(SSEEvent.finished(
                "diagnosticar_bussola",
                " ✅ Bússola e sistemas elétricos OK."
            )) 
            return

        for e in erros:
            self.log_info(
                "Problemas no avião",
                e,
                "corrigir_prevoo"
            )
        
        conversation_state.start_confirmation("corrigir_prevoo")

        self.feedback(
            SSEEvent.question("Correção automática",
            "Deseja que eu corrija automaticamente os parâmetros do motor?",
            "corrigir_prevoo")
        )

    def diagnosticar_motor(self):
        status = self._get_status()
        if not status:
            return
        erros = []

        mix = status.get_float("MIXTURE")
        throtlle = status.get_float("THROTTLE")
        fuel = status.get_bool("FUEL")
        magneto = status.get_int("MAGNETO")

        if not fuel:
            erros.append("⛽ Combustível desligado")

        if magneto != 3: 
            erros.append("🔑 Magnetos fora de BOTH")

        if mix is None or mix < 0.8:
             erros.append("🔧 Mistura pobre")

        if throtlle is None or throtlle < 0.1:
            erros.append("🛞 Potência insuficiente")

        if not erros:
            self.log_success(
                "Motor OK",
                "Configuração do motor está correta.",
                "diagnosticar-motor"
            )
            return

        for e in erros:
            self.log_info("Problema no motor", e, "corrigir_prevoo")
        
        conversation_state.start_confirmation("corrigir_prevoo")

        self.log_info(
            "Correção automática",
            "Deseja que eu corrija automaticamente os itens do motor?",
            "corrigir_prevoo"
        )

    def checklist_pre_voo(self, context: dict | None = None):

        if context is None:
            context= {}

        try:
            status = self._get_status()
        except (XplaneConnectionError, XplaneEmptyResponse) as e:
            self.feedback(
                SSEEvent.error(
                    "preparar_voo",
                    f"Erro ao conectar com o X-Plane: {e}"
                )
            )
            return


        if not status:
            self.feedback(
                SSEEvent.error(
                    "preparar_voo",
                    "Não foi possível obter o status da aeronave."
                )
            )
            return

        erros = []

        if not status.get_bool("BATTERY"):
            erros.append("🔋 Bateria desligada")

        if not status.get_bool("BEACON"):
            erros.append("💡 Beacon desligado")

        if not status.get_bool("AVIONIC"):
            erros.append("📟 Aviônicos OFF")

        if not status.get_bool("FUEL"):
            erros.append("⛽ Combustível incorreto")

        magneto = status.get_int("MAGNETO")
        if magneto != 3:
            erros.append("🔑 Magnetos != BOTH")

        mix = status.get_float("MIXTURE")
        prop = status.get_float("PROP")
        thr = status.get_float("THROTTLE")

        if mix is None or mix < 0.8:
            erros.append("🔧 Mistura pobre")

        if prop is None or prop < 0.8:
            erros.append("⚙️ Hélice não em máximo")

        if thr is None or thr > 0.1:
            erros.append("🛞 Potência não em idle")

        if not erros:
            self.log_success("✅ Checklist pré-voo aprovado!", "O avião está pronto para voar.", "checklist_pre_voo")
            return

        for e in erros:
            self.log_info("⚠️ Itens incorretos detectados", e, "corrigir_prevoo")

        conversation_state.start_confirmation("corrigir_prevoo")

        self.feedback(
            SSEEvent.question(
                title="Correção automática",
                message= "Deseja que eu corrija automaticamente os itens do pré-voo?",
                action_name="corrigir_prevoo"
            )
        )
        
        return
            
    def executar_correcao_automatica(self):
        comandos = [
            "BATTERY_ON=1",
            "AVIONIC_ON=1",
            "MAGNETO_BOTH=1"
        ]

        if self.tcp.send_commands(comandos):
            self.feedback("✅ Correção aplicada.")
        else:
            self.feedback("❌ Erro ao aplicar correção.")
        self.log_info("Correção", "Aplicando ajustes automáticos...", "corrigir_prevoo")

        try:
            with socket.create_connection(("127.0.0.1", 49005), timeout=2) as c:
                stream = c.makefile("w", encoding="ascii", newline="\r\n")

                cmds = [
                    "BATTERY_ON=1",
                    "AVIONIC_ON=1",
                    "MAGNETO_BOTH=1"
                ]

                for cmd in cmds:
                    stream.write(cmd + "\r\n")
                    stream.flush()
                    time.sleep(0.15)

            self.log_success("Correção aplicada", "Todos parâmetros ajustados.", "corrigir_prevoo")

        except Exception as e:
            self.log_error("Erro na correção", str(e), "corrigir_prevoo")

# instalação GFC700
    def copiar_plugins_gfc700(self):
        raiz = r"D:\arquivosChat\GFC700\MFSim GFC700 XPLANE"

        if not os.path.exists(raiz):
            self.feedback(
                SSEEvent.error(
                    "GFC700",
                    "❌ Pasta do GFC700 não encontrada."
                )
            )
            return

        exe = self.varredura_xplane()
        if not exe:
            return

        versao = "11" if "11" in exe else "12"
        origem = os.path.join(raiz, f"Plugins Xplane {versao}")

        destino = os.path.join(
            os.path.dirname(exe),
            "Resources",
            "plugins",
            os.path.basename(origem)
        )

        self.feedback(
            SSEEvent.action(
                "GFC700",
                f"📂 Copiando plugins para:\n{destino}",
                "copiar_plugins_gfc700"
            )
        )

        try:
            if os.path.exists(destino):
                shutil.rmtree(destino)

            shutil.copytree(origem, destino)

            self.feedback(
                SSEEvent.finished(
                    "copiar_plugins_gfc700",
                    "✅ Plugins GFC700 instalados com sucesso."
                )
            )

        except Exception as e:
            self.feedback(
                SSEEvent.error(
                    "Erro ao copiar plugins",
                    str(e)
                )
            )

    def executar_conector_gfc700_csharp(self):
        exe = r"D:\arquivosChat\GFC700\MFSim GFC700 XPLANE\MFSim Driver Connection.exe"

        if not os.path.exists(exe):
            self.feedback(
                SSEEvent.error(
                    "GFC700",
                    "❌ Driver Connection não encontrado."
                )
            )
            return

        self.feedback(
            SSEEvent.action(
                "GFC700",
                "🚀 Iniciando Driver Connection...",
                "executar_conector_gfc700_csharp"
            )
        )

        try:
            subprocess.Popen([exe], shell=True)

            self.feedback(
                SSEEvent.finished(
                    "executar_conector_gfc700_csharp",
                    "Driver Connection iniciado com sucesso."
                )
            )

        except Exception as e:
            self.feedback(
                SSEEvent.error(
                    "Erro ao iniciar Driver",
                    str(e)
                )
            )

    def fixar_gfc700_taskbar_csharp(self):
        exe = r"D:\arquivosChat\GFC700\MFSim GFC700 XPLANE\MFSim Driver Connection.exe"

        if not os.path.exists(exe):
            self.feedback(
                SSEEvent.error(
                    "GFC700",
                    "❌ Executável do GFC700 não encontrado."
                )
            )
            return

        self.feedback(
            SSEEvent.action(
                "GFC700",
                "📎 Criando atalho na área de trabalho...",
                "fixar_gfc700_taskbar_csharp"
            )
        )

        try:
            desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
            shortcut = os.path.join(desktop, "MFSim GFC700.lnk")

            shell = win32.Dispatch("WScript.Shell")
            link = shell.CreateShortcut(shortcut)
            link.TargetPath = exe
            link.WorkingDirectory = os.path.dirname(exe)
            link.Description = "MFSim GFC700"
            link.IconLocation = exe
            link.Save()

            self.feedback(
                SSEEvent.finished(
                    "fixar_gfc700_taskbar_csharp",
                    "Atalho do GFC700 criado com sucesso na área de trabalho."
                )
            )

        except Exception as e:
            self.feedback(
                SSEEvent.error(
                    "Erro ao criar atalho",
                    str(e)
                )
            )

# instalação G1000
    def copiar_plugins_g1000(self):
        raiz = r"D:\arquivosChat\G1000\XPLANE\MFsim\Resources"

        if not os.path.exists(raiz):
            self.feedback(
                SSEEvent.error(
                    "G1000",
                    "❌ Pasta do G1000 não encontrada."
                )
            )
            return

        exe = self.varredura_xplane()
        if not exe:
            return

        versao = "11" if "11" in exe else "12"
        origem = os.path.join(raiz, f"plugins")

        destino = os.path.join(
            os.path.dirname(exe),
            "Resources",
            "plugins",
            os.path.basename(origem)
        )

        self.feedback(
            SSEEvent.action(
                "G1000",
                f"📂 Copiando plugins para:\n{destino}",
                "copiar_plugins_g1000"
            )
        )

        try:
            if os.path.exists(destino):
                shutil.rmtree(destino)

            shutil.copytree(origem, destino)

            self.feedback(
                SSEEvent.finished(
                    "copiar_plugins_g1000",
                    "✅ Plugins G1000 instalados com sucesso."
                )
            )

        except Exception as e:
            self.feedback(
                SSEEvent.error(
                    "Erro ao copiar plugins",
                    str(e)
                )
            )

    def copiar_arquivos_joystick_g1000(self):
        origem = r"D:\arquivosChat\Joysticks"

        if not os.path.exists(origem):
            self.feedback(
                SSEEvent.error(
                    "G1000",
                    "❌ Pasta de Joysticks não encontrada."
                )
            )
            return

        # Localiza o X-Plane automaticamente
        exe = self.varredura_xplane()
        if not exe:
            return

        xplane_root = os.path.dirname(exe)
        destino = os.path.join(
            xplane_root,
            "Resources",
            "joystick configs"
        )

        # Garante que a pasta de destino exista
        os.makedirs(destino, exist_ok=True)

        self.feedback(
            SSEEvent.action(
                "G1000",
                f"🎮 Copiando arquivos de joystick para:\n{destino}",
                "copiar_joystick_g1000"
            )
        )

        try:
            for item in os.listdir(origem):
                src = os.path.join(origem, item)
                dst = os.path.join(destino, item)

                if os.path.isdir(src):
                    # Se existir, sobrescreve
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

            self.feedback(
                SSEEvent.finished(
                    "copiar_joystick_g1000",
                    "✅ Arquivos de joystick copiados com sucesso."
                )
            )

        except Exception as e:
            self.feedback(
                SSEEvent.error(
                    "Erro ao copiar joystick configs",
                    str(e)
                )
            )

    def executar_conector_g1000(self):
        exe = r"D:\softwaresMfsim\ConnectorMfsim\connector.exe"

        if not os.path.exists(exe):
            self.feedback(
                SSEEvent.error(
                    "G1000",
                    "❌ Driver Connection não encontrado."
                )
            )
            return

        self.feedback(
            SSEEvent.action(
                "G1000",
                "🚀 Iniciando Driver Connection...",
                "executar_conector_g1000"
            )
        )

        try:
            subprocess.Popen([exe], shell=True)

            self.feedback(
                SSEEvent.finished(
                    "executar_conector_g1000",
                    "Driver Connection iniciado com sucesso."
                )
            )

        except Exception as e:
            self.feedback(
                SSEEvent.error(
                    "Erro ao iniciar Driver",
                    str(e)
                )
            )

    def fixar_g1000_area_trabalho(self):
        exe = r"D:\softwaresMfsim\ConnectorMfsim\connector.exe"

        if not os.path.exists(exe):
            self.feedback(
                SSEEvent.error(
                    "G1000",
                    "❌ Executável do G1000 não encontrado."
                )
            )
            return

        self.feedback(
            SSEEvent.action(
                "G1000",
                "📎 Criando atalho na área de trabalho...",
                "fixar_g1000_area_trabalho"
            )
        )

        try:
            desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
            shortcut = os.path.join(desktop, "MFSim G1000.lnk")

            shell = win32.Dispatch("WScript.Shell")
            link = shell.CreateShortcut(shortcut)
            link.TargetPath = exe
            link.WorkingDirectory = os.path.dirname(exe)
            link.Description = "MFSim G1000"
            link.IconLocation = exe
            link.Save()

            self.feedback(
                SSEEvent.finished(
                    "fixar_g1000_area_trabalho",
                    "Atalho do G1000 criado com sucesso na área de trabalho."
                )
            )

        except Exception as e:
            self.feedback(
                SSEEvent.error(
                    "Erro ao criar atalho",
                    str(e)
                )
            )

    def salvar_configuracoes_g1000(self):
        import os
        import shutil

        exe = self.varredura_xplane()
        if not exe:
            return

        origem = os.path.join(
            os.path.dirname(exe),
            "Output",
            "preferences"
        )

        if not os.path.exists(origem):
            self.feedback(
                SSEEvent.error(
                    "G1000",
                    "❌ Pasta Output/preferences não encontrada."
                )
            )
            return

        destino = os.path.join(
            os.path.dirname(exe),
            "Output",
            "RESET"
        )

        self.feedback(
            SSEEvent.action(
                "G1000",
                f"💾 Salvando configurações do X-Plane:\n{destino}",
                "salvar_configuracoes_g1000"
            )
        )

        try:
            if os.path.exists(destino):
                shutil.rmtree(destino)

            shutil.copytree(origem, destino)

            self.feedback(
                SSEEvent.finished(
                    "salvar_configuracoes_g1000",
                    "✅ Configurações salvas com sucesso em Output/RESET."
                )
            )

        except Exception as e:
            self.feedback(
                SSEEvent.error(
                    "Erro ao salvar configurações",
                    str(e)
                )
            )
