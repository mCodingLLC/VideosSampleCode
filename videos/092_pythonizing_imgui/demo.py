# -*- coding: utf-8 -*-
import os
import sys

# For Linux/Wayland users.
if os.getenv("XDG_SESSION_TYPE") == "wayland":
    os.environ["XDG_SESSION_TYPE"] = "x11"

import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer

active = {
    "window": True,
    "child": False,
    "tooltip": False,
    "menu bar": False,
    "popup": False,
    "popup modal": False,
    "popup context item": False,
    "popup context window": False,
    "drag drop": False,
    "group": False,
    "tab bar": False,
    "list box": False,
    "popup context void": False,
    "table": False,
}

path_to_font = None  # "path/to/font.ttf"

opened_state = True


def frame_commands():
    gl.glClearColor(0.1, 0.1, 0.1, 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    io = imgui.get_io()

    if io.key_ctrl and io.keys_down[glfw.KEY_Q]:
        sys.exit(0)

    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):
            clicked_quit, selected_quit = imgui.menu_item("Quit", "Ctrl+Q", False, True)

            if clicked_quit:
                sys.exit(0)

            imgui.end_menu()
        imgui.end_main_menu_bar()

    # turn windows on/off
    imgui.begin("Active examples")
    for label, enabled in active.copy().items():
        _, enabled = imgui.checkbox(label, enabled)
        active[label] = enabled
    imgui.end()

    if active["window"]:
        imgui.begin("Hello, Imgui!")
        imgui.text("Hello, World!")
        imgui.end()

    if active["child"]:
        imgui.begin("Example: child region")
        imgui.begin_child("region", 150, -50, border=True)
        imgui.text("inside region")
        imgui.end_child()
        imgui.text("outside region")
        imgui.end()

    if active["tooltip"]:
        imgui.begin("Example: tooltip")
        imgui.button("Click me!")
        if imgui.is_item_hovered():
            imgui.begin_tooltip()
            imgui.text("This button is clickable.")
            imgui.end_tooltip()
        imgui.end()

    if active["menu bar"]:
        try:
            flags = imgui.WINDOW_MENU_BAR
            imgui.begin("Child Window - File Browser", flags=flags)
            if imgui.begin_menu_bar():
                if imgui.begin_menu('File'):
                    clicked, state = imgui.menu_item('Close')
                    if clicked:
                        active["menu bar"] = False
                        raise Exception
                    imgui.end_menu()
                imgui.end_menu_bar()
            imgui.end()
        except Exception:
            print("exception caught, but too late!")

    if active["popup"]:
        imgui.begin("Example: simple popup")
        if imgui.button("select"):
            imgui.open_popup("select-popup")
        imgui.same_line()
        if imgui.begin_popup("select-popup"):
            imgui.text("Select one")
            imgui.separator()
            imgui.selectable("One")
            imgui.selectable("Two")
            imgui.selectable("Three")
            imgui.end_popup()
        imgui.end()

    if active["popup modal"]:
        imgui.begin("Example: simple popup modal")
        if imgui.button("Open Modal popup"):
            imgui.open_popup("select-popup-modal")
        imgui.same_line()
        if imgui.begin_popup_modal("select-popup-modal")[0]:
            imgui.text("Select an option:")
            imgui.separator()
            imgui.selectable("One")
            imgui.selectable("Two")
            imgui.selectable("Three")
            imgui.end_popup()
        imgui.end()

    if active["popup context item"]:
        imgui.begin("Example: popup context view")
        imgui.text("Right-click to set value.")
        if imgui.begin_popup_context_item("Item Context Menu"):
            imgui.selectable("Set to Zero")
            imgui.end_popup()
        imgui.end()

    if active["popup context window"]:
        imgui.begin("Example: popup context window")
        if imgui.begin_popup_context_window():
            imgui.selectable("Clear")
            imgui.end_popup()
        imgui.end()

    if active["popup context void"]:
        if imgui.begin_popup_context_void():
            imgui.selectable("Clear")
            imgui.end_popup()

    if active["drag drop"]:
        imgui.begin("Example: drag and drop")
        imgui.button('source')
        if imgui.begin_drag_drop_source():
            imgui.set_drag_drop_payload('itemtype', b'payload')
            imgui.button('dragged source')
            imgui.end_drag_drop_source()
        imgui.button('dest')
        if imgui.begin_drag_drop_target():
            payload = imgui.accept_drag_drop_payload('itemtype')
            if payload is not None:
                print('Received:', payload)
            imgui.end_drag_drop_target()
        imgui.end()

    if active["group"]:
        imgui.begin("Example: item groups")
        imgui.begin_group()
        imgui.text("First group (buttons):")
        imgui.button("Button A")
        imgui.button("Button B")
        imgui.end_group()
        imgui.same_line(spacing=50)
        imgui.begin_group()
        imgui.text("Second group (text and bullet texts):")
        imgui.bullet_text("Bullet A")
        imgui.bullet_text("Bullet B")
        imgui.end_group()
        imgui.end()

    if active["tab bar"]:
        imgui.begin("Example Tab Bar")
        if imgui.begin_tab_bar("MyTabBar"):
            if imgui.begin_tab_item("Item 1")[0]:
                imgui.text("Here is the tab content!")
                imgui.end_tab_item()
            if imgui.begin_tab_item("Item 2")[0]:
                imgui.text("Another content...")
                imgui.end_tab_item()
            global opened_state
            selected, opened_state = imgui.begin_tab_item("Item 3", opened=opened_state)
            if selected:
                imgui.text("Hello Saylor!")
                imgui.end_tab_item()
            imgui.end_tab_bar()
        imgui.end()

    if active["list box"]:
        imgui.begin("Example: custom listbox")
        if imgui.begin_list_box("List", 200, 100):
            imgui.selectable("Selected", True)
            imgui.selectable("Not Selected", False)
            imgui.end_list_box()
        imgui.end()

    if active["table"]:
        imgui.begin("Example: table")
        if imgui.begin_table("data", 2):
            imgui.table_next_column()
            imgui.table_header("A")
            imgui.table_next_column()
            imgui.table_header("B")

            imgui.table_next_row()
            imgui.table_next_column()
            imgui.text("123")

            imgui.table_next_column()
            imgui.text("456")

            imgui.table_next_row()
            imgui.table_next_column()
            imgui.text("789")

            imgui.table_next_column()
            imgui.text("111")

            imgui.table_next_row()
            imgui.table_next_column()
            imgui.text("222")

            imgui.table_next_column()
            imgui.text("333")
            imgui.end_table()
        imgui.end()


def render_frame(impl, window, font):
    glfw.poll_events()
    impl.process_inputs()
    imgui.new_frame()

    gl.glClearColor(0.1, 0.1, 0.1, 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    if font is not None:
        imgui.push_font(font)
    frame_commands()
    if font is not None:
        imgui.pop_font()

    imgui.render()
    impl.render(imgui.get_draw_data())
    glfw.swap_buffers(window)


def impl_glfw_init():
    width, height = 1600, 900
    window_name = "minimal ImGui/GLFW3 example"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        sys.exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        sys.exit(1)

    return window


def main():
    imgui.create_context()
    window = impl_glfw_init()

    impl = GlfwRenderer(window)

    io = imgui.get_io()
    jb = io.fonts.add_font_from_file_ttf(path_to_font, 30) if path_to_font is not None else None
    impl.refresh_font_texture()

    while not glfw.window_should_close(window):
        render_frame(impl, window, jb)

    impl.shutdown()
    glfw.terminate()


if __name__ == "__main__":
    main()
