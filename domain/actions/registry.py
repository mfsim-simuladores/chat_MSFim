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
    CopiarPluginsG1000Action.action_name: CopiarPluginsG1000Action()
}

print(ACTIONS_REGISTRY.keys())