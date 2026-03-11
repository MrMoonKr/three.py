import re
from textwrap import dedent

ShaderChunk = {}
ShaderLib = {}

_INCLUDE_PATTERN = re.compile(r"^[ \t]*#include\s+<([\w\d./-]+)>[ \t]*$", re.MULTILINE)


def _normalizeShaderCode(shaderCode):
    return dedent(shaderCode).strip() + "\n"


def registerShaderChunk(name, shaderCode):
    ShaderChunk[name] = _normalizeShaderCode(shaderCode)
    return ShaderChunk[name]


def registerShaderLib(name, vertexShader, fragmentShader):
    ShaderLib[name] = {
        "vertexShader": _normalizeShaderCode(vertexShader),
        "fragmentShader": _normalizeShaderCode(fragmentShader),
    }
    return ShaderLib[name]


def resolveShaderIncludes(shaderCode, includeStack=None):
    includeStack = [] if includeStack is None else includeStack

    def replace(match):
        chunkName = match.group(1)

        if chunkName in includeStack:
            cycle = " -> ".join(includeStack + [chunkName])
            raise ValueError(f"Circular shader include detected: {cycle}")

        if chunkName not in ShaderChunk:
            raise KeyError(f"Unknown shader chunk: {chunkName}")

        includeStack.append(chunkName)
        chunkCode = resolveShaderIncludes(ShaderChunk[chunkName], includeStack)
        includeStack.pop()
        return chunkCode

    return _INCLUDE_PATTERN.sub(replace, _normalizeShaderCode(shaderCode))


def getShaderProgramSources(shaderName):
    if shaderName not in ShaderLib:
        raise KeyError(f"Unknown shader library entry: {shaderName}")

    shader = ShaderLib[shaderName]
    vertexShader = resolveShaderIncludes(shader["vertexShader"])
    fragmentShader = resolveShaderIncludes(shader["fragmentShader"])
    return vertexShader, fragmentShader

# "fog_vertex_pars"
registerShaderChunk(
    "fog_vertex_pars",
    """
    uniform bool useFog;
    out float cameraDistance;
    """,
)
# "fog_vertex"
registerShaderChunk(
    "fog_vertex",
    """
    if (useFog)
    {
        cameraDistance = gl_Position.w;
    }
    """,
)
# "fog_fragment_pars"
registerShaderChunk(
    "fog_fragment_pars",
    """
    uniform bool useFog;
    uniform vec3 fogColor;
    uniform float fogStartDistance;
    uniform float fogEndDistance;
    in float cameraDistance;
    """,
)
# "fog_fragment"
registerShaderChunk(
    "fog_fragment",
    """
    if ( useFog )
    {
        float fogFactor = clamp( (fogEndDistance - cameraDistance)/(fogEndDistance - fogStartDistance), 0.0, 1.0 );
        baseColor = mix( vec4(fogColor,1.0), baseColor, fogFactor );
    }
    """,
)

# "shadow_vertex_pars"
registerShaderChunk(
    "shadow_vertex_pars",
    """
    uniform bool receiveShadow;
    uniform mat4 shadowProjectionMatrix;
    uniform mat4 shadowViewMatrix;
    out vec4 positionFromShadowLight;
    """,
)
# "shadow_vertex"
registerShaderChunk(
    "shadow_vertex",
    """
    if (receiveShadow)
    {
        positionFromShadowLight = shadowProjectionMatrix * shadowViewMatrix * modelMatrix * vec4(vertexPosition, 1);
    }
    """,
)
# "shadow_fragment_pars"
registerShaderChunk(
    "shadow_fragment_pars",
    """
    uniform bool receiveShadow;
    in vec4 positionFromShadowLight;
    uniform sampler2D shadowMap;
    uniform float shadowStrength;
    uniform float shadowBias;
    uniform vec3 shadowLightDirection;
    """,
)
# "shadow_fragment"
registerShaderChunk(
    "shadow_fragment",
    """
    if ( receiveShadow )
    {
        vec3 unitNormal = normalize(normal);
        float cosAngle = dot(unitNormal, shadowLightDirection);
        bool facingLight = (cosAngle < -0.05);

        vec3 shadowCoord = ( positionFromShadowLight.xyz / positionFromShadowLight.w ) / 2.0 + 0.5;
        float closestDistanceToLight = texture2D(shadowMap, shadowCoord.xy).r;
        float fragmentDistanceToLight = shadowCoord.z;
        if (facingLight && fragmentDistanceToLight > closestDistanceToLight + shadowBias)
            baseColor *= vec4( shadowStrength, shadowStrength, shadowStrength, 1.0 );
    }
    """,
)

