import rubato as rb
import random, webbrowser

rb.init()
rb.utils.Display.set_window_name("yo mama's an Alien")

# design menu

menu = rb.Scene()
rb.game.scenes.add(menu, "menu")
rb.game.scenes.set("menu")
title = rb.sprite.Text({
    "pos": (rb.game.window_size / 2).round(0) - rb.Vector(0, rb.game.window_height / 4),
    "text": "if yo mama was an alien... she would be followed by fish",
    "size": 24,
})
play = rb.sprite.Text({
    "pos": (rb.game.window_size / 2).round(0),
    "text": "SPACE to Play",
    "size": 20,
})


def play_update():
    if rb.Input.is_pressed("SPACE"):
        rb.game.scenes.set("level1")


play.update = play_update
interested = rb.sprite.Text({
    "pos": (rb.game.window_size / 2 - rb.Vector.UP * (play.size * 1.5)).round(0),
    "text": "Interested in who we are? press \'L\'",
    "size": 20,
})


def interested_update():
    if rb.Input.is_pressed("l"):
        webbrowser.open("https://github.com/tinmarr/Alien-Fisher-Man")


interested.update = interested_update
menu.add(title)
menu.add(play)
menu.add(interested)

# design level1

level1 = rb.Scene()
rb.game.scenes.add(level1, "level1")
# game.scenes.set("level1")

player = rb.RigidBody({
    "friction": rb.Vector(0.95, 1),
    "hitbox": rb.Polygon.generate_rect(28 * 2, 15 * 2),
    "pos": rb.Vector(50, 50),
    "debug": True,
    "img": "img/ufo.png",
    "scale": rb.Vector(2, 2),
    "col_type": rb.COL_TYPE.ELASTIC,
})


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
barriers = [floor, wall_left, wall_right, ceiling]
for barrier in barriers: level1.add(barrier)  # TODO: add barriers as a group if Group collision already working
bg = rb.Image("img/ocean.png", pos=rb.Vector(0, int(height / 4)))
bg.scale_abs(rb.Vector(width, int(height / 2)))
bg.image.set_colorkey((200, 200, 200))
bg.image.set_alpha(100)

fish = rb.Group()
level1.add(fish)


def player_update():
    player.physics()

    if rb.Input.is_pressed("b"):
        for fishy in fish.sprites:
            fishy.acceleration = (rb.Vector.from_radial(player.pos.direction_to(fishy.pos),
                                                        player.pos.distance_to(fishy.pos) * 10 * rb.Time.delta_time(
                                                            "sec")))
            # fishy.velocity.clamp(rb.Vector.ONE * -100, rb.Vector.ONE * 100)
            # fishy.acceleration.clamp(rb.Vector.ONE * -2, rb.Vector.ONE * 2)

    if rb.Input.is_pressed("w"):
        player.acceleration.y = -400
    elif rb.Input.is_pressed("s"):
        player.acceleration.y = 400
    else:
        player.acceleration.y = 0

    if rb.Input.is_pressed("a"):
        player.acceleration.x = -500
    elif rb.Input.is_pressed("d"):
        player.acceleration.x = 500
    else:
        player.acceleration.x = 0

    fish.collide_rb(player)
    for barrier in barriers:
        fish.collide_rb(barrier)
        player.collide(barrier)
    fish.collide_self()

    level1.camera.pos = level1.camera.pos.lerp(player.pos - rb.game.window_size / 2, 0.05).round(0)
    level1.camera.pos.clamp(rb.Vector(-width / 2, -height / 2), rb.Vector(width / 2, height / 2) - rb.game.window_size)
    # TODO: support window_resizing and camera zoom in and out


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


gen_fish_clusters(rb.Vector(-width / 2, 0), rb.Vector(width / 2, height / 2), 20)
# TODO: 20 is plenty fish but anything more and it lags out (try 50). We need to not draw stuff off screen and more optimizations
rb.begin()
