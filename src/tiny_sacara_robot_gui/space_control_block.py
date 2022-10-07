import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox

from PIL import Image, ImageTk



class ControlBlock(tk.Frame):

    def __init__(self, container: tk.Tk, name: str, init_value: float, upper_bound=float("inf"), lower_bound=float("-inf")):
        tk.Frame.__init__(self, container, padx=10, pady=10)
        self._container = container
        self._name = name
        self._value = init_value
        self._upper_bound = upper_bound
        self._lower_bound = lower_bound

        self._font_small = font.Font(size=12)
        self._font_small_bold = font.Font(size=12, weight="bold")

        self.draw_control_block()
        self.set_value(self._value)
        

    def draw_control_block(self):
        style = ttk.Style()
        style.configure("TButton", font=self._font_small_bold)

        #Widgets in the base frame
        self.label = ttk.Label(self, justify=tk.CENTER, text=self._name, font=self._font_small)
        self.entry = ttk.Entry(self, width=8, justify=tk.CENTER, font=self._font_small)
        self.entry.bind("<KeyRelease-Return>", self.validate_entry_on_update)
        decrease_button_text = "-"
        increase_button_text = "+"
        self.decrease_button = ttk.Button(self, text=decrease_button_text, width=1, style="TButton",
                                          command=(lambda: self.change_value_on_click(decrease_button_text))
                                         )
        self.increase_button = ttk.Button(self, text=increase_button_text, width=1, style="TButton",
                                          command=(lambda: self.change_value_on_click(increase_button_text))
                                         )
        
        #Laying out the base frame
        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=4)

        self.label.grid(row=0, columnspan=3,)
        self.entry.grid(row=1, columnspan=3, pady=(5,10), sticky="nsew")
        self.decrease_button.grid(row=2, column=0, sticky="nsew")
        self.increase_button.grid(row=2, column=2, sticky="nsew")


    #Getters and Setters
    def get_value(self) -> float:
        return self._value

    def set_value(self, value):
        #check bounds
        if value > self._upper_bound:
            value = self._upper_bound
        elif value < self._lower_bound:
            value = self._lower_bound
        #set the value and update the entry widget
        self._value = value
        self.entry.delete(0, tk.END)
        self.entry.insert(0, f"{value:.2f}")

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str):
        self._name = name


    #Class methods
    def validate_entry_on_update(self, event):
        entry = self.entry.get()
        try:
            entry = float(entry)
            self.set_value(entry)
        except ValueError:
            #restor previous value
            self.set_value(self._value)
            tk.messagebox.showwarning(title="Invalid input", message="The previous value has been restored.")
        self.focus()
       
    def change_value_on_click(self, caption: str):
        # multiplier: float = Test.get_multiplier(self)
        if caption == "+":
            self.set_value(self._value + 1 * MainWindow.get_multiplier(app))
        elif caption == "-":
            self.set_value(self._value - 1 * MainWindow.get_multiplier(app))



class MainWindow(tk.Frame):
    def __init__(self, container: tk.Tk, theme: str="light"):
        tk.Frame.__init__(self, container)
        self._container = container
        self._multiplier = 1
        self._joint_value_list = [0.0,0.0,0.0]

        #Set theme Azure: https://github.com/rdbende/Azure-ttk-theme/tree/gif-based/
        self._theme = theme
        self.tk.call("source", "theme/azure/azure.tcl")
        self.tk.call("set_theme", self._theme)

        #Set styles
        self.font_medium = font.Font(size=14, weight="bold")

        #drawing main GUI
        self.draw_main_gui()
        self.update_robot_sim()

    def draw_main_gui(self):
        self.group_control_block(self, "JOINTS", ["AXIS 1", "AXIS 2", "AXIS 3"])

    def group_control_block(self, container, title: str, block_label_list: list[str]):
        s = ttk.Style()
        s.configure("TLabelframe.Label", font=self.font_medium)
        self.group_control_block_frame = ttk.Labelframe(container, text=title) # style="TLabelframe"
        self.group_control_block_frame.pack(side=tk.LEFT)
        self.group_control_block_frame.bind("<Button-1>", self.click_test)

        i = 1
        for label in block_label_list:
            name = f"control_block_{i}"
            self.name = ControlBlock(self.group_control_block_frame, label, 0.0)
            self.name.pack(side=tk.LEFT)
            i += 1

    def get_multiplier(self) -> float:
        return self._multiplier

    def update_robot_sim(self, value=0):
        pass

    def click_test(self, event):
        self.update_robot_sim(1)



#Test main Script
if __name__ == "__main__":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        #Init
        root = tk.Tk()
        root.minsize(500, 300)
        root.title("TinyScara Manager GUI")
        app = MainWindow(root, "light")
        app.pack(fill="both", expand=True)
        #Icon
        ico = Image.open("assets\icon_tiny_scara_resized.png")
        photo = ImageTk.PhotoImage(ico)
        root.wm_iconphoto(False, photo)
        # root.iconbitmap("assets\icon_tiny_scara_resized.ico")
        #Main loop
        root.mainloop()