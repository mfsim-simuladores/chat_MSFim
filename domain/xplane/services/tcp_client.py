import socket
from typing import List
from domain.xplane.entities import AircraftStatus
from domain.xplane.exceptions import XplaneConnectionError, XplaneEmptyResponse


class XPlaneTCPClient:
    def __init__(self, host="127.0.0.1", port=49005, timeout=2):
        self.host = host
        self.port = port
        self.timeout = timeout

    def get_status(self) -> AircraftStatus:
        try:
            with socket.create_connection((self.host, self.port), timeout=self.timeout) as s:
                s.sendall(b"STATUS\n")
                raw = s.recv(2048).decode("ascii", errors="ignore").strip()

        except Exception as e:
            raise XPlaneConnectionError(f"Erro na conexão TCP: {e}")

        if not raw:
            raise XPlaneEmptyResponse("Plugin retornou resposta vazia.")

        status_dict = {}
        for item in raw.split(";"):
            if "=" in item:
                k, v = item.split("=", 1)
                status_dict[k] = v

        return AircraftStatus(status_dict)

    def send_commands(self, commands: List[str]) -> None:
        try:
            with socket.create_connection((self.host, self.port), timeout=self.timeout) as s:
                for cmd in commands:
                    s.sendall((cmd + "\n").encode("ascii"))

        except Exception as e:
            raise XPlaneConnectionError(f"Falha ao enviar comandos: {e}")
