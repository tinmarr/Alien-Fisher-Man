import rubato as rb

rb.init()

import mainMenu, level1

rb.utils.Display.set_window_name("yo mama's an Alien")

rb.game.scenes.set(level1.level1.id)

rb.begin()
