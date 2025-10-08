#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <GLES3/gl3.h>
#include <GLFW/glfw3.h>
#define STB_IMAGE_IMPLEMENTATION
#include <stb/stb_image.h>

char *fileReader(char *fileName);
void createVS(GLuint* vs, const char *vss);
void createFS(GLuint* fs, const char *fss);
void createSP(GLuint* vs, GLuint* fs, GLuint* sp);
void createTEX(GLuint* tex, char *imgName, int textureSlot);
void key_callback(GLFWwindow* window, int key, int scancode, int action, int mods);

float force = 0.0;

int main() {
	glfwInit();

	glfwWindowHint(GLFW_CLIENT_API, GLFW_OPENGL_ES_API);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 0);

	int w, h;

	GLFWwindow* win = glfwCreateWindow(800, 600, "test", NULL, NULL);
	glfwMakeContextCurrent(win);
	glEnable(GL_BLEND);
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
	glfwSetKeyCallback(win, key_callback);
	
	GLuint vs, fs, sp, vao, vbo, ebo, tex, texLoc, offsetLoc; // Bird
	GLuint vs1, fs1, sp1, vao1, vbo1, ebo1, tex1;  // Sky

	// Bird

	const char *vss = fileReader("vsh");
	const char *fss = fileReader("fsh");

	createVS(&vs, vss);
	createFS(&fs, fss);
	createSP(&vs, &fs, &sp);

	glDeleteShader(vs);
	glDeleteShader(fs);

	glUseProgram(sp);
	texLoc = glGetUniformLocation(sp, "TEX");
	offsetLoc = glGetUniformLocation(sp, "offset");
	createTEX(&tex, "Bird.png", 0);
	glUniform1i(texLoc, 0);

	float vert[] = {
		0.25, 0.25, 0.0,     1.0, 1.0,    // top right
		-0.25, 0.25, 0.0,    0.0, 1.0,   // top left
		-0.25, -0.25, 0.0,   0.0, 0.0,  // bottom left
		0.25, -0.25, 0.0,    1.0, 0.0  // bottom right
	};

	unsigned int ind[] = {
		3, 0, 1,
		3, 2, 1
	};

	glGenVertexArrays(1, &vao);
	glGenBuffers(1, &vbo);
	glGenBuffers(1, &ebo);

	glBindVertexArray(vao);

	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(ind), ind, GL_STATIC_DRAW);
	
	glBindBuffer(GL_ARRAY_BUFFER, vbo);
	glBufferData(GL_ARRAY_BUFFER, sizeof(vert), vert, GL_STATIC_DRAW);

	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)0 );
	glEnableVertexAttribArray(0);

	glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)(3 * sizeof(float)) );
	glEnableVertexAttribArray(1);

	// Sky

	const char *vss1 = fileReader("vsh1");
	const char *fss1 = fileReader("fsh1");

	createVS(&vs1, vss1);
	createFS(&fs1, fss1);
	createSP(&vs1, &fs1, &sp1);

	glDeleteShader(vs1);
	glDeleteShader(fs1);

	glUseProgram(sp1);
	GLuint TEX1Loc = glGetUniformLocation(sp1, "TEX1");
	GLuint panLoc = glGetUniformLocation(sp1, "pan");
	createTEX(&tex1, "sky-rework.png", 0);
	glUniform1i(TEX1Loc, 0);

	float vert1[] = {
		1.0, 1.0, -1.0,     1.0, 1.0,    // top right
		-1.0, 1.0, -1.0,    0.0, 1.0,   // top left
		-1.0, -1.0, -1.0,   0.0, 0.0,  // bottom left
		1.0, -1.0, -1.0,    1.0, 0.0  // bottom right
	};

	unsigned int ind1[] = {
		3, 0, 1,
		3, 2, 1
	};

	glGenVertexArrays(1, &vao1);
	glGenBuffers(1, &vbo1);
	glGenBuffers(1, &ebo1);

	glBindVertexArray(vao1);

	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo1);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(ind1), ind1, GL_STATIC_DRAW);

	glBindBuffer(GL_ARRAY_BUFFER, vbo1);
	glBufferData(GL_ARRAY_BUFFER, sizeof(vert1), vert1, GL_STATIC_DRAW);

	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)0 );
	glEnableVertexAttribArray(0);

	glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)(3 * sizeof(float)) );
	glEnableVertexAttribArray(1);

	float gravity = -0.002, yPos = 0.0, distance = 0.0;

	double prev_time, current_time, delta_time; 
	prev_time = glfwGetTime();

	while(!glfwWindowShouldClose(win)) {
		glClearColor(0.2, 0.1, 0.4, 1.0);
		glClear(GL_COLOR_BUFFER_BIT);

		glfwGetFramebufferSize(win, &w, &h);
		glViewport(0, 0, w, h);

		current_time = glfwGetTime();

		delta_time = current_time - prev_time;
		prev_time = current_time;

		distance += (1.0 * delta_time);

		glBindVertexArray(vao1);
		glUseProgram(sp1);
		glUniform1f(panLoc, distance);
		glBindTexture(GL_TEXTURE_2D, tex1);
		glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);

		glBindVertexArray(vao);
		glUseProgram(sp);
		glBindTexture(GL_TEXTURE_2D, tex);

		force += gravity;
		yPos += force;
		glUniform1f(offsetLoc, yPos);

		glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);

		glfwSwapBuffers(win);
		glfwPollEvents();
	}

	glfwDestroyWindow(win);
	glDeleteProgram(sp);
	glDeleteProgram(sp1);
	free((void*)vss);
	free((void*)fss);
	glDeleteTextures(1, &tex);
	glDeleteVertexArrays(1, &vao);
	glDeleteBuffers(1, &vbo);
	glDeleteBuffers(1, &ebo);
	glDeleteTextures(1, &tex1);
	glDeleteVertexArrays(1, &vao1);
	glDeleteBuffers(1, &vbo1);
	glDeleteBuffers(1, &ebo1);
	glfwTerminate();
}

