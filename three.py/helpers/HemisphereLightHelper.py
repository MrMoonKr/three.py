from core import Mesh
from geometry import SphereGeometry
from material import SurfaceBasicMaterial
from mathutils import Matrix


class HemisphereLightHelper(Mesh):

    def __init__(self, hemisphereLight, radius=30, xResolution=32, yResolution=16):

        self.hemisphereLight = hemisphereLight

        geo = SphereGeometry(radius=radius, xResolution=xResolution, yResolution=yResolution)

        skyColor = hemisphereLight.uniformList.getUniformValue("color")
        groundColor = hemisphereLight.uniformList.getUniformValue("groundColor")

        vertexColorData = []
        for position in geo.attributeData["vertexPosition"]["value"]:
            blend = max(0.0, min(1.0, position[1] / radius * 0.5 + 0.5))
            color = [
                groundColor[0] * (1.0 - blend) + skyColor[0] * blend,
                groundColor[1] * (1.0 - blend) + skyColor[1] * blend,
                groundColor[2] * (1.0 - blend) + skyColor[2] * blend,
            ]
            vertexColorData.append(color)

        geo.setAttribute("vec3", "vertexColor", vertexColorData)

        mat = SurfaceBasicMaterial(color=[1,1,1], useVertexColors=True)
        mat.renderFront = False
        mat.renderBack = True

        super().__init__(geo, mat)

        # The dome stays centered on the scene origin and only follows the light direction.
        self.transform = Matrix()

    def render(self, shaderProgramID=None):
        self.transform.setRotationSubmatrix(self.hemisphereLight.transform.getRotationMatrix())
        super().render(shaderProgramID)
