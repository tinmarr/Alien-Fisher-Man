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


def empty_update():
    if rb.Input.is_pressed("SPACE"):
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