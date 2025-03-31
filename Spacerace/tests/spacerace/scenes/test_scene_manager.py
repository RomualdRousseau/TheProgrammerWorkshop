from spacerace.scenes.scene_manager import Scene, get_next_scene


def test_get_next_scene():
    class SceneA:
        def init(self):
            print("init")

        def close(self):
            print("close")

        def update(self, dt: float):
            print("update")

        def draw(self):
            print("draw")

        def get_action(self) -> str:
            return "a"

    class SceneB:
        def init(self):
            print("init")

        def close(self):
            print("close")

        def update(self, dt: float):
            print("update")

        def draw(self):
            print("draw")

        def get_action(self) -> str:
            return "b"

    scenes: list[Scene] = [SceneA(), SceneB()]

    actions: list[str] = ["a", "b"]

    initial_scene = scenes[0]

    transition_table = {
        (scenes[0], actions[0]): scenes[1],
        (scenes[1], actions[1]): scenes[0],
    }

    scene = initial_scene
    scene.init()

    scene = get_next_scene(scene, transition_table)
    assert scene == scenes[1]

    scene = get_next_scene(scene, transition_table)
    assert scene == scenes[0]

    scene.close()
