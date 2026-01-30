import json
from datetime import datetime

def _event(
        event_type,
        title,
        message,
        action=None,
        progress=None,
        attachments=None,
        media=None,            # 🔑 NOVO
    ):
        payload = {
            "type": event_type,
            "title": title,
            "message": message,
            "action": action,
            "progress": progress,
            "timestamp": datetime.utcnow().isoformat(),
        }

        if attachments:
            payload["attachments"] = attachments

        if media:              # 🔑 NOVO
            payload["media"] = media

        return payload


class SSEEvent:

    @staticmethod
    def action(title, message, action_name=None, attachments=None):
        return _event(
            "action",
            title,
            message,
            action=action_name,
            attachments=attachments,
        )

    @staticmethod
    def log(message, title="Log"):
        return _event("log", title, message)

    @staticmethod
    def warning(message, title="Atenção"):
        return _event("warning", title, message)

    @staticmethod
    def error(title, message):
        return _event("error", title, message)

    @staticmethod
    def message(message, title=None, attachments=None, media=None):
        return _event(
            event_type="message",
            title=title,
            message=message,
            attachments=attachments,
            media=media,
        )

    @staticmethod
    def progress(title, message, progress, action_name=None):
        return _event(
            "progress",
            title,
            message,
            action=action_name,
            progress=progress,
        )


    @staticmethod
    def finished(action_name, message="Concluído"):
        return _event(
            "finished",
            action_name,
            message,
            action=action_name,
        )


    @staticmethod
    def question(title, message, action_name):
        return _event(
            event_type="question",
            title=title,
            message=message,
            action= action_name
        )
