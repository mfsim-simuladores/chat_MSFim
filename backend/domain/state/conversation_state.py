from typing import List, Optional, Dict


class ConversationState:
    def __init__(self):
        self.reset()

    # =========================
    # CORE RESET
    # =========================

    def reset(self):
        self.wizard: Optional[Dict] = None
        self.active_wizard_id: Optional[str] = None
        self.wizard_steps: List[Dict] = []
        self.wizard_index: int = 0

        self.pending_action: Optional[str] = None
        self._awaiting_confirmation = False
        self._awaiting_ok = False

        self._step_sent = False
        self.just_started = False

    # =========================
    # WIZARD CONTROL
    # =========================

    def start_wizard(self, wizard_def: Dict):
        self.wizard = wizard_def
        self.active_wizard_id = wizard_def.get("id")
        self.wizard_steps = wizard_def.get("steps", [])
        self.wizard_index = 0

        self.pending_action = None
        self._awaiting_confirmation = False
        self._awaiting_ok = False
        self._step_sent = False

        self.just_started = True

    def stop_wizard(self):
        self.reset()

    def wizard_running(self) -> bool:
        return self.wizard is not None

    def current_step(self) -> Optional[Dict]:
        if not self.wizard_running():
            return None

        if self.wizard_index >= len(self.wizard_steps):
            return None

        return self.wizard_steps[self.wizard_index]

    # =========================
    # STEP NAVIGATION
    # =========================

    def can_go_back(self) -> bool:
        return self.wizard_index > 0

    def go_back(self):
        if self.wizard_index > 0:
            self.wizard_index -= 1
            self._step_sent = False

    def advance_step(self):
        self.wizard_index += 1

        self._awaiting_confirmation = False
        self._awaiting_ok = False
        self._step_sent = False

        if self.wizard_index >= len(self.wizard_steps):
            self.reset()

    # =========================
    # CONFIRMATION / OK FLOW
    # =========================

    def start_confirmation(self, action_name: str):
        self.pending_action = action_name
        self._awaiting_confirmation = True
        self._awaiting_ok = False

    def consume_confirmation(self):
        action = self.pending_action
        self.pending_action = None
        self._awaiting_confirmation = False
        return action

    def expect_confirmation(self):
        self._awaiting_confirmation = True
        self._awaiting_ok = False

    def expect_ok(self):
        self._awaiting_ok = True
        self._awaiting_confirmation = False

    def awaiting_confirmation(self) -> bool:
        return self._awaiting_confirmation

    def awaiting_ok(self) -> bool:
        return self._awaiting_ok

    # =========================
    # STEP SENT CONTROL (SSE)
    # =========================

    def step_was_sent(self) -> bool:
        return self._step_sent

    def mark_step_sent(self):
        self._step_sent = True

    # =========================
    # UI
    # =========================

    def wizard_title(self) -> str:
        if not self.wizard:
            return "Instalação"
        return self.wizard.get("title", "Instalação")


conversation_state = ConversationState()
