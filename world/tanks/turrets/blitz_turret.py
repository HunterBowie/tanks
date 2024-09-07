
from assets import assets
from camera import Camera
from constants import BulletSize, ExplosionSize, TankColor
from world.bullet import Bullet
from world.tanks.turrets.turret import Turret


class BlitzTurret(Turret):
    DEFAULT_BULLET_SPEED = 10
    DEFAULT_FIRING_DELAY = .2

    LAUNCH_POS_OFFSET = 80

    def __init__(self, pivot_pos: tuple[int, int], flipped: bool, camera: Camera) -> None:
        image_name = "blitz_turret"
        if flipped:
            image_name = image_name + "_flipped"
        super().__init__(
            pivot_pos, assets.images.turrets[image_name], camera)

    def _fire(self, tank_id: int) -> Bullet:
        return Bullet(self.launch_pos, TankColor.BLACK, BulletSize.MINI, ExplosionSize.SMALL, 0.0, self.angle, self.bullet_speed, tank_id, self.camera)