# "light_struct"
registerShaderChunk(
    "light_struct",
    """
    struct Light
    {
        bool isAmbient;
        bool isDirectional;
        bool isPoint;
        bool isHemisphere;

        float strength;
        vec3 color;

        vec3 position;
        vec3 direction;
        vec3 groundColor;
    };

    uniform Light light0;
    uniform Light light1;
    uniform Light light2;
    uniform Light light3;
    """,
)
# "light_calculation"
registerShaderChunk(
    "light_calculation",
    """
    vec3 lightCalculation(Light light, vec3 fragPosition, vec3 fragNormal)
    {
        if ( light.isAmbient )
        {
            return light.color * light.strength;
        }
        else if ( light.isDirectional )
        {
            vec3 unitNormal = normalize(fragNormal);
            float cosAngle = max( dot(unitNormal, -light.direction), 0.0 );
            return light.color * light.strength * cosAngle;
        }
        else if ( light.isPoint )
        {
            vec3 lightDirection = normalize(light.position - fragPosition);
            vec3 unitNormal = normalize(fragNormal);
            float cosAngle = max( dot(unitNormal, lightDirection), 0.0 );
            float attenuation = 1.0;
            return light.color * light.strength * cosAngle * attenuation;
        }
        else if ( light.isHemisphere )
        {
            vec3 unitNormal = normalize(fragNormal);
            float blend = dot(unitNormal, light.direction) * 0.5 + 0.5;
            vec3 hemisphereColor = mix(light.groundColor, light.color, blend);
            return hemisphereColor * light.strength;
        }
        else
        {
            return vec3(0,0,0);
        }
    }
    """,
)

# "line_basic_vertex_pars"
registerShaderChunk(
    "line_basic_vertex_pars",
    """
    in vec3 vertexPosition;
    in vec3 vertexColor;
    in float vertexArcLength;

    out vec3 vColor;
    out float arcLength;

    uniform mat4 projectionMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 modelMatrix;

    #include <fog_vertex_pars>
    """,
)
# "line_basic_vertex"
registerShaderChunk(
    "line_basic_vertex",
    """
    arcLength = vertexArcLength;
    vColor = vertexColor;
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);

    #include <fog_vertex>
    """,
)
# "line_basic_fragment_pars"
registerShaderChunk(
    "line_basic_fragment_pars",
    """
    uniform vec3 color;
    uniform float alpha;

    uniform bool useVertexColors;
    in vec3 vColor;

    uniform bool useDashes;
    uniform float dashLength;
    uniform float gapLength;
    uniform float dashOffset;
    in float arcLength;

    #include <fog_fragment_pars>
    """,
)
# "line_basic_fragment"
registerShaderChunk(
    "line_basic_fragment",
    """
    if ( useDashes )
    {
        float modLength = mod(arcLength + dashOffset, dashLength + gapLength);
        if ( modLength > dashLength )
            discard;
    }

    vec4 baseColor = vec4(color, alpha);

    if ( useVertexColors )
        baseColor *= vec4( vColor, 1.0 );

    #include <fog_fragment>

    gl_FragColor = baseColor;
    """,
)

