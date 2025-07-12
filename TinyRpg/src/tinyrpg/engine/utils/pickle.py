import pickle

import pyray as pr


class PRPickler(pickle.Pickler):
    def __init__(self, file):
        super().__init__(file)

    def persistent_id(self, obj):
        match obj:
            case pr.ffi.CData():
                match pr.ffi.typeof(obj).cname:
                    case "struct Vector2":
                        return ("Vector2", (obj.x, obj.y))  # type: ignore
                    case "struct Vector3":
                        return ("Vector3", (obj.x, obj.y, obj.z))  # type: ignore
                    case "struct Rectangle":
                        return ("Rectangle", (obj.x, obj.y, obj.width, obj.height))  # type: ignore
                    case "struct BoundingBox":
                        return ("BoundingBox", ((obj.min.x, obj.min.y, obj.min.z), (obj.max.x, obj.max.y, obj.max.z)))  # type: ignore
                    case "struct Texture":
                        return ("Texture", None)
                    case _:
                        return None
            case _:
                return None


class PRUnpickler(pickle.Unpickler):
    def __init__(self, file):
        super().__init__(file)

    def persistent_load(self, pid):
        match pid:
            case ("Vector2", (x, y)):
                return pr.Vector2(x, y)
            case ("Vector3", (x, y, z)):
                return pr.Vector3(x, y, z)
            case ("Rectangle", (x, y, width, height)):
                return pr.Rectangle(x, y, width, height)
            case ("BoundingBox", (min, max)):
                return pr.BoundingBox(min, max)
            case ("Texture", None):
                return None
            case _:
                raise pickle.UnpicklingError("unsupported persistent object")
