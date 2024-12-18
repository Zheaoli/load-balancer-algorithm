import dataclasses


@dataclasses.dataclass
class Node:
    host: str = ""
    port: int = 0
    node_available: bool = True

    @property
    def available(self) -> bool:
        return self.node_available