# "surface_basic_vertex_pars"
registerShaderChunk(
    "surface_basic_vertex_pars",
    """
    in vec3 vertexPosition;
    in vec2 vertexUV;
    in vec3 vertexNormal;
    in vec3 vertexColor;

    out vec3 position;
    out vec2 UV;
    out vec3 normal;
    out vec3 vColor;

    uniform mat4 projectionMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 modelMatrix;

    #include <fog_vertex_pars>
    #include <shadow_vertex_pars>
    """,
)
# "surface_basic_vertex"
registerShaderChunk(
    "surface_basic_vertex",
    """
    position = vec3( modelMatrix * vec4(vertexPosition, 1) );
    UV = vertexUV;
    normal = normalize(mat3(modelMatrix) * vertexNormal);
    vColor = vertexColor;

    #include <shadow_vertex>

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);

    #include <fog_vertex>
    """,
)
# "surface_basic_fragment_pars"
registerShaderChunk(
    "surface_basic_fragment_pars",
    """
    uniform vec3 color;
    uniform float alpha;

    in vec3 position;
    in vec2 UV;
    in vec3 normal;

    uniform bool useVertexColors;
    in vec3 vColor;

    uniform bool useTexture;
    uniform sampler2D image;

    uniform float alphaTest;

    uniform bool useLight;

    #include <light_struct>
    #include <light_calculation>
    #include <fog_fragment_pars>
    #include <shadow_fragment_pars>
    """,
)
# "surface_basic_fragment"
registerShaderChunk(
    "surface_basic_fragment",
    """
    vec4 baseColor = vec4(color, alpha);

    if ( useVertexColors )
        baseColor *= vec4(vColor, 1);

    if ( useTexture )
        baseColor *= texture2D(image, UV);

    if ( useLight )
    {
        vec3 totalLight = vec3(0,0,0);
        totalLight += lightCalculation( light0, position, normal );
        totalLight += lightCalculation( light1, position, normal );
        totalLight += lightCalculation( light2, position, normal );
        totalLight += lightCalculation( light3, position, normal );
        totalLight = min( totalLight, vec3(1,1,1) );
        baseColor *= vec4( totalLight, 1 );
    }

    #include <fog_fragment>
    #include <shadow_fragment>

    gl_FragColor = baseColor;

    if (gl_FragColor.a < alphaTest)
        discard;
    """,
)

# "basic" shader program
registerShaderLib(
    "basic",
    """
    #include <surface_basic_vertex_pars>

    void main()
    {
        #include <surface_basic_vertex>
    }
    """,
    """
    #include <surface_basic_fragment_pars>

    void main()
    {
        #include <surface_basic_fragment>
    }
    """,
)

# "line_basic" shader program
registerShaderLib(
    "line_basic",
    """
    #include <line_basic_vertex_pars>

    void main()
    {
        #include <line_basic_vertex>
    }
    """,
    """
    #include <line_basic_fragment_pars>

    void main()
    {
        #include <line_basic_fragment>
    }
    """,
)

# "dashed" shader program
registerShaderLib(
    "dashed",
    """
    #include <line_basic_vertex_pars>

    void main()
    {
        #include <line_basic_vertex>
    }
    """,
    """
    #include <line_basic_fragment_pars>

    void main()
    {
        #include <line_basic_fragment>
    }
    """,
)

# "points_vertex_pars"
registerShaderChunk(
    "points_vertex_pars",
    """
    in vec3 vertexPosition;
    in vec3 vertexColor;

    out vec3 vColor;

    uniform bool usePerspective;
    uniform float size;

    uniform mat4 projectionMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 modelMatrix;
    """,
)
# "points_vertex"
registerShaderChunk(
    "points_vertex",
    """
    vColor = vertexColor;
    vec4 eyePosition = viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);

    if ( usePerspective )
        gl_PointSize = 500 * size / length(eyePosition);
    else
        gl_PointSize = size;

    gl_Position = projectionMatrix * eyePosition;
    """,
)
# "points_fragment_pars"
registerShaderChunk(
    "points_fragment_pars",
    """
    uniform vec3 color;
    uniform float alpha;

    uniform bool useVertexColors;
    in vec3 vColor;

    uniform bool useTexture;
    uniform sampler2D image;
    uniform float alphaTest;
    """,
)
# "points_fragment"
registerShaderChunk(
    "points_fragment",
    """
    vec4 baseColor = vec4(color, alpha);

    if ( useVertexColors )
        baseColor *= vec4(vColor, 1.0);

    if ( useTexture )
        baseColor *= texture(image, gl_PointCoord);

    gl_FragColor = baseColor;

    if (gl_FragColor.a < alphaTest)
        discard;
    """,
)

