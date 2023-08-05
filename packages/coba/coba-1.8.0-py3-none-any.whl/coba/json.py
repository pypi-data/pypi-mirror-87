"""The json module contains classes for serializing and deserializing coba classes"""

import json
import inspect

from abc import ABC, abstractmethod
from typing import Dict, Any

class JsonSerializable(ABC):
    """An interface for coba types that can convert to and from json.
    
    The built in JSON decoder/encoder expects objects. Therefore our interface
    merely does the work necessary to get coba types into formats that the built
    in encoder/decoder can work with and doesn't actually convert all the way to
    and from json text itself.
    """
    
    @abstractmethod
    def __to_json__(self) -> Dict[str,Any]:
        ...

    @staticmethod
    @abstractmethod
    def __from_json__(obj: Dict[str,Any]) -> Any:
        ...

class CobaJsonEncoder(json.JSONEncoder):
    """A json encoder that works with JsonSerializable to encode coba types."""
    
    def default(self, obj):
        """Use JsonSerializable to convert coba types to json."""

        if hasattr(obj, "__to_json__") and callable(obj.__to_json__):

            all_bases = [c.__name__ for c in inspect.getmro(obj.__class__)]
            json_obj  = obj.__to_json__()

            JS_index = all_bases.index('JsonSerializable') if 'JsonSerializable' in all_bases else -1

            json_obj['__type__'] = all_bases if JS_index == -1 else all_bases[0] if JS_index == 1 else all_bases[0:JS_index]

            return json_obj

        return super().default(obj)

class CobaJsonDecoder:
    """A json decoder that works with JsonSerializable to decode coba types."""

    def __init__(self, *args, types=[], **kwargs):
        """Instantiate a CobaJsonDecoder."""
        
        self._decoder = json.JSONDecoder(object_hook=self.object_hook, *args, **kwargs)

        # Because of circular imports we can't actually import COBA types directly
        # since many coba classes already import CobaJsonDecoder themselves. So, 
        # we instead rely on calling modules to provide us with all types that we 
        # need at any given time to decode a given json string with coba types.
        from coba.statistics import StatisticalEstimate

        self._known_types = { 
            "StatisticalEstimate": StatisticalEstimate,
        }

        for tipe in types: self._known_types[tipe.__name__] = tipe

    def decode(self, json_txt: str) -> Any:
        """Decode json text into objects.
        
        Args:
            json_txt: The json text we wish to decode into objects.
        """
        
        return self._decoder.decode(json_txt)

    def object_hook(self, json_obj: Dict[str,Any]) -> Any:

        __type__  = json_obj.get('__type__', [])
        __types__ = [__type__] if isinstance(__type__,str) else __type__

        for __type__ in __types__:
            if __type__ in self._known_types:
                return self._known_types[__type__].__from_json__(json_obj)

        return json_obj