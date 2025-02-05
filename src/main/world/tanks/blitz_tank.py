from ...assets import assets
from ...camera import Camera
from ...constants import TankTrackSize
from ..bullet import Bullet
from ..tanks.tank import Tank
from ..tanks.turrets import BasicTurret
from ..tanks.turrets.blitz_turret import BlitzTurret
from ..tanks.turrets.seeking_turret import SeekingTurret


class BlitzTank(Tank):
    DEFAULT_SPEED = 4
    MAX_HEALTH = 100

    LEFT_TURRET_OFFSET = -20, 15
    RIGHT_TURRET_OFFSET = 20, 15

    def __init__(self, pos: tuple[int, int], camera: Camera) -> None:
        super().__init__(
            pos, assets.images.tanks[f"special_tank_body_2"], TankTrackSize.LARGE, camera)
        self.attach_turret(BlitzTurret(
            (pos[0]+self.LEFT_TURRET_OFFSET[0], pos[1]+self.LEFT_TURRET_OFFSET[1]), False, camera))
        self.attach_turret(BlitzTurret(
            (pos[0]+self.RIGHT_TURRET_OFFSET[0], pos[1]+self.RIGHT_TURRET_OFFSET[1]), True, camera))
