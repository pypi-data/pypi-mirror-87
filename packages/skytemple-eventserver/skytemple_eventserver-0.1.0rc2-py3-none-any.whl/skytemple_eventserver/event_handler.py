#  Copyright 2020 Parakoopa
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.
import json

from skytemple_eventserver.websocket_server import WebsocketServer

from skytemple.core.abstract_module import AbstractModule
from skytemple.core.events.abstract_listener import AbstractListener
from skytemple.core.module_controller import AbstractController
from skytemple.core.rom_project import RomProject


class EventHandler(AbstractListener):
    def __init__(self, server: WebsocketServer):
        self.server = server

    def on(self, event_name: str, *args, **kwargs):
        self.server.send_message_to_all(json.dumps({
            'event': event_name,
            'args': [self._stringify(a) for a in args],
            'kwargs': {k: self._stringify(v) for k, v in kwargs.items()},
        }))

    @classmethod
    def _stringify(cls, obj):
        if isinstance(obj, int):
            return obj
        if isinstance(obj, dict):
            return {k: cls._stringify(v) for k, v in obj.items()}
        if isinstance(obj, list) or isinstance(obj, set) or isinstance(obj, tuple):
            return [cls._stringify(a) for a in obj]
        if isinstance(obj, RomProject):
            return obj.filename
        if isinstance(obj, AbstractModule):
            return obj.__class__.__name__
        if isinstance(obj, AbstractController):
            return obj.__class__.__name__
        return str(obj)
