from material.LineDashedMaterial import LineDashedMaterial


class LineDashedScrollingMaterial(LineDashedMaterial):

    def __init__(
        self,
        color=[1, 1, 1],
        alpha=1,
        lineWidth=4,
        dashLength=0.50,
        gapLength=0.25,
        dashOffset=0.0,
        dashSpeed=1.0,
        useVertexColors=False,
    ):

        super().__init__(
            color=color,
            alpha=alpha,
            lineWidth=lineWidth,
            dashLength=dashLength,
            gapLength=gapLength,
            dashOffset=dashOffset,
            useVertexColors=useVertexColors,
        )

        self.dashSpeed = dashSpeed

    def update(self, deltaTime):
        self.advance(self.dashSpeed * deltaTime)
