#version 330 core
in vec2 TexCoord;
out vec4 FragColor;

uniform sampler2D texture1;        // texture unit 0: the container
uniform sampler2D texture2;        // texture unit 1: the smiley face
uniform float mixValue;            // 0 = only texture1, 1 = only texture2

void main()
{
    FragColor = mix(texture(texture1, TexCoord), texture(texture2, TexCoord), mixValue);
}
