# All the imported libraries are on the top

from OpenGL.GL import *
import glfw
import numpy









# After importing the libraries, comes the custom functions to make development easier for the future


def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

def makeShader(src, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, src)
    glCompileShader(shader)
    return shader
    glDeleteShader(shader)







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






vs_src = """
#version 330 core
layout (location = 0) in vec3 aPos;
void main() {
    gl_Position = vec4(aPos, 1.0);
}
"""

fs_src = """
#version 330 core
out vec4 FragColor;
void main() {
    FragColor = vec4(0.0, 1.0, 0.0, 1.0);
}
"""

vs2_src = """
#version 330 core
layout (location = 0) in vec3 aPos;
void main() {
    gl_Position = vec4(aPos, 1.0);
}
"""

fs2_src = """
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

vs = makeShader(vs_src, GL_VERTEX_SHADER)
fs = makeShader(fs_src, GL_FRAGMENT_SHADER)

sp = glCreateProgram()
glAttachShader(sp, vs)
glAttachShader(sp, fs)
glLinkProgram(sp)

glDeleteShader(vs)
glDeleteShader(fs)

# Shader stuff for background

vs2 = makeShader(vs2_src, GL_VERTEX_SHADER)
fs2 = makeShader(fs2_src, GL_FRAGMENT_SHADER)

sp2 = glCreateProgram()
glAttachShader(sp2, vs2)
glAttachShader(sp2, fs2)
glLinkProgram(sp2)

glDeleteShader(vs2)
glDeleteShader(fs2)






# Player data

vao = glGenVertexArrays(1)
vbo = glGenBuffers(1)
ebo = glGenBuffers(1)

glBindVertexArray(vao)

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, standard_indices.nbytes, standard_indices, GL_STATIC_DRAW)

glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, player_vertices.nbytes, player_vertices, GL_STATIC_DRAW)

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
glEnableVertexAttribArray(0)

# Background data

vao2 = glGenVertexArrays(1)
vbo2 = glGenBuffers(1)
ebo2 = glGenBuffers(1)

glBindVertexArray(vao2)

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo2)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, standard_indices.nbytes, standard_indices, GL_STATIC_DRAW)

glBindBuffer(GL_ARRAY_BUFFER, vbo2)
glBufferData(GL_ARRAY_BUFFER, background_vertices.nbytes, background_vertices, GL_STATIC_DRAW)

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
glEnableVertexAttribArray(0)



# Out main loop where we keep updating stuff


while not glfw.window_should_close(window):
    glClearColor(0.1, 0.4, 0.7, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # bro for some reason this part has weird syntax, some pythonic black magic
    window_width, window_height = glfw.get_framebuffer_size(window) # this is the line I was talking about
    glViewport(0, 0, window_width, window_height)

    glBindVertexArray(vao2)
    glUseProgram(sp2)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

    glBindVertexArray(vao)
    glUseProgram(sp)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

    process_input(window)

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()