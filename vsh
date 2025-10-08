#version 300 es
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 bPos;
out vec2 TexCoords;
uniform float offset;
vec3 finalPos;
void main() {
	finalPos = vec3(aPos.x, aPos.y + offset, aPos.z);
	gl_Position = vec4(finalPos, 1.0);
	TexCoords = bPos;
}
