# -*- coding: utf-8 -*-
import collections
import itertools
import os
import pathlib
import sys
import time

import numpy as np

# For Linux/Wayland users.
if os.getenv("XDG_SESSION_TYPE") == "wayland":
    os.environ["XDG_SESSION_TYPE"] = "x11"

import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer

DRIFT_SPEED = 100
TAIL_LENGTH = 1000

frame_time = 0.0


def tick():
    global frame_time
    frame_time = time.perf_counter()


bm = collections.deque([np.array([0., 0.])] * 10, maxlen=TAIL_LENGTH)

IS_DEBUG = (sys.gettrace() is not None)


def frame_commands():
    last_time = frame_time
    tick()
    curr_time = frame_time
    dt = curr_time - last_time
    try:
        fps = int(1 / dt)
    except ZeroDivisionError:
        fps = 0

    io = imgui.get_io()

    if io.key_ctrl and io.keys_down[glfw.KEY_Q]:
        sys.exit(0)

    with imgui.begin_main_menu_bar() as main_menu_bar:
        if main_menu_bar.opened:
            with imgui.begin_menu("File", True) as file_menu:
                if file_menu.opened:
                    clicked_quit, selected_quit = imgui.menu_item("Quit", "Ctrl+Q")
                    if clicked_quit:
                        sys.exit(0)

    with imgui.begin("FPS"):
        imgui.text(f"Debug: ")
        imgui.same_line()
        if IS_DEBUG:
            imgui.text_colored("ON", 0., 1., 0.)
        else:
            imgui.text_colored("OFF", 1., 0., 0.)
        imgui.text(f"FPS: {fps}")

    scale = np.sqrt(dt) * 200
    dbm = np.random.multivariate_normal(mean=(0.0, 0.0), cov=scale * np.eye(2))
    next_bm = bm[len(bm) - 1] + dbm
    next_bm = np.maximum(next_bm, 0.0)
    next_bm = np.minimum(next_bm, np.array(glfw.get_window_size(glfw.get_current_context())))
    bm.append(next_bm)
    if tuple(io.mouse_pos) != (-1, -1):
        drift = (np.array(io.mouse_pos) - next_bm) / DRIFT_SPEED
        next_bm += drift
    draw_list = imgui.get_overlay_draw_list()
    for idx, ((x1, y1), (x2, y2)) in enumerate(itertools.pairwise(bm)):
        color = imgui.get_color_u32_rgba(1., 1., 1., idx / (len(bm) - 1))
        draw_list.add_line(x1, y1, x2, y2, color, thickness=1.0)


def render_frame(impl, window, font):
    glfw.poll_events()
    impl.process_inputs()
    imgui.new_frame()

    gl.glClearColor(0.1, 0.1, 0.1, 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    imgui.push_font(font)
    frame_commands()
    imgui.pop_font()

    imgui.render()
    impl.render(imgui.get_draw_data())
    glfw.swap_buffers(window)


def impl_glfw_init():
    width, height = 600, 600
    window_name = "Brownian motion demo"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        sys.exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.make_context_current(window)
    glfw.swap_interval(0)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        sys.exit(1)

    return window


def main():
    imgui.create_context()
    window = impl_glfw_init()

    impl = GlfwRenderer(window)

    font_path = pathlib.Path(__file__).with_name("Montserrat-ExtraBold.ttf")
    try:
        font = imgui.get_io().fonts.add_font_from_file_ttf(str(font_path), 80)
    except imgui.ImGuiError:
        font = imgui.get_io().fonts.add_font_default()
    impl.refresh_font_texture()

    while not glfw.window_should_close(window):
        render_frame(impl, window, font)

    impl.shutdown()
    glfw.terminate()


if __name__ == "__main__":
    main()
