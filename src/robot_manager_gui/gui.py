import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox


class ControlBlock(tk.Frame):

    def __init__(self, parent: tk.Tk, name: str, init_value: float, upper_bound=float("inf"), lower_bound=float("-inf")):
        tk.Frame.__init__(self, parent, padx=10)
        self._name = name
        self._value = init_value
        self._upper_bound = upper_bound
        self._lower_bound = lower_bound

        self._font_small = font.Font(size=12)
        self._font_small_bold = font.Font(size=12, weight="bold")
        self._font_medium = font.Font(size=14)
        self._font_big = font.Font(size=16)

        self.draw_control_block()
        self.set_value(self._value)
        

    def draw_control_block(self):
        style = ttk.Style()
        style.configure("TButton", font=self._font_small_bold)

        #Widgets in the base frame
        self.label = ttk.Label(self, justify=tk.CENTER, text=self._name, font=self._font_medium)
        self.entry = ttk.Entry(self, width=8, justify=tk.CENTER, font=self._font_small)
        self.entry.bind("<KeyRelease-Return>", self.validate_entry_on_update)
        decrease_button_text = "+"
        increase_button_text = "-"
        self.decrease_button = ttk.Button(
                                          self, text=decrease_button_text, width=1, style="TButton",
                                          command=(lambda: self.change_value_on_click(decrease_button_text))
                                         )
        self.increase_button = ttk.Button(
                                          self, text=increase_button_text, width=1, style="TButton",
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
            self.set_value(self._value + 1 * Test.get_multiplier(test))
        elif caption == "-":
            self.set_value(self._value - 1 * Test.get_multiplier(test))



class Test(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.tk.call("source", "theme/azure/azure.tcl")
        self.tk.call("set_theme", "dark")
        self.pack_test()
        self.multiplier = 10

    def pack_test(self):
        self.control_block1 = ControlBlock(self, "Name1", 0.0, 35.7, -12.2)
        self.control_block2 = ControlBlock(self, "Name2", 0.0, 12, -27)
        self.control_block1.pack(padx=5, pady=(5,10), side=tk.LEFT)
        self.control_block2.pack(padx=5, pady=(5,10), side=tk.LEFT)

    def get_multiplier(self) -> float:
        return self.multiplier


#Test main Script
if __name__ == "__main__":
    root = tk.Tk()
    test = Test(root)
    test.pack(fill="both", expand=True)
    root.mainloop()
