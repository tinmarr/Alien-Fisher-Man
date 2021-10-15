import rubato as rb
import random

game = rb.Game()

mainScene = rb.Scene()
game.scenes.add(mainScene, "main")
game.scenes.set("main")

player = rb.RigidBody({
    "friction": rb.Vector(0.95, 1),
    "hitbox": rb.Polygon.generate_rect(32, 16),
    "pos": rb.Vector(50, 50),
    "debug": True,
    "img": "",
    "col_type": rb.COL_TYPE.ELASTIC,
})

floor = rb.RigidBody({
    "hitbox": rb.Polygon.generate_rect(600, 1),
    "pos": rb.Vector(300, 400),
    "debug": True,
    "img": "empty",
    "gravity": 0,
})
bg = rb.Image("", rb.Vector(50, 10), scale_factor=rb.Vector(20, 20))
mainScene.add(floor)

fish = rb.Group()
mainScene.add(fish)

def player_update():
    player.physics()

    if rb.Input.is_pressed("b"):
        pass
    if rb.Input.is_pressed("w"):
        player.acceleration.y = -500
    else:
        player.acceleration.y = 0

    if rb.Input.is_pressed("a"):
        player.acceleration.x = -500
    elif rb.Input.is_pressed("d"):
        player.acceleration.x = 500
    else:
        player.acceleration.x = 0

    fish.collide_rb(player)
    fish.collide_rb(floor)
    player.collide(floor)
    fish.collide_self()


    mainScene.camera.pos = mainScene.camera.pos.lerp(player.pos - game.window_size / 2, 0.05).round(0)
    print(mainScene.camera.pos)


player.update = player_update

mainScene.add(player)
mainScene.add(bg)



fish = rb.Group()
mainScene.add(fish)

def gen_fish(top_left: rb.Vector, bottom_right: rb.Vector, amt):
    fish_imgs = ["img/greenfish.png", "img/whitefish.png"]
    for _ in range(amt):
        fish.add(rb.RigidBody({
                "img": random.choice(fish_imgs),
                "hitbox": rb.Polygon.generate_rect(16, 16),
                "pos": rb.Vector(random.randint(top_left.x, bottom_right.x), random.randint(top_left.y, bottom_right.y)),
                "debug": False,
                "gravity": 0,
                "col_type": rb.COL_TYPE.STATIC,
                "scale": rb.Vector(2,2)
            }))

gen_fish(rb.Vector(), rb.Vector(600, 400), 20)
game.begin()
