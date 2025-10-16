#!/usr/bin/env python3
"""
Spiral Window - Interactive 2D choice elements with simulated Aletheia agent

This expands the minimal prototype to:
- Render selectable 2D vectors (nodes) on a canvas
- Log user selections and interactions
- Show responses from a simulated "Aletheia" agent
- Provide hooks for modular ND (multi-dimensional) extensions and agent-driven dialogs

Dependencies:
- tkinter (stdlib)

Run:
  python -m ui.spiral_window
"""
from __future__ import annotations
import json
import math
import time
import tkinter as tk
from dataclasses import dataclass, field
from tkinter import ttk, messagebox
from typing import Callable, List, Optional, Tuple, Dict, Any

# -----------------------------
# Data models
# -----------------------------

@dataclass
class Choice:
    label: str
    x: float
    y: float
    level: int = 0
    parent: Optional["Choice"] = None
    radius: int = 36
    selected: bool = False
    meta: Dict[str, Any] = field(default_factory=dict)
    children: List["Choice"] = field(default_factory=list)

    def is_point_inside(self, px: float, py: float) -> bool:
        return math.hypot(px - self.x, py - self.y) <= self.radius


# -----------------------------
# Simulated Aletheia agent
# -----------------------------

class AletheiaAgent:
    """Very lightweight simulated agent for demo purposes.
    Replace this with a real agent API later.
    """

    def respond(self, event: str, payload: Dict[str, Any]) -> str:
        label = payload.get("label")
        level = payload.get("level")
        if event == "expand":
            return f"Aletheia: Expanding '{label}' at level {level}. Consider related intents."
        if event == "collapse":
            return f"Aletheia: Collapsed '{label}'. Backtracked to parent context."
        if event == "select":
            return f"Aletheia: You selected '{label}'. Next: confirm parameters or branch."
        if event == "hover":
            return f"Aletheia: Hovering over '{label}'."
        if event == "reset":
            return "Aletheia: Reset to root choices."
        return "Aletheia: Acknowledged."


# -----------------------------
# Spiral Window
# -----------------------------

class SpiralWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Spiral OS - Choice Primitive Interface")
        self.root.geometry("960x720")

        # State
        self.choices: List[Choice] = []
        self.expanded_choice: Optional[Choice] = None
        self.hover_choice: Optional[Choice] = None
        self.log: List[Dict[str, Any]] = []
        self.agent = AletheiaAgent()

        # UI
        self._setup_ui()
        self._create_initial_choices()

    # ----- UI setup -----
    def _setup_ui(self):
        # Header
        header = ttk.Frame(self.root)
        header.pack(fill=tk.X, padx=10, pady=6)

        ttk.Label(header, text="Spiral OS", font=("Segoe UI", 14, "bold")).pack(side=tk.LEFT)
        self.info_label = ttk.Label(header, text="Hover or click a choice.")
        self.info_label.pack(side=tk.LEFT, padx=12)

        ttk.Button(header, text="Reset", command=self._reset_choices).pack(side=tk.RIGHT)

        # Main content split: canvas (left) and right panel (logs + agent)
        body = ttk.Frame(self.root)
        body.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(body, bg="#0b0f14", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right = ttk.Notebook(body)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        # Logs tab
        self.log_text = tk.Text(right, height=16, wrap="word")
        self.log_text.configure(state="disabled")
        right.add(self.log_text, text="Log")

        # Agent tab
        agent_frame = ttk.Frame(right)
        right.add(agent_frame, text="Aletheia")
        self.agent_text = tk.Text(agent_frame, height=16, wrap="word")
        self.agent_text.pack(fill=tk.BOTH, expand=True)
        self.agent_text.insert("end", "Aletheia ready.\n")
        self.agent_text.configure(state="disabled")

        # Footer
        footer = ttk.Frame(self.root)
        footer.pack(fill=tk.X, padx=10, pady=6)
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(footer, textvariable=self.status_var).pack(side=tk.LEFT)

        # Bindings
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<Motion>", self._on_motion)
        self.root.bind("<Escape>", lambda e: self._reset_choices())

    # ----- Initial graph -----
    def _create_initial_choices(self):
        self.choices.clear()
        self.expanded_choice = None
        center = (420, 320)
        radius = 150
        labels = [
            "Ask", "Plan", "Do", "Reflect",
            "Share", "Data", "Agents", "Settings",
        ]
        for i, label in enumerate(labels):
            angle = (2 * math.pi / len(labels)) * i
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            self.choices.append(Choice(label=label, x=x, y=y, level=0, radius=34))
        self._draw_choices()
        self._log_event("init", {"labels": labels})
        self._agent_say("reset", {"labels": labels})

    # ----- Drawing -----
    def _draw_choices(self):
        self.canvas.delete("all")
        # Optional: draw center
        self.canvas.create_oval(410, 310, 430, 330, outline="#3a556a", fill="#13202e")
        for c in self.choices:
            self._draw_choice(c)

    def _draw_choice(self, c: Choice):
        fill = "#1e2a36"
        outline = "#4ea1ff" if c is self.hover_choice else "#2e4153"
        if c.selected:
            fill = "#234d20"  # greenish when selected
            outline = "#58d68d"
        x0, y0 = c.x - c.radius, c.y - c.radius
        x1, y1 = c.x + c.radius, c.y + c.radius
        self.canvas.create_oval(x0, y0, x1, y1, fill=fill, outline=outline, width=2)
        self.canvas.create_text(c.x, c.y, text=c.label, fill="#e6eef7", font=("Segoe UI", 10, "bold"))
        # Draw a vector line from parent (if any)
        if c.parent is not None:
            self.canvas.create_line(c.parent.x, c.parent.y, c.x, c.y, fill="#3a7bd5", dash=(3, 3))

    # ----- Interaction handlers -----
    def _on_motion(self, event):
        choice = self._find_choice_at(event.x, event.y)
        if choice is not self.hover_choice:
            self.hover_choice = choice
            if choice:
                self.status_var.set(f"Hover: {choice.label}")
                self.info_label.config(text=f"Hovering over {choice.label} (level {choice.level})")
                self._agent_say("hover", {"label": choice.label, "level": choice.level})
            else:
                self.status_var.set("Ready.")
                self.info_label.config(text="Hover or click a choice.")
            self._draw_choices()

    def _on_click(self, event):
        choice = self._find_choice_at(event.x, event.y)
        if not choice:
            self.status_var.set("Clicked empty space.")
            return
        # Toggle expand/collapse on non-leaf; select on leaf
        if choice.children:
            # collapse
            self._collapse_choice(choice)
            self._log_event("collapse", {"label": choice.label, "level": choice.level})
            self._agent_say("collapse", {"label": choice.label, "level": choice.level})
        else:
            # if already expanded previously, selection toggles
            if self._can_expand(choice):
                self._expand_choice(choice)
                self._log_event("expand", {"label": choice.label, "level": choice.level})
                self._agent_say("expand", {"label": choice.label, "level": choice.level})
            else:
                choice.selected = not choice.selected
                self._handle_choice_selection(choice)
        self._draw_choices()

    def _can_expand(self, choice: Choice) -> bool:
        # You can always expand until level 2 for demo
        return choice.level < 2

    def _expand_choice(self, choice: Choice):
        # Generate 4 child choices in a small spiral around the parent
        r0 = max(18, choice.radius - 8)
        for i in range(4):
            angle = (i * (math.pi / 3)) + (choice.level * 0.7)
            dist = 70 + 20 * i
            x = choice.x + dist * math.cos(angle)
            y = choice.y + dist * math.sin(angle)
            child = Choice(
                label=f"{choice.label}:{i+1}",
                x=x,
                y=y,
                level=choice.level + 1,
                parent=choice,
                radius=r0,
            )
            choice.children.append(child)
            self.choices.append(child)

    def _collapse_choice(self, choice: Choice):
        # remove all descendants from flat list
        def collect_desc(c: Choice, acc: List[Choice]):
            for ch in c.children:
                acc.append(ch)
                collect_desc(ch, acc)
        to_remove: List[Choice] = []
        collect_desc(choice, to_remove)
        for ch in to_remove:
            if ch in self.choices:
                self.choices.remove(ch)
        choice.children.clear()

    def _find_choice_at(self, x: float, y: float) -> Optional[Choice]:
        # Iterate from topmost to bottom
        for c in reversed(self.choices):
            if c.is_point_inside(x, y):
                return c
        return None

    def _handle_choice_selection(self, choice: Choice):
        self._log_event("select", {"label": choice.label, "level": choice.level, "selected": choice.selected})
        self._agent_say("select", {"label": choice.label, "level": choice.level, "selected": choice.selected})
        self.status_var.set(f"Selected: {choice.label} = {choice.selected}")

    def _reset_choices(self):
        self._create_initial_choices()
        self._log_event("reset", {})
        self._agent_say("reset", {})

    # ----- Logging -----
    def _log_event(self, etype: str, data: Dict[str, Any]):
        entry = {"t": time.time(), "type": etype, **data}
        self.log.append(entry)
        self.log_text.configure(state="normal")
        self.log_text.insert("end", json.dumps(entry) + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _agent_say(self, event: str, payload: Dict[str, Any]):
        msg = self.agent.respond(event, payload)
        self.agent_text.configure(state="normal")
        self.agent_text.insert("end", msg + "\n")
        self.agent_text.see("end")
        self.agent_text.configure(state="disabled")

    # ----- ND extension hooks -----
    def add_nd_dimension(self, name: str, renderer: Callable[[tk.Canvas, List[Choice]], None]):
        """Register an additional N-dimensional renderer that can draw overlays or
        additional interaction layers. For now this is a placeholder; call renderer
        immediately with current choices.
        """
        renderer(self.canvas, self.choices)

    def start_agent_dialog(self, context: Dict[str, Any]):
        """Placeholder for agent-driven dialog modules. Integrate a modal or sidebar
        that queries the agent and collects structured user input.
        """
        messagebox.showinfo("Aletheia dialog", f"Starting dialog with context: {context}")


def main():
    root = tk.Tk()
    app = SpiralWindow(root)
    messagebox.showinfo(
        "Spiral OS",
        "Interactive choice primitives demo:\n\n"
        "- Click: expand/collapse or select leaves\n"
        "- Hover: see agent hints\n"
        "- Reset: ESC or button\n\n"
        "Future: ND overlays and agent dialogs via modular hooks."
    )
    root.mainloop()


if __name__ == "__main__":
    main()
