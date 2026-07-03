from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from models.activity import Activity
from models.state import State


@dataclass
class Node:

    state: State

    parent: Optional["Node"] = None

    action: Optional[Activity] = None

    g_cost: float = 0.0

    h_cost: float = 0.0

    f_cost: float = 0.0

    depth: int = 0

    def calculate_f_cost(self) -> float:

        self.f_cost = self.g_cost + self.h_cost

        return self.f_cost

    def is_root(self) -> bool:

        return self.parent is None

    def goal(self) -> bool:

        return self.state.is_goal()

    def expand(
        self,
        activity: Activity,
    ) -> "Node":

        new_state = self.state.clone()

        new_state.advance(activity)

        return Node(
            state=new_state,
            parent=self,
            action=activity,
            depth=self.depth + 1,
        )

    def path(self) -> list["Node"]:

        node = self

        result = []

        while node is not None:

            result.append(node)

            node = node.parent

        result.reverse()

        return result

    def to_dict(self):

        return {

            "depth": self.depth,

            "g_cost": self.g_cost,

            "h_cost": self.h_cost,

            "f_cost": self.f_cost,

            "action": (
                self.action.name
                if self.action
                else None
            ),

            "state": self.state.to_dict(),
        }

    def __lt__(
        self,
        other: "Node",
    ) -> bool:

        return self.f_cost < other.f_cost

    def __str__(self):

        action = (
            self.action.name
            if self.action
            else "START"
        )

        return (
            f"Node("
            f"depth={self.depth}, "
            f"action={action}, "
            f"g={self.g_cost:.2f}, "
            f"h={self.h_cost:.2f}, "
            f"f={self.f_cost:.2f})"
        )