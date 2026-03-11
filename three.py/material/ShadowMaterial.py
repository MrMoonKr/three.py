from material.Material import Material

class ShadowMaterial(Material):

    def __init__(self):
        super().__init__(shaderName="shadow", name="ShadowMaterial")
