import rubato as rb

externals = {}

def init(**kwargs):
    global externals
    externals = kwargs

player = rb.RigidBody({
    "friction": rb.Vector(0.95, 1),
    "hitbox": rb.Polygon.generate_rect(28 * 2, 15 * 2),
    "pos": rb.Vector(50, 50),
    "debug": True,
    "img": "img/ufo.png",
    "scale": rb.Vector(2, 2),
    "col_type": rb.COL_TYPE.ELASTIC,
})

def player_update():
    player.physics()

    if rb.Input.is_pressed("b"):
        for fishy in externals["fish"].sprites:
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

    externals["fish"].collide_rb(player)

    externals["barriers"].collide_rb(player)
    externals["barriers"].collide_group(externals["fish"])

    externals["fish"].collide_self()

    externals["level1"].camera.pos = externals["level1"].camera.pos.lerp(player.pos - rb.game.window_size / 2, 0.05).round(0)
    externals["level1"].camera.pos.clamp(rb.Vector(-externals["width"] / 2, -externals["height"] / 2), rb.Vector(externals["width"] / 2, externals["height"] / 2) - rb.game.window_size)
    # TODO: support window_resizing and camera zoom in and out


player.update = player_update