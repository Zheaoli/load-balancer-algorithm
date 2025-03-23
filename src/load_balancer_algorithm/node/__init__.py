import dataclasses


@dataclasses.dataclass
class Node:
    host: str = ""
    port: int = 0
    node_available: bool = True
    weight: int = 0
    current_weight: int = 0
    connections: int = 0

    @property
    def available(self) -> bool:
        return self.node_available

    def __str__(self) -> str:
        return f"{self.host}:{self.port}"
