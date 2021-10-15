import rubato as rb

game = rb.Game()

mainScene = rb.Scene()
game.scenes.add(mainScene, "main")

player = rb.RigidBody({
    "hitbox": rb.Polygon.generate_rect(32, 32),
    "pos": rb.Vector(50, 50),
    "debug": True
})