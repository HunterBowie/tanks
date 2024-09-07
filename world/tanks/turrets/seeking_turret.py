
from assets import assets
from camera import Camera
from constants import BulletSize, ExplosionSize, TankColor
from world.bullet import Bullet
from world.tanks.turrets.turret import Turret


class SeekingTurret(Turret):
    DEFAULT_BULLET_SPEED = 4
    DEFAULT_FIRING_DELAY = .4

    def __init__(self, pivot_pos: tuple[int, int], camera: Camera) -> None:
        super().__init__(
            pivot_pos, assets.images.turrets["seeking_turret"], camera)

    def _fire(self, tank_id: int) -> Bullet:
        return Bullet(self.launch_pos, TankColor.BLACK, BulletSize.BASIC, ExplosionSize.REGULAR, 0.05, self.angle, self.bullet_speed, tank_id, self.camera)