char *fileReader(char *fileName) {
	FILE* filePointer = fopen(fileName, "r");
	fseek(filePointer, 0, SEEK_END);
	long fileSize = ftell(filePointer);
	rewind(filePointer);
	char* buffer = malloc(fileSize + 1);
	fread(buffer, 1, fileSize, filePointer);
	buffer[fileSize] = '\0';
	fclose(filePointer);
	return buffer;
}

void createVS(GLuint* vs, const char* vss) {
	*vs = glCreateShader(GL_VERTEX_SHADER);
	glShaderSource(*vs, 1, &vss, NULL);
	glCompileShader(*vs);
}

void createFS(GLuint* fs, const char* fss) {
	*fs = glCreateShader(GL_FRAGMENT_SHADER);
	glShaderSource(*fs, 1, &fss, NULL);
	glCompileShader(*fs);
}

void createSP(GLuint* vs, GLuint* fs, GLuint* sp) {
	*sp = glCreateProgram();
	glAttachShader(*sp, *vs);
	glAttachShader(*sp, *fs);
	glLinkProgram(*sp);
}

void createTEX(GLuint* tex, char *imageName, int textureSlot) {
	stbi_set_flip_vertically_on_load(true);
	int iw, ih, nch;
	unsigned char *imgData = stbi_load(imageName, &iw, &ih, &nch, 4);
	glGenTextures(1, tex);
	glActiveTexture(GL_TEXTURE0 + textureSlot);
	glBindTexture(GL_TEXTURE_2D, *tex);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, iw, ih, 0, GL_RGBA, GL_UNSIGNED_BYTE, imgData);
	glGenerateMipmap(GL_TEXTURE_2D);
	stbi_image_free(imgData);
}

void key_callback(GLFWwindow* window, int key, int scancode, int action, int mods) {
	if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS) {
		glfwSetWindowShouldClose(window, GLFW_TRUE);
	}

	else if(key == GLFW_KEY_SPACE && action == GLFW_PRESS) {
		force = 0.05;
	}
}
