#version 330 core
in vec3 ourColor;
in vec2 TexCoord;
out vec4 FragColor;

uniform sampler2D ourTexture;      // which texture unit to read from
uniform bool useVertexColor;       // multiply by the vertex colours?

void main()
{
    vec4 texel = texture(ourTexture, TexCoord);     // sample the texture
    if (useVertexColor)
        FragColor = texel * vec4(ourColor, 1.0);
    else
        FragColor = texel;
}
