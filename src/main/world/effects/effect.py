from ..entity import Entity


class Effect(Entity):
    rendering_layer: int

    def is_finished(self) -> bool:
        ...
