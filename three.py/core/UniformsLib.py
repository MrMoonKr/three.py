from copy import deepcopy


UniformsLib = {
    "common": [
        ("vec3", "color", [1, 1, 1]),
        ("float", "alpha", 1),
    ],
    "line": [
        ("bool", "useVertexColors", 0),
        ("bool", "useDashes", 0),
        ("float", "dashLength", 0),
        ("float", "gapLength", 0),
        ("float", "dashOffset", 0),
    ],
    "surface": [
        ("bool", "useVertexColors", 0),
        ("bool", "useTexture", 0),
        ("sampler2D", "image", -1),
        ("float", "alphaTest", 0),
        ("bool", "useLight", 0),
    ],
    "points": [
        ("bool", "useVertexColors", 0),
        ("bool", "useTexture", 0),
        ("sampler2D", "image", -1),
        ("bool", "usePerspective", 1),
        ("float", "size", 1),
        ("float", "alphaTest", 0.75),
    ],
    "sprite": [
        ("vec2", "size", [1, 1]),
        ("vec2", "anchor", [0.5, 0.5]),
        ("sampler2D", "image", -1),
        ("float", "alphaTest", 0),
    ],
}


def cloneUniformSet(uniforms):
    return [(uniformType, name, deepcopy(value)) for uniformType, name, value in uniforms]


def mergeUniformSets(*uniformSets):
    merged = {}

    for uniformSet in uniformSets:
        for uniformType, name, value in uniformSet:
            merged[name] = (uniformType, name, deepcopy(value))

    return list(merged.values())


def getUniformsLib(*names):
    uniformSets = []
    for name in names:
        if name not in UniformsLib:
            raise KeyError(f"Unknown uniforms library entry: {name}")
        uniformSets.append(UniformsLib[name])
    return mergeUniformSets(*uniformSets)
