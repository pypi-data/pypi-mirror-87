# PytgVoIP-Pyrogram - Pyrogram support module for Telegram VoIP Library for Python
# Copyright (C) 2020 bakatrouble <https://github.com/bakatrouble>
#
# This file is part of PytgVoIP.
#
# PytgVoIP is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PytgVoIP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with PytgVoIP.  If not, see <http://www.gnu.org/licenses/>.

from collections import deque
from typing import Union, List, IO

from tgvoip_pyrogram import VoIPOutgoingCall, VoIPIncomingCall, VoIPService
from tgvoip_pyrogram.base_call import VoIPCallBase


class VoIPNativeIOCallMixin(VoIPCallBase):
    def __init__(self, *args, **kwargs):
        super(VoIPNativeIOCallMixin, self).__init__(*args, **kwargs)
        self.ctrl.native_io = True

    def play(self, path: str):
        return self.ctrl.play(path)

    def play_on_hold(self, paths: List[str]):
        self.ctrl.play_on_hold(paths)

    def set_output_file(self, path: str):
        return self.ctrl.set_output_file(path)

    def clear_play_queue(self):
        self.ctrl.clear_play_queue()

    def clear_hold_queue(self):
        self.ctrl.clear_hold_queue()

    def unset_output_file(self):
        self.ctrl.unset_output_file()


class VoIPOutgoingNativeIOCall(VoIPNativeIOCallMixin, VoIPOutgoingCall):
    pass


class VoIPIncomingNativeIOCall(VoIPNativeIOCallMixin, VoIPIncomingCall):
    pass


class VoIPNativeIOService(VoIPService):
    incoming_call_class = VoIPIncomingNativeIOCall
    outgoing_call_class = VoIPOutgoingNativeIOCall
