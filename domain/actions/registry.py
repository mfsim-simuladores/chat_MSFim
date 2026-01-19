from .verificar_inst_xplane_action import VerificarInstalacaoXPlaneAction
from .start_sim_action import StartSimAction
from .preparar_voo_action import PrepararVooAction
from .copiar_plugins_gfc700_action import CopiarPluginsGFC700Action
from .corrigir_bussola_action import CorrigirBussolaAction
from .corrigir_prevoo_action import CorrigirPreVooAction
from .diagnosticar_bussola_action import DiagnosticarBussolaAction
from .diagnosticar_motor_action import DiagnosticarMotorAction
from .executar_conector_gfc700_action import ExecutarConectorGFC700Action
from .fixar_gfc700_taskbar_action import FixarGFC700TaskbarAction
from .plugins_xplane_action import PluginsXPlaneAction
from .copiar_plugins_g1000_action import CopiarPluginsG1000Action
from .copiar_arquivos_joystick_g1000_action import CopiarArquivosG1000Action
from .executar_conector_g1000_action import ExecutarConectorG1000Action
from .salvar_configuracoes_g1000_action import salvarConfiguracoes
from .fixar_g1000_area_trabalho_action import fixar_g1000_area_trabalho
from .responder_texto_action import RespondeTextoAction

ACTIONS_REGISTRY = {
    VerificarInstalacaoXPlaneAction.action_name: VerificarInstalacaoXPlaneAction(),
    StartSimAction.action_name: StartSimAction(),
    PrepararVooAction.action_name: PrepararVooAction(),
    PluginsXPlaneAction.action_name: PluginsXPlaneAction(),
    FixarGFC700TaskbarAction.action_name: FixarGFC700TaskbarAction(),
    ExecutarConectorGFC700Action.action_name: ExecutarConectorGFC700Action(),
    DiagnosticarMotorAction.action_name: DiagnosticarMotorAction(),
    DiagnosticarBussolaAction.action_name: DiagnosticarBussolaAction(),
    CorrigirBussolaAction.action_name: CorrigirBussolaAction(),
    CorrigirPreVooAction.action_name: CorrigirPreVooAction(),
    CopiarPluginsGFC700Action.action_name: CopiarPluginsGFC700Action(),
    CopiarPluginsG1000Action.action_name: CopiarPluginsG1000Action(),
    CopiarArquivosG1000Action.action_name: CopiarArquivosG1000Action(),
    ExecutarConectorG1000Action.action_name: ExecutarConectorG1000Action(),
    FixarGFC700TaskbarAction.action_name: FixarGFC700TaskbarAction(),
    fixar_g1000_area_trabalho.action_name: fixar_g1000_area_trabalho(),
    salvarConfiguracoes.action_name: salvarConfiguracoes(),
    RespondeTextoAction.action_name: RespondeTextoAction(),
}

print(ACTIONS_REGISTRY.keys())