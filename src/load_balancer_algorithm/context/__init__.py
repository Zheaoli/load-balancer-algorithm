import dataclasses


@dataclasses.dataclass
class RequestContext:
    url: str = ""
