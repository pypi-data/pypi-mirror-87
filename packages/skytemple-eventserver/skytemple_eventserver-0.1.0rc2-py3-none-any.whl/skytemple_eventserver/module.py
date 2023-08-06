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
import logging
from threading import Thread

from skytemple_eventserver.websocket_server import WebsocketServer

from skytemple.core.abstract_module import AbstractModule
from skytemple.core.events.manager import EventManager
from skytemple.main import SKYTEMPLE_LOGLEVEL
from skytemple_eventserver.event_handler import EventHandler

logger = logging.getLogger(__name__)
DEFAULT_PORT = 45546


class EventThread(Thread):
    daemon = True

    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        try:
            self.server.serve_forever()
        except (KeyboardInterrupt, SystemExit):
            self.server.server_close()
            logger.info("Eventserver terminated.")
        except BaseException as e:
            logger.error(str(e), exc_info=e)


class EventserverModule(AbstractModule):
    @classmethod
    def depends_on(cls):
        return []

    @classmethod
    def sort_order(cls):
        return 0  # n/a

    @classmethod
    def load(cls):
        try:
            # Start the server
            server = WebsocketServer(port=DEFAULT_PORT, loglevel=SKYTEMPLE_LOGLEVEL)
            EventThread(server).start()
            # Register the event handler to the event manager
            EventManager.instance().register_listener(EventHandler(server))
        except BaseException as e:
            logger.error(f"Failed loading websocket eventserver", exc_info=e)

    def load_tree_items(self, item_store, root_node):
        pass  # n/a

    def __init__(self, *args):
        pass
