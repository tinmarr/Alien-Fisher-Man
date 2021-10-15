import rubato as rb

game = rb.Game()

mainScene = rb.Scene()
game.scenes.add(mainScene, "main")
game.scenes.set("main")

player = rb.RigidBody({
    "friction": rb.Vector(0.95, 1),
    "hitbox": rb.Polygon.generate_rect(32, 32),
    "pos": rb.Vector(50, 50),
    "debug": True,
    "img": "empty",
})

def player_update():
    player.physics()

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

player.update = player_update

mainScene.add(player)

game.begin()