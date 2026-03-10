import importlib.util
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORE_DIR = PROJECT_ROOT / "core"


def load_module(module_name):
    module_path = CORE_DIR / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def test_shader_lib_entries(shaders):
    expected_names = ["basic", "dashed", "points", "shadow", "sprite", "surface_basic", "line_basic"]
    for name in expected_names:
        assert_true(name in shaders.ShaderLib, f"Missing ShaderLib entry: {name}")


def test_include_resolution(shaders):
    for name in ["basic", "dashed", "points", "shadow", "sprite"]:
        vertex_shader, fragment_shader = shaders.getShaderProgramSources(name)
        assert_true("#include" not in vertex_shader, f"Unresolved include in vertex shader: {name}")
        assert_true("#include" not in fragment_shader, f"Unresolved include in fragment shader: {name}")
        assert_true("void main()" in vertex_shader, f"Vertex shader missing main(): {name}")
        assert_true("void main()" in fragment_shader, f"Fragment shader missing main(): {name}")


def test_uniforms_lib(uniforms):
    common_uniforms = uniforms.getUniformsLib("common")
    points_uniforms = uniforms.getUniformsLib("points")
    merged_uniforms = uniforms.getUniformsLib("common", "points")

    assert_true(len(common_uniforms) == 2, "Unexpected common uniform count")
    assert_true(len(points_uniforms) == 6, "Unexpected points uniform count")
    assert_true(len(merged_uniforms) == 8, "Unexpected merged uniform count")

    merged_names = {uniform[1] for uniform in merged_uniforms}
    for required_name in ["color", "alpha", "size", "usePerspective", "image", "alphaTest"]:
        assert_true(required_name in merged_names, f"Missing merged uniform: {required_name}")


def test_uniform_merge_override(uniforms):
    merged_uniforms = uniforms.mergeUniformSets(
        [("float", "alpha", 1.0), ("float", "size", 1.0)],
        [("float", "alpha", 0.25)],
    )
    merged_map = {name: (uniform_type, value) for uniform_type, name, value in merged_uniforms}

    assert_true(merged_map["alpha"] == ("float", 0.25), "Later uniform set should override earlier values")
    assert_true(merged_map["size"] == ("float", 1.0), "Non-overridden uniform should remain present")


def main():
    shaders = load_module("Shaders")
    uniforms = load_module("UniformsLib")

    test_shader_lib_entries(shaders)
    test_include_resolution(shaders)
    test_uniforms_lib(uniforms)
    test_uniform_merge_override(uniforms)

    print("Shader system tests passed.")


if __name__ == "__main__":
    main()
