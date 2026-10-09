import math
import tkinter as tk

_SCROLL_TARGETS = {}
_SCROLL_BINDINGS = {}


def rounded_panel(frame, fill, outline=None, radius=12):
    try:
        parent_background = frame.master.cget("bg")
    except tk.TclError:
        parent_background = "#f4efe7"

    frame.configure(
        bg=parent_background,
        bd=0,
        relief="flat",
        highlightthickness=0,
    )
    background = tk.Canvas(
        frame,
        bg=parent_background,
        bd=0,
        highlightthickness=0,
    )
    background.place(x=0, y=0, relwidth=1, relheight=1)

    def draw_panel(event):
        width = event.width
        height = event.height
        corner_radius = min(radius, width / 2, height / 2)
        points = []
        corners = (
            (corner_radius, corner_radius, 180),
            (width - corner_radius, corner_radius, 270),
            (width - corner_radius, height - corner_radius, 0),
            (corner_radius, height - corner_radius, 90),
        )
        for center_x, center_y, start_angle in corners:
            for step in range(9):
                angle = math.radians(start_angle + step * 90 / 8)
                points.extend(
                    (
                        center_x + corner_radius * math.cos(angle),
                        center_y + corner_radius * math.sin(angle),
                    )
                )

        background.delete("rounded-panel")
        background.create_polygon(
            *points,
            fill=fill,
            outline=outline or fill,
            width=1,
            tags="rounded-panel",
        )

    frame.bind("<Configure>", draw_panel, add="+")
    return background


def enable_mousewheel_scrolling(container, canvas):
    root = container._root()
    root_key = id(root.tk)
    window_key = (root_key, container.winfo_toplevel()._w)
    _SCROLL_TARGETS[window_key] = canvas

    def forget_target(event):
        if event.widget is container and _SCROLL_TARGETS.get(window_key) is canvas:
            _SCROLL_TARGETS.pop(window_key, None)

    container.bind("<Destroy>", forget_target, add="+")
    if root_key in _SCROLL_BINDINGS:
        return

    def scroll(event):
        try:
            event_window_key = (root_key, event.widget.winfo_toplevel()._w)
            target = _SCROLL_TARGETS.get(event_window_key)
            if target is None or not target.winfo_exists():
                return None
        except tk.TclError:
            return None

        if getattr(event, "num", None) == 4:
            units = -1
        elif getattr(event, "num", None) == 5:
            units = 1
        else:
            delta = getattr(event, "delta", 0)
            if not delta:
                return "break"
            units = max(1, round(abs(delta) / 120))
            if delta > 0:
                units = -units

        target.yview_scroll(units, "units")
        return "break"

    root.bind_all("<MouseWheel>", scroll, add="+")
    root.bind_all("<Button-4>", scroll, add="+")
    root.bind_all("<Button-5>", scroll, add="+")
    _SCROLL_BINDINGS[root_key] = root