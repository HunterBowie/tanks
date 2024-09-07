from assets import assets
from camera import Camera
from constants import BulletSize, ExplosionSize, TankColor
from world.bullet import Bullet
from world.tanks.turrets.turret import Turret


class WideTurret(Turret):
    DEFAULT_BULLET_SPEED = 4
    DEFAULT_FIRING_DELAY = .8

    def __init__(self, pivot_pos: tuple[int, int], color: TankColor, camera: Camera) -> None:
        self.color = color
        super().__init__(
            pivot_pos, assets.images.turrets[f"{color.name.lower()}_turret_wide"], camera)

    def _fire(self, tank_id: int) -> Bullet:
        return Bullet(self.launch_pos, self.color, BulletSize.WIDE, ExplosionSize.LARGE, 0, self.angle, self.bullet_speed, tank_id, self.camera)
