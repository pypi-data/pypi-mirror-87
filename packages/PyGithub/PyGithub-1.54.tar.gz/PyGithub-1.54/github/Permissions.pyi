from typing import Any, Dict

from github.GithubObject import NonCompletableGithubObject

class Permissions(NonCompletableGithubObject):
    def __repr__(self) -> str: ...
    def _initAttributes(self) -> None: ...
    def _useAttributes(self, attributes: Dict[str, Any]) -> None: ...
    @property
    def admin(self) -> bool: ...
    @property
    def pull(self) -> bool: ...
    @property
    def push(self) -> bool: ...