# "point_basic"
registerShaderLib(
    "point_basic",
    """
    #include <points_vertex_pars>

    void main()
    {
        #include <points_vertex>
    }
    """,
    """
    #include <points_fragment_pars>

    void main()
    {
        #include <points_fragment>
    }
    """,
)

# "points" shader program
registerShaderLib(
    "points",
    """
    #include <points_vertex_pars>

    void main()
    {
        #include <points_vertex>
    }
    """,
    """
    #include <points_fragment_pars>

    void main()
    {
        #include <points_fragment>
    }
    """,
)

# "shadow_vertex_pars_only"
registerShaderChunk(
    "shadow_vertex_pars_only",
    """
    in vec3 vertexPosition;
    uniform mat4 shadowProjectionMatrix;
    uniform mat4 shadowViewMatrix;
    uniform mat4 modelMatrix;
    """,
)
# "shadow_vertex_main"
registerShaderChunk(
    "shadow_vertex_main",
    """
    gl_Position = shadowProjectionMatrix * shadowViewMatrix * modelMatrix * vec4(vertexPosition, 1);
    """,
)
# "shadow_fragment_main"
registerShaderChunk(
    "shadow_fragment_main",
    """
    gl_FragColor = vec4(gl_FragCoord.z, gl_FragCoord.z, gl_FragCoord.z, 1);
    """,
)

# "shadow" shader program
registerShaderLib(
    "shadow",
    """
    #include <shadow_vertex_pars_only>

    void main()
    {
        #include <shadow_vertex_main>
    }
    """,
    """
    void main()
    {
        #include <shadow_fragment_main>
    }
    """,
)

# "sprite_vertex_pars"
registerShaderChunk(
    "sprite_vertex_pars",
    """
    in vec2 vertexData;
    out vec2 UV;

    uniform vec2 anchor;
    uniform vec2 size;

    uniform mat4 projectionMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 modelMatrix;
    """,
)
# "sprite_vertex"
registerShaderChunk(
    "sprite_vertex",
    """
    UV = vertexData;
    vec3 position = vec3( (vertexData.x - anchor.x) * size.x, (vertexData.y - anchor.y) * size.y, 0 );
    mat4 billboardMatrix = viewMatrix * modelMatrix;
    billboardMatrix[0][0] = 1;
    billboardMatrix[0][1] = 0;
    billboardMatrix[0][2] = 0;
    billboardMatrix[1][0] = 0;
    billboardMatrix[1][1] = 1;
    billboardMatrix[1][2] = 0;
    billboardMatrix[2][0] = 0;
    billboardMatrix[2][1] = 0;
    billboardMatrix[2][2] = 1;
    gl_Position = projectionMatrix * billboardMatrix * vec4( position, 1 );
    """,
)
# "sprite_fragment_pars"
registerShaderChunk(
    "sprite_fragment_pars",
    """
    uniform vec3 color;
    uniform float alpha;

    in vec2 UV;
    uniform sampler2D image;

    uniform float alphaTest;
    """,
)
# "sprite_fragment"
registerShaderChunk(
    "sprite_fragment",
    """
    gl_FragColor = vec4(color, alpha) * texture2D(image, UV);

    if (gl_FragColor.a < alphaTest)
        discard;
    """,
)

# "sprite" shader program
registerShaderLib(
    "sprite",
    """
    #include <sprite_vertex_pars>

    void main()
    {
        #include <sprite_vertex>
    }
    """,
    """
    #include <sprite_fragment_pars>

    void main()
    {
        #include <sprite_fragment>
    }
    """,
)

# "surface_basic" shader program
registerShaderLib(
    "surface_basic",
    """
    #include <surface_basic_vertex_pars>

    void main()
    {
        #include <surface_basic_vertex>
    }
    """,
    """
    #include <surface_basic_fragment_pars>

    void main()
    {
        #include <surface_basic_fragment>
    }
    """,
)
