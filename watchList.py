import tkinter as tk
import json
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.data_list = []
        self.load_data()

    def create_widgets(self):
        self.name_label = tk.Label(self)
        self.name_label["text"] = "Name:"
        self.name_label.pack(side="top")

        self.name_entry = tk.Entry(self)
        self.name_entry.pack(side="top")

        self.price_label = tk.Label(self)
        self.price_label["text"] = "Price:"
        self.price_label.pack(side="top")

        self.price_entry = tk.Entry(self)
        self.price_entry.pack(side="top")

        self.submit_button = tk.Button(self)
        self.submit_button["text"] = "Submit"
        self.submit_button["command"] = self.submit
        self.submit_button.pack(side="top")

        self.listbox = tk.Listbox(self)
        self.listbox.pack(side="top")
        #show data when a list item is selected
        self.listbox.bind("<<ListboxSelect>>", self.show_data)

        self.delete_button = tk.Button(self)
        self.delete_button["text"] = "Delete"
        self.delete_button["command"] = self.delete_data
        self.delete_button.pack(side="top")

        self.save_button = tk.Button(self)
        self.save_button["text"] = "Save"
        self.save_button["command"] = self.save_data
        self.save_button.pack(side="top")

    def submit(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        data = {"name": name, "price": price}
        # replace the item with the same name
        for i, item in enumerate(self.data_list):
            if item["name"] == name:
                self.data_list[i] = data
                self.listbox.delete(i)
                self.listbox.insert(i, json.dumps(data))
                return
        # if no item with the same name, append to the list
        self.data_list.append(data)
        self.listbox.insert(tk.END, json.dumps(data))
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    def show_data(self, event):
        selected_index = self.listbox.curselection()[0]
        selected_data = self.data_list[selected_index]
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.name_entry.insert(0, selected_data["name"])
        self.price_entry.insert(0, selected_data["price"])

    def delete_data(self):
        selected_index = self.listbox.curselection()[0]
        if selected_index != ():
            self.data_list.pop(selected_index)
            self.listbox.delete(selected_index)

    def save_data(self):
        with open("watchlist.json", "w") as f:
            json.dump(self.data_list, f)

    def load_data(self):
        if os.path.exists("watchlist.json") and  os.stat("watchlist.json").st_size > 0:
            with open("watchlist.json","r") as f:
                self.data_list = json.loads(f.read())
                print("Data list: ")
                print(self.data_list)
                for data in self.data_list:
                    self.listbox.insert(tk.END, json.dumps(data))

root = tk.Tk()
app = Application(master=root)
app.mainloop()