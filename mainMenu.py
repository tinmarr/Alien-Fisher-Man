import rubato as rb
import webbrowser


menu = rb.Scene()
rb.game.scenes.add(menu, "menu")

title = rb.Text({
    "pos": (rb.game.window_size / 2).round(0) - rb.Vector(0, rb.game.window_height / 4),
    "text": "if yo mama was an alien... she would be followed by fish",
    "size": 24,
})
play = rb.Text({
    "pos": (rb.game.window_size / 2).round(0),
    "text": "SPACE to Play",
    "size": 20,
})
empty = rb.sprite.Empty()
width, height = 2000, 1000
bg = rb.Image("img/ocean.png", pos=rb.Vector(0, height // 4), z_index=-1)
bg.scale_abs(rb.Vector(width, height // 2))
bg.image.set_colorkey((200, 200, 200))
bg.image.set_alpha(100)
menu.add(bg)


def empty_update():
    if rb.Input.is_pressed("SPACE"):
        pos = rb.Vector(0, -200)
        # TODO: camera not moving
        while (pos - menu.camera.pos).magnitude > 1:
            menu.camera.pos = menu.camera.pos.lerp(pos - rb.game.window_size / 2, 1.5 * rb.Time.delta_time("sec")).round(0)

        rb.game.scenes.set("level1")


empty.update = empty_update
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
menu.add(empty)
menu.add(interested)
