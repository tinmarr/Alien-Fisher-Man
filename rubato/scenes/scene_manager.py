from rubato.scenes.scene import Scene


class SceneManager:
    """
    The Scene Manager houses a collection of scenes and allows switching between different scenes.
    Also handles the drawing and updating of current scene.
    """
    def __init__(self):
        self.scenes = {}
        self.min_id = 0
        self.current = 0

    def add(self, scene: Scene, scene_id: int | str = "") -> int | str:
        """
        Creates a new scene and adds it to the scene manager.

        :param scene: A scene object.
        :param scene_id: The id for the new scene. defaults to an incrementing value.
        :return: The scene's id value.
        """
        if scene_id == "":
            scene_id = self.min_id
            self.min_id += 1

        if scene_id in self.scenes.keys():
            raise ValueError(f"The scene id {scene_id} is not unique in this manager")

        self.scenes[scene_id] = scene
        scene.id = scene_id
        return scene_id

    @property
    def is_empty(self) -> bool:
        """
        Property method to check if the scene is empty.

        :return: Returns whether the scene list is empty.
        """
        return not bool(self.scenes.keys())

    def set(self, scene_id: int or str):
        """
        Changes the current scene to a new scene.

        :param scene_id: The id of the new scene.
        """
        self.current = scene_id

    @property
    def current_scene(self) -> Scene:
        """
        Get the Scene class of the current scene.

        :return: The Scene class of the current scene.
        """
        return self.scenes.get(self.current)

    def update(self):
        """
        Calls the update function of the current scene.
        """
        if self.is_empty: return
        self.current_scene.update()

    def draw(self, game):
        """
        Calls the draw function of the current scene.
        """
        if self.is_empty: return
        self.current_scene.draw(game)

