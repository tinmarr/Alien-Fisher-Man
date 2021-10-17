import rubato as rb
import random, player

level1 = rb.Scene()
level1.camera.pos = rb.Vector(0, 150)
rb.game.scenes.add(level1, "level1")

score = 0

score_text = rb.sprite.Text({
    "text": str(score),
    "pos": rb.Vector(50, 50),
    "static": True
})
level1.add(score_text)

def increment_score():
    global score
    score += 1
    score_text.text = str(score)
    score_text.remake_image()

def gen_barrier(hitbox, pos):
    temp = rb.RigidBody({
        "hitbox": hitbox,
        "pos": pos,
        "debug": True,
        "img": "empty",
        "gravity": 0,
    })
    temp.in_frame = True
    return temp


width = 2000
height = 1000

floor = gen_barrier(rb.Polygon.generate_rect(width, 100), rb.Vector(0, 50 + (height / 2)))
wall_left = gen_barrier(rb.Polygon.generate_rect(100, height), rb.Vector(-50 - (width / 2), 0))
wall_right = gen_barrier(rb.Polygon.generate_rect(100, height), rb.Vector(50 + (width / 2), 0))
ceiling = gen_barrier(rb.Polygon.generate_rect(width, 100), rb.Vector(0, -50 - (height / 2)))
barriers = rb.Group()
barriers.sprites = [floor, wall_left, wall_right, ceiling]

bg = rb.Image("img/ocean.png", pos=rb.Vector(0, height // 4), z_index=-1)
bg.scale_abs(rb.Vector(width, height // 2))
bg.image.set_colorkey((200, 200, 200))
bg.image.set_alpha(100)

sky = rb.Rectangle(rb.Vector(0, -height//4), rb.Vector(width, height//2), (92, 210, 242), -1)

fish = rb.Group()
level1.add(fish)

level1.add(bg)
level1.add(sky)

fish = rb.Group()
level1.add(fish)

class Fish(rb.RigidBody):
    def __init__(self, options):
        super().__init__(options)
        self.time_in_beam = 0

    def custom_update(self):
        if self.acceleration != rb.Vector(): print(self.acceleration)
        if not rb.Input.is_pressed("b"):
            self.acceleration = rb.Vector()

        if self.pos.y < 0:
            self.params["gravity"] = 100
            self.params["debug"] = True
        elif self.pos.y > 5:
            if self.acceleration == rb.Vector():
                self.velocity.y = 0
            self.params["gravity"] = 0


def gen_fish(top_left: rb.Vector, bottom_right: rb.Vector, amt):
    fish_imgs = ["img/greenfish.png", "img/whitefish.png"]
    for _ in range(amt+1):
        scale = random.randint(1, 3)
        rotation = random.randint(0, 360)
        fish_ = Fish({
            "img": random.choice(fish_imgs),
            "hitbox": rb.Polygon.generate_rect(20 * scale, 11 * scale),
            "pos": rb.Vector(random.randint(top_left.x, bottom_right.x), random.randint(top_left.y, bottom_right.y)),
            "gravity": 0,
            "col_type": rb.COL_TYPE.STATIC,
            "scale": rb.Vector(scale, scale),
            "rotation": rotation,
        })
        fish_.hitbox.rotation = -rotation
        fish.add(fish_)

def gen_fish_clusters(top_left: rb.Vector, bottom_right: rb.Vector, amt):
    while amt > 1:
        pos = rb.Vector(random.randint(top_left.x, bottom_right.x), random.randint(top_left.y, bottom_right.y))
        pos2 = rb.Vector(random.randint(pos.x, bottom_right.x), random.randint(pos.y, bottom_right.y))
        amt_ = random.randint(0, amt//2)
        amt -= amt_
        gen_fish(pos, pos2, amt_)

player.init(width=width, height=height, level1=level1, barriers=barriers, fish=fish, increment=increment_score)
level1.add(player.player)
level1.add(player.beam_collider)


gen_fish(rb.Vector(-width / 2, 100), rb.Vector(width / 2, height / 2), 50)
