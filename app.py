from owlready2 import get_ontology, sync_reasoner_pellet
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk  

# Load Ontology
ontology_path = "GeometryOntology.owl"  
ontology = get_ontology(ontology_path).load()

sync_reasoner_pellet()

# GUI Class
class GeometryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Geometry - An Intelligent Tutoring System")
        self.root.geometry("450x600")  
        self.root.configure(bg="#C5E1F8")
        self.create_widgets()

    def create_widgets(self):
        # Logo at the top
        img = Image.open("logo.png")  
        img = img.resize((300, 300), Image.Resampling.LANCZOS)
        self.logo = ImageTk.PhotoImage(img)
        tk.Label(self.root, image=self.logo, bg="#C5E1F8").pack(pady=5)

        # Dropdown for shape selection
        tk.Label(self.root, text="Select a Shape:", font=("Arial", 12), bg="#C5E1F8").pack()
        self.selected_shape = tk.StringVar()
        self.shape_menu = ttk.Combobox(self.root, textvariable=self.selected_shape, state="readonly")
        self.shape_menu.pack(pady=5)
        self.shape_menu.bind("<<ComboboxSelected>>", self.update_parameter_fields)

        # Input Frame
        self.input_frame = tk.Frame(self.root, bg="#C5E1F8")
        self.input_frame.pack(pady=10)
        self.entries = {}

        # Calculate Button
        self.calc_button = tk.Button(self.root, text="Calculate", bg="blue", fg="white", font=("Arial", 12),
                                     command=self.calculate)
        self.calc_button.pack(pady=10)

        # Result Label
        self.result_label = tk.Label(self.root, text="Result:", font=("Arial", 12), bg="#C5E1F8")
        self.result_label.pack(pady=5)

        # Populate dropdown
        self.populate_shapes()

    def populate_shapes(self):
        # Add shape options
        self.shape_menu["values"] = ["Circle", "Cube", "Sphere", "Square", "Triangle"]

   

    def update_parameter_fields(self, event):
        # Clear previous fields
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        self.entries = {}
        shape = self.selected_shape.get()
        parameters = []

        # Define input fields based on shape
        if shape == "Circle":
            parameters = [("Radius (r):", "r")]
        elif shape == "Cube":
            parameters = [("Side Length:", "side")]
        elif shape == "Sphere":
            parameters = [("Radius (r):", "r")]
        elif shape == "Square":
            parameters = [("Side Length:", "side")]
        elif shape == "Triangle":
            parameters = [("Base:", "base"), ("Height:", "height")]

        # Create input fields
        for label, var_name in parameters:
            tk.Label(self.input_frame, text=label, font=("Arial", 10), bg="#C5E1F8").pack()
            entry = tk.Entry(self.input_frame)
            entry.pack(pady=5)
            self.entries[var_name] = entry

    def calculate(self):
        
        formulas = {
            "Circle": "3.14 * r ** 2",
            "Cube": "side ** 3",
            "Sphere": "4 / 3 * 3.14 * r ** 3",
            "Square": "side ** 2",
            "Triangle": "0.5 * base * height"
        }

        # Result text mappings
        result_texts = {
            "Circle": "Area of Circle:",
            "Cube": "Volume of Cube:",
            "Sphere": "Volume of Sphere:",
            "Square": "Area of Square:",
            "Triangle": "Area of Triangle:"
        }

        shape = self.selected_shape.get()
        formula = formulas.get(shape)
        result_label = result_texts.get(shape, "Result:")

        if not formula:
            messagebox.showerror("Error", f"No formula available for '{shape}'")
            return

        try:
            # Get input variables and evaluate formula
            variables = {var: float(entry.get()) for var, entry in self.entries.items()}
            result = eval(formula, {}, variables)
            self.result_label.config(text=f"{result_label} {result:.2f}")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input or calculation error: {e}")

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = GeometryApp(root)
    root.mainloop()
