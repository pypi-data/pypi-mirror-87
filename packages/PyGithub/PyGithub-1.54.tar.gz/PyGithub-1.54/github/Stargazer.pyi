from datetime import datetime
from typing import Any, Dict

from github.GithubObject import NonCompletableGithubObject
from github.NamedUser import NamedUser

class Stargazer(NonCompletableGithubObject):
    def __repr__(self) -> str: ...
    def _initAttributes(self) -> None: ...
    def _useAttributes(self, attributes: Dict[str, Any]) -> None: ...
    @property
    def starred_at(self) -> datetime: ...
    @property
    def user(self) -> NamedUser: ...
