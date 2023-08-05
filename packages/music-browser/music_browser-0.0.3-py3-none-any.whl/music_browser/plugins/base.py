import abc
from typing import List, Set
from ..models import SimpleTrack


class Plugin(abc.ABC):
    @abc.abstractproperty
    def known_fields(self) -> Set[str]:
        raise NotImplementedError("You must implement known_fields property of your Plugin")

    @abc.abstractmethod
    def query(self, query_params, query_fields) -> dict:
        raise NotImplementedError("You must implement query method of your Plugin")

    @abc.abstractmethod
    def search(self, query: str) -> List[SimpleTrack]:
        raise NotImplementedError("You must implement search method to use a plugin as search_plugin...")
