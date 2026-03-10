# Shader System Notes

## Current Structure

- This project currently defines GLSL shaders as Python string literals inside `Material` subclasses.
- The common shader compilation entry point is `three.py/material/Material.py`.
- Existing materials such as `SurfaceBasicMaterial` and `LineBasicMaterial` follow this inline-string pattern.

## Porting Direction

- The codebase is already well-suited for a three.js-style shader system port.
- The preferred approach is to layer a shader registry and preprocessing system on top of the current string-based model.
- A full renderer rewrite is not the goal.

## Target Design

- Add a `ShaderChunk`-style registry for reusable GLSL fragments.
- Add a preprocessor that resolves `#include <chunk>` directives.
- Add a `ShaderLib`-style registry for named vertex/fragment shader templates.
- Add a `UniformsLib`-style registry for reusable uniform groups and merges.
- Migrate existing materials gradually to the shared shader system.

## Constraints

- Keep existing string-based materials working during the transition.
- Do not require an immediate switch to file-based shaders.
- Minimize changes by focusing first on `Material` and shader compilation utilities.

## Working Summary

`three.py` already uses a string-based GLSL material structure, so the most practical way to port the three.js shader system is to add `ShaderChunk`, `ShaderLib`, and `#include` preprocessing around the existing `Material` pipeline.
