# All the imported libraries are on the top

from OpenGL.GL import *
import glfw
import numpy









# After importing the libraries, comes the custom functions to make development easier for the future


def process_input(window, Loc):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        print("Hello")

def makeShader(src, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, src)
    glCompileShader(shader)
    return shader

def make_sp(vertex_shader, fragment_shader):
    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)
    return shader_program







# Vertices are defined here along with indices
# Do keep in mind that the vertices are defined top-left first, top-right second, bottom-left third, bottom-right last

player_vertices = numpy.array( [
    -0.3, 0.3, 0.0,
     0.3, 0.3, 0.0,
    -0.3,-0.3, 0.0,
     0.3,-0.3, 0.0
], dtype = numpy.float32 )

background_vertices = numpy.array( [
    -1.0, 1.0,-1.0,
     1.0, 1.0,-1.0,
    -1.0,-1.0,-1.0,
     1.0,-1.0,-1.0
], dtype = numpy.float32 )

standard_indices = numpy.array( [
    0, 1, 3,
    0, 2, 3
], dtype = numpy.int32 )





# After custom functions are shaders that are gonna be used in the game, they are here now for the sake of organization,
# they will be moved to different files later on






player_vs_src = """
#version 330 core
layout (location = 0) in vec3 aPos;
void main() {
    gl_Position = vec4(aPos, 1.0);
}
"""

player_fs_src = """
#version 330 core
out vec4 FragColor;
void main() {
    FragColor = vec4(0.0, 1.0, 0.0, 1.0);
}
"""

background_vs_src = """
#version 330 core
layout (location = 0) in vec3 aPos;
uniform vec2 offset;
vec3 finalPos;
void main() {
    finalPos = vec3(aPos.x + offset.x, aPos.y + offset.y, aPos.z)
    gl_Position = vec4(finalPos, 1.0);
}
"""

background_fs_src = """
#version 330 core
out vec4 FragColor;
void main() {
    FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
"""





# You could say here starts the actual code but it is just initializing glfw


glfw.init()
window_width = 800
window_height = 600
window = glfw.create_window(window_width, window_height, "basic", None, None)
glfw.make_context_current(window)



# Shader stuff for player

vs = makeShader(player_vs_src, GL_VERTEX_SHADER)
fs = makeShader(player_fs_src, GL_FRAGMENT_SHADER)
sp = make_sp(vs, fs)

glDeleteShader(vs)
glDeleteShader(fs)

# Shader stuff for background

vs2 = makeShader(background_vs_src, GL_VERTEX_SHADER)
fs2 = makeShader(background_fs_src, GL_FRAGMENT_SHADER)
sp2 = make_sp(vs2, fs2)

glDeleteShader(vs2)
glDeleteShader(fs2)






# Player data

player_vao = glGenVertexArrays(1)
player_vbo = glGenBuffers(1)
player_ebo = glGenBuffers(1)

glBindVertexArray(player_vao)

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, player_ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, standard_indices.nbytes, standard_indices, GL_STATIC_DRAW)

glBindBuffer(GL_ARRAY_BUFFER, player_vbo)
glBufferData(GL_ARRAY_BUFFER, player_vertices.nbytes, player_vertices, GL_STATIC_DRAW)

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
glEnableVertexAttribArray(0)

# Background data

background_vao = glGenVertexArrays(1)
background_vbo = glGenBuffers(1)
background_ebo = glGenBuffers(1)

glBindVertexArray(background_vao)

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, background_ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, standard_indices.nbytes, standard_indices, GL_STATIC_DRAW)

glBindBuffer(GL_ARRAY_BUFFER, background_vbo)
glBufferData(GL_ARRAY_BUFFER, background_vertices.nbytes, background_vertices, GL_STATIC_DRAW)

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
glEnableVertexAttribArray(0)


glUseProgram(sp2)
offsetLoc = glGetUniformLocation(sp2, "offset")



# Our main loop where we keep updating stuff


while not glfw.window_should_close(window):
    glClearColor(0.0, 0.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # bro for some reason this part has weird syntax, some pythonic black magic
    window_width, window_height = glfw.get_framebuffer_size(window) # this is the line I was talking about
    glViewport(0, 0, window_width, window_height)

    glBindVertexArray(background_vao)
    glUseProgram(sp2)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

    glBindVertexArray(player_vao)
    glUseProgram(sp)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

    process_input(window)

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
