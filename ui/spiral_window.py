#!/usr/bin/env python3
"""
Spiral Window - Minimal UI Prototype for Spiral OS

This prototype demonstrates the core concept of choice primitives in a visual interface.
It presents a simple window with selectable 2D choices that can spiral into deeper
levels of interaction.

Dependencies:
- tkinter (usually comes with Python)
- Pillow (pip install pillow)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math


class Choice:
    """Represents a single choice primitive in the system."""
    
    def __init__(self, label, x, y, level=0, parent=None):
        self.label = label
        self.x = x
        self.y = y
        self.level = level
        self.parent = parent
        self.children = []
        self.selected = False
        self.radius = 40 - (level * 5)  # Smaller at deeper levels
        
    def add_child(self, choice):
        """Add a child choice that spirals from this one."""
        self.children.append(choice)
        
    def is_point_inside(self, px, py):
        """Check if a point is inside this choice circle."""
        distance = math.sqrt((px - self.x) ** 2 + (py - self.y) ** 2)
        return distance <= self.radius


class SpiralWindow:
    """Main window for Spiral OS UI prototype."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Spiral OS - Choice Primitive Interface")
        self.root.geometry("800x600")
        
        # State
        self.choices = []
        self.expanded_choice = None
        self.hover_choice = None
        
        # Setup UI
        self._setup_ui()
        self._create_initial_choices()
        
    def _setup_ui(self):
        """Initialize the user interface components."""
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(
            header_frame, 
            text="Spiral OS - Choice Primitive Demo",
            font=("Arial", 14, "bold")
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            header_frame,
            text="Reset",
            command=self._reset_choices
        ).pack(side=tk.RIGHT)
        
        # Canvas for drawing choices
        self.canvas = tk.Canvas(
            self.root,
            bg="#1e1e1e",
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Event bindings
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<Motion>", self._on_canvas_motion)
        
        # Info panel
        info_frame = ttk.Frame(self.root)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.info_label = ttk.Label(
            info_frame,
            text="Click on a choice to spiral into more options. Hover to see details.",
            foreground="#666"
        )
        self.info_label.pack()
        
    def _create_initial_choices(self):
        """Create the initial set of root choices."""
        # Clear existing
        self.choices = []
        self.expanded_choice = None
        
        # Create root-level choices in a circular pattern
        center_x = 400
        center_y = 300
        radius = 150
        
        root_choices = [
            "File System",
            "Applications",
            "Settings",
            "Network",
            "Agents"
        ]
        
        num_choices = len(root_choices)
        for i, label in enumerate(root_choices):
            angle = (2 * math.pi * i) / num_choices - (math.pi / 2)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            choice = Choice(label, x, y, level=0)
            self.choices.append(choice)
            
        self._draw_choices()
        
    def _create_spiral_children(self, parent_choice):
        """Create child choices in a spiral pattern from a parent."""
        # Define child choices based on parent
        child_labels = {
            "File System": ["Browse", "Search", "Recent", "Favorites"],
            "Applications": ["Launch", "Install", "Update", "Manage"],
            "Settings": ["Display", "Privacy", "System", "Accounts"],
            "Network": ["Connect", "Status", "VPN", "Share"],
            "Agents": ["Aletheia", "Monitor", "Orchestrate", "Configure"]
        }
        
        labels = child_labels.get(parent_choice.label, ["Option A", "Option B", "Option C"])
        
        # Create children in a spiral
        num_children = len(labels)
        spiral_radius = 80
        
        for i, label in enumerate(labels):
            angle = (2 * math.pi * i) / num_children + (parent_choice.level * 0.5)
            x = parent_choice.x + spiral_radius * math.cos(angle)
            y = parent_choice.y + spiral_radius * math.sin(angle)
            
            child = Choice(label, x, y, level=parent_choice.level + 1, parent=parent_choice)
            parent_choice.add_child(child)
            self.choices.append(child)
            
    def _draw_choices(self):
        """Render all choices on the canvas."""
        self.canvas.delete("all")
        
        # Draw connections first (so they appear behind circles)
        for choice in self.choices:
            if choice.parent:
                self.canvas.create_line(
                    choice.parent.x, choice.parent.y,
                    choice.x, choice.y,
                    fill="#444",
                    width=2
                )
        
        # Draw choices
        for choice in self.choices:
            # Determine color based on state
            if choice == self.hover_choice:
                fill_color = "#4a9eff"
                outline_color = "#6db3ff"
            elif choice.selected:
                fill_color = "#2d7a3e"
                outline_color = "#3d9a5e"
            elif choice == self.expanded_choice:
                fill_color = "#7a2d7a"
                outline_color = "#9a3d9a"
            else:
                # Color by level
                colors = ["#3a3a3a", "#4a4a4a", "#5a5a5a"]
                fill_color = colors[min(choice.level, len(colors) - 1)]
                outline_color = "#6a6a6a"
            
            # Draw circle
            self.canvas.create_oval(
                choice.x - choice.radius,
                choice.y - choice.radius,
                choice.x + choice.radius,
                choice.y + choice.radius,
                fill=fill_color,
                outline=outline_color,
                width=2
            )
            
            # Draw label
            self.canvas.create_text(
                choice.x,
                choice.y,
                text=choice.label,
                fill="white",
                font=("Arial", 10 if choice.level == 0 else 8)
            )
            
    def _on_canvas_click(self, event):
        """Handle click events on the canvas."""
        clicked_choice = self._find_choice_at(event.x, event.y)
        
        if clicked_choice:
            if clicked_choice == self.expanded_choice:
                # Collapse: remove children
                self._collapse_choice(clicked_choice)
                self.expanded_choice = None
            else:
                # Expand: add children if not already present
                if not clicked_choice.children:
                    self._create_spiral_children(clicked_choice)
                    self.expanded_choice = clicked_choice
                else:
                    # Toggle selection
                    clicked_choice.selected = not clicked_choice.selected
                    self._handle_choice_selection(clicked_choice)
                    
            self._draw_choices()
            
    def _on_canvas_motion(self, event):
        """Handle mouse motion for hover effects."""
        new_hover = self._find_choice_at(event.x, event.y)
        
        if new_hover != self.hover_choice:
            self.hover_choice = new_hover
            
            if new_hover:
                info_text = f"Choice: {new_hover.label} (Level {new_hover.level})"
                if new_hover.children:
                    info_text += f" - {len(new_hover.children)} sub-choices"
                self.info_label.config(text=info_text)
            else:
                self.info_label.config(
                    text="Click on a choice to spiral into more options. Hover to see details."
                )
                
            self._draw_choices()
            
    def _find_choice_at(self, x, y):
        """Find the choice at given coordinates."""
        # Search in reverse order (topmost first)
        for choice in reversed(self.choices):
            if choice.is_point_inside(x, y):
                return choice
        return None
        
    def _collapse_choice(self, choice):
        """Remove a choice's children from the display."""
        # Recursively remove all descendants
        for child in choice.children:
            self._collapse_choice(child)
            if child in self.choices:
                self.choices.remove(child)
        choice.children = []
        
    def _handle_choice_selection(self, choice):
        """Handle when a choice is selected."""
        if choice.selected:
            messagebox.showinfo(
                "Choice Selected",
                f"You selected: {choice.label}\n\n"
                f"In a full Spiral OS implementation, this would:\n"
                f"- Trigger an Aletheia agent action\n"
                f"- Update system state through choice primitives\n"
                f"- Coordinate with other system components"
            )
        
    def _reset_choices(self):
        """Reset to initial choice state."""
        self._create_initial_choices()


def main():
    """Entry point for the spiral window demo."""
    root = tk.Tk()
    app = SpiralWindow(root)
    
    # Add welcome message
    messagebox.showinfo(
        "Welcome to Spiral OS",
        "This is a minimal prototype demonstrating choice primitives.\n\n"
        "Features:\n"
        "• Click choices to spiral into sub-choices\n"
        "• Hover to see information\n"
        "• Click expanded choices to collapse them\n"
        "• Click leaf choices to select them\n\n"
        "This will evolve into a full OS interface!"
    )
    
    root.mainloop()


if __name__ == "__main__":
    main()
