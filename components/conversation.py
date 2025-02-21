from typing import Dict, List, Tuple

import yaml

from components.base_component import BaseComponent


class ConversationNode:
    def __init__(self, npc_text: str, player_text: str):
        self.npc_text = npc_text
        self.player_text = player_text
        self.next_node_ids: List[str] = []


class Conversation(BaseComponent):
    def __init__(self, path: str):
        """
        Create a new conversation from a YAML file.
        """
        super().__init__()
        self.nodes: Dict[str, ConversationNode] = {}  # store nodes by id
        self.current_node: ConversationNode  # active conversation node
        self.load_from_yaml(path)
        self.is_finished = False

    def load_from_yaml(self, path: str):
        """
        Loads the conversation structure from a YAML file and sets up node links.
        """
        with open(path, "r") as file:
            data = yaml.safe_load(file)

        # First, create all nodes
        for entry in data:
            node_id = entry["id"]
            self.nodes[node_id] = ConversationNode(
                npc_text=entry.get("npc_text", ""), player_text=entry.get("player_text", "")
            )

        # Now, link nodes
        for entry in data:
            node = self.nodes[entry["id"]]
            for child_id in entry.get("next", []):
                node.next_node_ids.append(child_id)

        # Set the root node (default to 'root')
        if "root" not in self.nodes:
            raise ValueError("Conversation must have a root node.")

        self.current_node = self.nodes["root"]

    def get_current_npc_text(self) -> str:
        """Returns what the NPC is saying in the current conversation node."""
        return self.current_node.npc_text if self.current_node else ""

    def get_responses(self) -> Tuple[Tuple[str, str], ...]:
        return tuple((i, self.nodes[i].player_text) for i in self.current_node.next_node_ids)

    def pick_response(self, response_id: str):
        self.current_node = self.nodes[response_id]
        if not self.current_node.next_node_ids:
            self.is_finished = True

    def reset(self):
        self.current_node = self.nodes["root"]
        self.is_finished = False
