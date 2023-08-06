__version__ = "1.1.1"

import asyncio
import sys

from .field import Field, ListField
from .model import ModelMeta, Model
from .serialize import SerializableModel
from .type_cast import TypeCast

if sys.platform.startswith('win'):
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

__all__ = (
    'Field',
    'ListField',
    'SerializableModel',
    'ModelMeta',
    'Model',
    'TypeCast'
)
