#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;

out vec2 TexCoord;

uniform mat4 transform;           // the whole transformation, sent from Python

void main()
{
    gl_Position = transform * vec4(aPos, 1.0);   // matrix * vector
    TexCoord = aTexCoord;
}
