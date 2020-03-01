# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, List

from dial_core.utils.log import DEBUG, log_on_end

if TYPE_CHECKING:
    from .node import Node


class Scene:
    def __init__(self):
        self.__nodes: List["Node"] = []

    @property
    def nodes(self) -> List["Node"]:
        """Returns all the nodes on the scene."""
        return self.__nodes

    @log_on_end(DEBUG, "{node} added to the scene.")
    def add_node(self, node: "Node"):
        """Adds a new node to the scene."""
        self.nodes.append(node)