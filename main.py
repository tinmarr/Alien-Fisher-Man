import rubato as rb

rb.init()

import mainMenu, level1

rb.utils.Display.set_window_name("yo mama's an Alien")

rb.game.scenes.set(mainMenu.menu.id)

rb.begin()
