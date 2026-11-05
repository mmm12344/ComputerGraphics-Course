#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;

out vec2 TexCoord;

uniform float texScale;            // 1.0 = normal, 2.0 = coordinates 0..2

void main()
{
    gl_Position = vec4(aPos, 1.0);
    TexCoord = aTexCoord * texScale;
}
