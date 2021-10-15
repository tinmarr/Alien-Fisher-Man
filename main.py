import rubato as rb
import random

game = rb.Game()

mainScene = rb.Scene()
game.scenes.add(mainScene, "main")

player = rb.RigidBody({
    "hitbox": rb.Polygon.generate_rect(32, 32),
    "pos": rb.Vector(50, 50),
    "debug": True
})


fish = rb.Group()
mainScene.add(fish)

def gen_fish(top_left: rb.Vector, bottom_right: rb.Vector, amt):
    fish_imgs = [""]
    for _ in range(amt):
        fish.add(rb.RigidBody({
                "img": random.choice(fish_imgs),
                "hitbox": rb.Polygon.generate_rect(16, 16),
                "pos": random.randint(top_left.x, bottom_right.x), random.randint(top_left.y, bottom_right.y),
                "debug": True
            })
