#version 330
layout(location = 0) in vec3 position;
layout(location = 1) in vec4 colour;
layout(location = 2) in mat4 model;

uniform mat4 view;
uniform mat4 proj;

out vec4 solidColour;

void main()
{
    solidColour = colour;
    gl_Position = proj * view * model * vec4(position, 1.0);
}
