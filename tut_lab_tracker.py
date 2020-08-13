import tkinter as tk
from tkinter.colorchooser import askcolor

class Module_Info():
    def __init__(self,root_window,mod_code,mod_color,slot_code,slot_color):
        '''
        root_window = Parent Frame for the module frame
        mod_code = String containing module code (manually entered by user)
        mod_color = String containing hex color of background for module code label
        slot_code = String containing name of tutorial/lab slot (manually entered by user)
        '''
        self.frame = tk.Frame(root_window,borderwidth=1,padx=4,pady=4)
        self.mod_code = mod_code
        self.mod_color = mod_color
        self.slot_code = slot_code
        self.slot_color = slot_color
        self.setup_pack_widgets()

    def setup_pack_widgets(self):
        mod_label = tk.Label(master=self.frame,text=self.mod_code,bg=self.mod_color,height=3)
        slot_label = tk.Label(master=self.frame,text=self.slot_code,bg=self.slot_color,height=3)
        mod_label.pack(side=tk.LEFT)
        slot_label.pack(side=tk.LEFT)

    def remove(self):
        self.frame.destroy()

class MainApp():
    def __init__(self):
        self.page = tk.Tk()
        self.page.title("Tut/Lab Slot Tracker")
        self.page.resizable(False,True)
        self.mod_slots = []

        self.setup_slot_adder()
        self.setup_slot_holder()
        self.pack_widgets()
        self.page.mainloop()

    def setup_slot_adder(self):
        self.slot_adder_container = tk.Frame(master=self.page,borderwidth=3,relief=tk.RIDGE,width=300)
        self.slot_adder = tk.Frame(master=self.slot_adder_container,width=300)
        intro_label = tk.Label(master=self.slot_adder,name="intro_label",text="Add tutorial/lab slots here:")
        mod_code_label = tk.Label(master=self.slot_adder,name="mod_code_label",text="Module Code",fg="black")
        mod_code_entry = tk.Entry(master=self.slot_adder,name="mod_code_entry")
        slot_code_label = tk.Label(master=self.slot_adder,name="slot_code_label",text="Tut/Lab slot",fg="black")
        slot_code_entry = tk.Entry(master=self.slot_adder,name="slot_code_entry")
                
        def color_chooser(color_box):
            color = askcolor()[1]
            if color is not None:
                color_box.config(bg=color)

        mod_color = tk.Label(master=self.slot_adder,name="mod_color",bg="#add8e6",width=8,height=1,borderwidth=1,relief=tk.GROOVE)
        mod_color.bind("<Button-1>",lambda e: color_chooser(mod_color))

        slot_color = tk.Label(master=self.slot_adder,name="slot_color",bg="#ffcccb",width=8,height=1,borderwidth=1,relief=tk.GROOVE)
        slot_color.bind("<Button-1>",lambda e: color_chooser(slot_color))
        
        add_slot_button = tk.Button(master=self.slot_adder,name="add_slot_button",bg="white",text="Add slot",command=self.add_slot)

        intro_label.grid(row=0,columnspan=3)
        mod_code_label.grid(row=1,sticky=tk.E)
        slot_code_label.grid(row=2,sticky=tk.E)
        mod_code_entry.grid(row=1,column=1)
        slot_code_entry.grid(row=2,column=1)
        mod_color.grid(row=1,column=2)
        slot_color.grid(row=2,column=2)
        add_slot_button.grid(row=3,column=0,columnspan=3)

    def setup_slot_holder(self):
        self.ranking_container = tk.Frame(master=self.page,borderwidth=3,relief=tk.RIDGE,width=300)
        self.ranking_canvas = tk.Canvas(master=self.ranking_container,borderwidth=0,width=300)
        self.ranking_frame = tk.Frame(master=self.ranking_canvas,width=300)
        
        self.cont_label_var = tk.StringVar()
        self.cont_label_var.set("{} Tutorial/Lab Slots selected:".format(len(self.mod_slots)))
        cont_label = tk.Label(master=self.ranking_container,textvariable=self.cont_label_var)
        cont_label.pack(side=tk.TOP)
        
        ranking_vsb = tk.Scrollbar(self.ranking_container,orient="vertical",command=self.ranking_canvas.yview)
        self.ranking_canvas.configure(yscrollcommand=ranking_vsb.set)

        ranking_vsb.pack(side=tk.RIGHT,fill=tk.Y)
        self.ranking_canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        self.ranking_canvas.create_window((3,3),window=self.ranking_frame,anchor=tk.CENTER,tags="self.ranking_frame")
        self.ranking_frame.bind("<Configure>",self.onFrameConfigure)
    
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.ranking_canvas.configure(scrollregion=self.ranking_canvas.bbox("all"))

    def pack_widgets(self):
        self.slot_adder.pack(anchor=tk.CENTER)
        self.slot_adder_container.grid(row=0)
        self.ranking_container.grid(row=1,sticky=tk.N+tk.S+tk.E+tk.W)
        self.page.grid_rowconfigure(0,weight=1)
        self.page.grid_rowconfigure(1,weight=10)

    def add_slot(self):
        inputs = self.slot_adder.children
        mod_code = inputs['mod_code_entry'].get()
        slot_code = inputs['slot_code_entry'].get()
        mod_color = inputs['mod_color'].cget("background")
        slot_color = inputs['slot_color'].cget("background")
        slot_frame = tk.Frame(master=self.ranking_frame,relief=tk.RIDGE,borderwidth=3,pady=4,width=160,height=75)
        
        slot = Module_Info(slot_frame,mod_code,mod_color,slot_code,slot_color)
        remove_slot_button = tk.Button(master=slot_frame,bg="white",text='del',command=lambda :self.delete_slot(slot_frame),height=2,width=4)
        
        slot_move_subframe = tk.Frame(master=slot_frame)
        move_slot_up_button = tk.Button(master=slot_move_subframe,bg="white",text='up',command=lambda :self.move_slot(slot_frame,'up'),height=1,width=4)
        move_slot_down_button = tk.Button(master=slot_move_subframe,bg="white",text='down',command=lambda :self.move_slot(slot_frame,'down'),height=1,width=4)
        move_slot_up_button.pack(side=tk.TOP)
        move_slot_down_button.pack(side=tk.TOP)

        remove_slot_button.pack(side=tk.LEFT)
        slot.frame.pack(side=tk.LEFT)
        slot_move_subframe.pack(side=tk.LEFT)

        self.mod_slots.append(slot_frame)
        self.refresh_mod_slots()

    def delete_slot(self,slot_frame):
        self.mod_slots.remove(slot_frame)
        slot_frame.destroy()
        self.refresh_mod_slots()

    def move_slot(self,slot_frame,direction):
        idx = self.mod_slots.index(slot_frame)
        if direction == 'up' and idx != 0:
            self.mod_slots[idx], self.mod_slots[idx-1] = self.mod_slots[idx-1], self.mod_slots[idx]
        elif direction == 'down' and idx != (len(self.mod_slots)-1):
            self.mod_slots[idx], self.mod_slots[idx+1] = self.mod_slots[idx+1], self.mod_slots[idx]
        self.refresh_mod_slots()

    
    def refresh_mod_slots(self):
        for mod_slot in self.mod_slots:
            mod_slot.forget()
        for mod_slot in self.mod_slots:
            mod_slot.pack(side=tk.TOP,anchor=tk.CENTER)
        self.cont_label_var.set("{} Tutorial/Lab Slots selected:".format(len(self.mod_slots)))

if __name__ == '__main__':
    MainApp_window = MainApp()

