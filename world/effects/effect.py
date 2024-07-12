from world.world_entity import WorldEntity


class Effect(WorldEntity):
    def is_dead(self) -> bool:
        ...
