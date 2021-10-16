import rubato as rb
import random, player

level1 = rb.Scene()
rb.game.scenes.add(level1, "level1")

def gen_barrier(hitbox, pos):
    temp = rb.RigidBody({
        "hitbox": hitbox,
        "pos": pos,
        "debug": True,
        "img": "empty",
        "gravity": 0,
    })
    return temp


width = 2000
height = 1000

floor = gen_barrier(rb.Polygon.generate_rect(width, 1), rb.Vector(0, height / 2))
wall_left = gen_barrier(rb.Polygon.generate_rect(1, height), rb.Vector(-width / 2, 0))
wall_right = gen_barrier(rb.Polygon.generate_rect(1, height), rb.Vector(width / 2, 0))
ceiling = gen_barrier(rb.Polygon.generate_rect(width, 1), rb.Vector(0, -height / 2))
barriers = rb.Group()
barriers.sprites = [floor, wall_left, wall_right, ceiling]

level1.add(barriers) # This line is actually useless. We can delete it later but this is so that the hitboxes are rendered. Collision still works without

bg = rb.Image("img/ocean.png", pos=rb.Vector(0, int(height / 4)))
bg.scale_abs(rb.Vector(width, int(height / 2)))
bg.image.set_colorkey((200, 200, 200))
bg.image.set_alpha(100)

fish = rb.Group()
level1.add(fish)

level1.add(bg)

fish = rb.Group()
level1.add(fish)


def gen_fish(top_left: rb.Vector, bottom_right: rb.Vector, amt):
    fish_imgs = ["img/greenfish.png", "img/whitefish.png"]
    for _ in range(amt+1):
        scale = random.randint(1, 3)
        rotation = random.randint(0, 360)
        fish_ = rb.RigidBody({
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

player.init(width=width, height=height, level1=level1, barriers=barriers, fish=fish)
level1.add(player.player)


gen_fish_clusters(rb.Vector(-width / 2, 0), rb.Vector(width / 2, height / 2), 20)