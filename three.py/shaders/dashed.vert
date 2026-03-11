in vec3 vertexPosition;
in vec3 vertexColor;
in float vertexArcLength;

out vec3 vColor;
out float arcLength;

uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;
uniform mat4 modelMatrix;

uniform bool useFog;
out float cameraDistance;

void main()
{
    arcLength = vertexArcLength;
    vColor = vertexColor;

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);

    if (useFog)
    {
        cameraDistance = gl_Position.w;
    }
}
