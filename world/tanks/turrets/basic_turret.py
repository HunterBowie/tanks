
from assets import assets
from camera import Camera
from constants import BulletSize, TankColor
from world.bullet import Bullet
from world.tanks.turrets.turret import Turret


class BasicTurret(Turret):
    DEFAULT_BULLET_SPEED = 4
    DEFAULT_FIRING_DELAY = .2

    def __init__(self, pivot_pos: tuple[int, int], color: TankColor, camera: Camera) -> None:
        self.color = color
        super().__init__(
            pivot_pos, assets.images.tanks[f"{color.name.lower()}_turret_basic"], camera)

    def _fire(self, tank_id: int) -> Bullet:
        return Bullet(self.launch_pos, self.color, BulletSize.BASIC, self.angle, self.bullet_speed, tank_id, self.camera)
