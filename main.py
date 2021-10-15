import rubato as rb
import random

game = rb.Game()
rb.utils.Display.set_window_name("yo mama's an Alien")

menu = rb.Scene()
game.scenes.add(menu, "menu")
game.scenes.set("menu")
title = rb.sprite.Text({
    "pos": (game.window_size / 2).round(0) - rb.Vector(0, game.window_height/4),
    "text": "if yo mama was an alien... she would be followed by fish",
    "size": 24,
})
play = rb.sprite.Text({
    "pos": (game.window_size / 2).round(0),
    "text": "SPACE to Play",
    "size": 20,
})
def play_update():
    if rb.Input.is_pressed("SPACE"):
        game.scenes.set("level1")
play.update = play_update
menu.add(title)
menu.add(play)

bg = rb.Image("", rb.Vector(50, 10), rb.Vector(20, 20), -1)


level1 = rb.Scene()
game.scenes.add(level1, "level1")
# game.scenes.set("level1")

player = rb.RigidBody({
    "friction": rb.Vector(0.95, 1),
    "hitbox": rb.Polygon.generate_rect(28*2, 15*2),
    "pos": rb.Vector(50, 50),
    "debug": True,
    "img": "img/ufo.png",
    "scale": rb.Vector(2,2),
    "col_type": rb.COL_TYPE.ELASTIC,
})


floor = rb.RigidBody({
    "hitbox": rb.Polygon.generate_rect(600, 1),
    "pos": rb.Vector(300, 400),
    "debug": True,
    "img": "empty",
    "gravity": 0,
})
bg = rb.Image("", rb.Vector(50, 10), rb.Vector(20, 20), -1)
level1.add(floor)

fish = rb.Group()
level1.add(fish)

def player_update():
    player.physics()

    if rb.Input.is_pressed("b"):
        for fishy in fish.sprites:
            fishy.acceleration = (rb.Vector.from_radial(player.pos.direction_to(fishy.pos), player.pos.distance_to(fishy.pos)*10*rb.Time.delta_time("sec")))
            fishy.velocity.clamp(rb.Vector.ONE * -100, rb.Vector.ONE * 100)
            fishy.acceleration.clamp(rb.Vector.ONE * -2, rb.Vector.ONE * 2)

    if rb.Input.is_pressed("w"):
        player.acceleration.y = -400
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


    level1.camera.pos = level1.camera.pos.lerp(player.pos - game.window_size / 2, 0.05).round(0)
    print(level1.camera.pos)


player.update = player_update

level1.add(player)
level1.add(bg)



fish = rb.Group()
level1.add(fish)

def gen_fish(top_left: rb.Vector, bottom_right: rb.Vector, amt):
    fish_imgs = ["img/greenfish.png", "img/whitefish.png"]
    for _ in range(amt):
        scale = random.randint(1, 3)
        rotation = random.randint(0, 360)
        fish_ = rb.RigidBody({
                "img": random.choice(fish_imgs),
                "hitbox": rb.Polygon.generate_rect(20*scale, 11*scale),
                "pos": rb.Vector(random.randint(top_left.x, bottom_right.x), random.randint(top_left.y, bottom_right.y)),
                "debug": True,
                "gravity": 0,
                "col_type": rb.COL_TYPE.STATIC,
                "scale": rb.Vector(scale,scale),
                "rotation": rotation,
            })
        fish_.hitbox.rotation = -rotation
        fish.add(fish_)

gen_fish(rb.Vector(), rb.Vector(600, 400), 20)
game.begin()
