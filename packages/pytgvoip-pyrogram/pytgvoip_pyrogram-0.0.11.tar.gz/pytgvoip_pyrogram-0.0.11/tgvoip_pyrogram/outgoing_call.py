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
import asyncio

import hashlib
from random import randint
from typing import Union

import pyrogram
from pyrogram.raw import functions, types

from tgvoip import CallState
from tgvoip.utils import i2b, b2i, calc_fingerprint
from tgvoip_pyrogram.base_call import VoIPCallBase


class VoIPOutgoingCall(VoIPCallBase):
    is_outgoing = True

    def __init__(self, user_id: Union[int, str], *args, **kwargs):
        super(VoIPOutgoingCall, self).__init__(*args, **kwargs)
        self.user_id = user_id
        self.call_accepted_handlers = []

    async def request(self):
        self.update_state(CallState.REQUESTING)
        self.peer = await self.client.resolve_peer(self.user_id)
        await self.get_dhc()
        self.a = randint(2, self.dhc.p-1)
        self.g_a = pow(self.dhc.g, self.a, self.dhc.p)
        self.g_a_hash = hashlib.sha256(i2b(self.g_a)).digest()
        self.call = (await self.client.send(functions.phone.RequestCall(
            user_id=self.peer,
            random_id=randint(0, 0x7fffffff - 1),
            g_a_hash=self.g_a_hash,
            protocol=self.get_protocol(),
        ))).phone_call
        self.update_state(CallState.WAITING)

    def on_call_accepted(self, func: callable) -> callable:  # the call was accepted by other party
        self.call_accepted_handlers.append(func)
        return func

    async def process_update(self, _, update, users, chats) -> None:
        await super(VoIPOutgoingCall, self).process_update(_, update, users, chats)
        if isinstance(self.call, types.PhoneCallAccepted) and not self.auth_key:
            await self.call_accepted()
            raise pyrogram.StopPropagation
        raise pyrogram.ContinuePropagation

    async def call_accepted(self) -> None:
        for handler in self.call_accepted_handlers:
            asyncio.iscoroutinefunction(handler) and asyncio.ensure_future(handler(self), loop=self.client.loop)

        self.update_state(CallState.EXCHANGING_KEYS)
        await self.get_dhc()
        self.g_b = b2i(self.call.g_b)
        self.check_g(self.g_b, self.dhc.p)
        self.auth_key = pow(self.g_b, self.a, self.dhc.p)
        self.key_fingerprint = calc_fingerprint(self.auth_key_bytes)
        self.call = (await self.client.send(functions.phone.ConfirmCall(
            key_fingerprint=self.key_fingerprint,
            peer=types.InputPhoneCall(id=self.call.id, access_hash=self.call_access_hash),
            g_a=i2b(self.g_a),
            protocol=self.get_protocol(),
        ))).phone_call
        await self._initiate_encrypted_call()
