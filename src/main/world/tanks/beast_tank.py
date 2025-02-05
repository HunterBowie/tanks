from ...assets import assets
from ...camera import Camera
from ...constants import TankTrackSize
from ..bullet import Bullet
from ..tanks.tank import Tank
from ..tanks.turrets import BasicTurret
from ..tanks.turrets.blitz_turret import BlitzTurret
from ..tanks.turrets.seeking_turret import SeekingTurret


class BeastTank(Tank):
    DEFAULT_SPEED = 3
    MAX_HEALTH = 100

    LEFT_TURRET_OFFSET = -20, -10
    RIGHT_TURRET_OFFSET = 20, -10
    BACK_TURRET_OFFSET = 0, 45

    def __init__(self, pos: tuple[int, int], camera: Camera) -> None:
        super().__init__(
            pos, assets.images.tanks[f"special_tank_body_3"], TankTrackSize.DOUBLE, camera)
        self.attach_turret(BlitzTurret(
            (pos[0]+self.LEFT_TURRET_OFFSET[0], pos[1]+self.LEFT_TURRET_OFFSET[1]), False, camera))
        self.attach_turret(BlitzTurret(
            (pos[0]+self.RIGHT_TURRET_OFFSET[0], pos[1]+self.RIGHT_TURRET_OFFSET[1]), True, camera))
        self.attach_turret(SeekingTurret((
            pos[0]+self.BACK_TURRET_OFFSET[0], pos[1]+self.BACK_TURRET_OFFSET[1]), camera))
