from typing import List, Optional, Dict

from .constants import Vec2, Millis


class DialogChoice:
    def __init__(self, text: str, leads_to_id: str):
        self.text = text
        self.leads_to_id = leads_to_id


class NodeGraphics:

    def __init__(self, animation_id: Optional[str] = None, image_ids: Optional[List[str]] = None,
        offset: Optional[Vec2] = None, screen_shake: Optional[Millis] = None,
        instant_text: bool = False):
        self.animation_id = animation_id
        self.image_ids = image_ids
        self.offset: Vec2 = offset or (0, 0)
        self.screen_shake = screen_shake
        self.instant_text = instant_text


class DialogNode:
    def __init__(self, node_id: str, text: str, choices: List[DialogChoice], graphics: Optional[NodeGraphics] = None,
        sound_id: Optional[str] = None):
        if not node_id:
            raise ValueError("Invalid node config (missing ID)")
        self.node_id = node_id
        self.text = text
        self.choices = choices
        self.graphics = graphics
        self.sound_id = sound_id


class DialogGraph:
    """
    A graph representation of a dialog

    This class is very central. One instance represents a full dialog. It keeps track of where you are as you progress
    through a dialog.
    """
    def __init__(self, root_node_id: str, nodes: List[DialogNode], title: Optional[str] = None,
        background_image_id: Optional[str] = None):
        self.title = title
        self.background_image_id = background_image_id
        self._nodes_by_id: Dict[str, DialogNode] = {}
        self._active_node_id = root_node_id
        for node in nodes:
            node_id = node.node_id
            if node_id in self._nodes_by_id:
                raise ValueError(f"Duplicate node ID found: {node_id}")
            self._nodes_by_id[node_id] = node

        for node in nodes:
            for choice in node.choices:
                if choice.leads_to_id not in self._nodes_by_id:
                    raise ValueError(
                        f"Dialog choice leading to missing node: {choice.leads_to_id}")

        if root_node_id not in self._nodes_by_id:
            raise ValueError(f"No node found with ID: {root_node_id}")

    def current_node(self) -> DialogNode:
        return self._nodes_by_id[self._active_node_id]

    def make_choice(self, choice_index: int):
        node = self._nodes_by_id[self._active_node_id]
        self._active_node_id = node.choices[choice_index].leads_to_id

    def nodes(self) -> List[DialogNode]:
        """ Return the nodes of this graph as a list. Should not needed for normal usage,
         but is used when visualizing the graph with graphviz. """
        return list(self._nodes_by_id.values())

    def __repr__(self):
        return str(self.__dict__)
