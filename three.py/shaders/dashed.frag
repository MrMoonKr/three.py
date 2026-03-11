uniform vec3 color;
uniform float alpha;

uniform bool useVertexColors;
in vec3 vColor;

uniform bool useDashes;
uniform float dashLength;
uniform float gapLength;
uniform float dashOffset;
in float arcLength;

uniform bool useFog;
uniform vec3 fogColor;
uniform float fogStartDistance;
uniform float fogEndDistance;
in float cameraDistance;

void main()
{
    if (useDashes)
    {
        float modLength = mod(arcLength + dashOffset, dashLength + gapLength);
        if (modLength > dashLength)
        {
            discard;
        }
    }

    vec4 baseColor = vec4(color, alpha);

    if (useVertexColors)
    {
        baseColor *= vec4(vColor, 1.0);
    }

    if (useFog)
    {
        float fogFactor = clamp(
            (fogEndDistance - cameraDistance) / (fogEndDistance - fogStartDistance),
            0.0,
            1.0
        );
        baseColor = mix(vec4(fogColor, 1.0), baseColor, fogFactor);
    }

    gl_FragColor = baseColor;
}
