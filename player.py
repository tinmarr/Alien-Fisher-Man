import rubato as rb
import pygame
externals = {}

def init(**kwargs):
    global externals
    externals = kwargs

player = rb.RigidBody({
    "friction": rb.Vector(0.97, 1),
    "hitbox": rb.Polygon.generate_rect(28 * 2, 15 * 2),
    "pos": rb.Vector(50, 0),
    "debug": False,
    "img": "img/ufo.png",
    "scale": rb.Vector(2, 2),
    "col_type": rb.COL_TYPE.ELASTIC,
})

beam_collider = rb.RigidBody({
    "hitbox": rb.Polygon.generate_rect(50, 300),
    "pos": rb.Vector(50, 10),
    "debug": False,
    "img": (0, 0, 255, 127), 
    "z_index": 2
})

def fishy_accelerator(fishy):
    fishy.acceleration = rb.Vector.from_radial(player.pos.direction_to(fishy.pos),
        player.pos.distance_to(fishy.pos) * 50 * rb.Time.delta_time("sec"))


def beam_update():
    # How do you get a colliders size?
    beam_collider.pos = player.pos + rb.Vector.DOWN * (300 / 2 + 15)

    if rb.Input.is_pressed("SPACE"):
        for fishy in externals["fish"].sprites:
            if beam_collider.overlap(fishy) is not None:
                fishy.time_in_beam += rb.Time.delta_time("sec")
                darkness = pygame.Surface((fishy.image.image.get_width(), fishy.image.image.get_height()),
                                          flags=pygame.SRCALPHA)
                darkness.fill((1, 1, 1, 2))
                fishy.image.image.blit(darkness, (0, 0))
                # fishy.image.image = fishy.image.image.set_colorkey(fishy.image.image.get_at((0, 0)))
                fishy_accelerator(fishy)
                if fishy.time_in_beam > 4:
                    externals["fish"].sprites.remove(fishy)
                    externals["increment"]()


beam_collider.update = beam_update

def player_update():
    player.physics()

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

    externals["level1"].camera.pos = externals["level1"].camera.pos.lerp(player.pos - rb.game.window_size / 2, 1.5 * rb.Time.delta_time("sec")).round(0)
    externals["level1"].camera.pos.clamp(rb.Vector(-externals["width"] / 2, -externals["height"] / 2), rb.Vector(externals["width"] / 2, externals["height"] / 2) - rb.game.window_size)
    # TODO: support window_resizing and camera zoom in and out

player.update = player_update