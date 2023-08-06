# Copyright 2020 Josh Pieper, jjp@pobox.com.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Classes and functions for interoperating with the moteus brushless
controller."""

__all__ = [
    'Fdcanusb', 'Router', 'Controller', 'Register',
    'Mode', 'QueryResolution', 'PositionResolution', 'Command',
    'Pi3HatRouter',
]


from moteus.command import Command
from moteus.fdcanusb import Fdcanusb
from moteus.router import Router
from moteus.moteus import (Controller, Register, Mode, QueryResolution, PositionResolution, set_router_factory)
from moteus.pi3hat_router import Pi3HatRouter
import moteus.moteus

_global_pi3hat = None

def _pi3hat_get_singleton():
    global _global_pi3hat

    if _global_pi3hat:
        return _global_pi3hat

    _global_pi3hat = Pi3HatRouter()
    return _global_pi3hat

set_router_factory(_pi3hat_get_singleton)


VERSION = "0.1.2"
