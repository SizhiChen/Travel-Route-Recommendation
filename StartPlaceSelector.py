import ttkbootstrap as tb
from tkinter import messagebox

class StartPlaceSelector:
    def __init__(self, parent, gmaps_client, set_start_point, set_start_text):
        self.parent = parent
        self.gmaps = gmaps_client
        self.set_start_point = set_start_point
        self.set_start_text = set_start_text
        self.start_place_candidates = []
        self.selected_start_place = None

        # ====== New Window Setup ======
        self.window = tb.Toplevel(self.parent)
        self.window.title("Choose Start Place")
        window_width = 700
        window_height = 500
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.window.configure(background="#F4FAFD")
        # Stay at top
        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.focus()

        # ====== Style Setup ======
        self.style = tb.Style()
        self.style.configure('HeaderH1.TLabel', background='#0279B1',
                             font=('Times New Roman', 20, 'bold'), foreground='white')

        # ====== Header ======
        self.header = tb.Frame(self.window, style='Header.TFrame', padding=10)
        self.header.pack(fill='x')
        tb.Label(self.header, text="Search for Start Place",
                 style='HeaderH1.TLabel', anchor='center', justify='center').pack(fill='x')

        # ====== Input Area ======
        self.input = tb.Frame(self.window, style='Other.TFrame', padding=10)
        self.input.pack(anchor='center')

        tb.Label(self.input, text="Enter Address:", style='Other.TLabel',
                 font=('Times New Roman', 12, 'bold')).grid(row=0, column=0, sticky='w')
        self.entry = tb.Entry(self.input, width=50)
        self.entry.grid(row=0, column=1, padx=10)
        self.search_btn = tb.Button(self.input, text="Search")
        self.search_btn.configure(command=self.search_place)
        self.search_btn.grid(row=0, column=2, padx=10)

        # ====== Scroll Area ======
        self.result = tb.Frame(self.window, style='Other.TFrame', padding=5)
        self.result.pack(fill='x')

        # ------ Treeview ------
        columns = ("name", "address")
        self.tree = tb.Treeview(self.result, columns=columns, show='headings', height=10)
        self.tree.pack(fill='x', padx = 10)
        self.tree.bind("<<TreeviewSelect>>", self.change_confirm_text)
        # Set header, size and color
        self.tree.heading("name", text="Name")
        self.tree.heading("address", text="Address")
        self.tree.column("name", width=200)
        self.tree.column("address", width=400)
        self.tree.tag_configure('odd_row', background='#f0f0f0')
        self.tree.tag_configure('even_row', background='white')

        # ====== Confirm Area ======
        self.confirm = tb.Frame(self.window, style='Other.TFrame', padding=10)
        self.confirm.pack(fill='x')

        # ------ Confirm Grid ------
        self.confirm_text = tb.Label(self.confirm, text="Please Select a Start Place", anchor='center',
                                     style='Other.TLabel', font=('Times New Roman', 12, 'bold'))
        self.confirm_text.grid(row=0, column=0, sticky='w', padx=5)
        self.confirm_btn = tb.Button(self.confirm, text="Confirm", width=20, style='Preference.TButton')
        self.confirm_btn.grid(row=0, column=1, sticky='e', padx=10)
        self.confirm_btn.configure(command=self.confirm_start_place)
        self.confirm.columnconfigure(0, weight=1)
        self.confirm.columnconfigure(1, weight=0)

    def search_place(self):
        query = self.entry.get().strip()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a keyword.")
            return

        try:
            response = self.gmaps.places(query=query, location=(49.2827, -123.1207), radius=10000)
            results = response.get("results", [])[:10]
            self.start_place_candidates = results

            # Update TreeView
            for row in self.tree.get_children():
                self.tree.delete(row)

            for idx, place in enumerate(results):
                name = place.get('name', 'Unknown')
                address = place.get('formatted_address', 'N/A')
                tag = 'even_row' if idx % 2 == 0 else 'odd_row'
                self.tree.insert('', 'end', values=(name, address), tags=(tag,))

        except Exception as e:
            messagebox.showwarning("Error", f"Failed to search: {e}")

    def confirm_start_place(self):
        if not self.selected_start_place:
            messagebox.showwarning("No Selection", "Please select a place first.")
            return
        # Set start_point in searchUI
        self.set_start_point(self.selected_start_place)
        self.set_start_text(self.selected_start_place)
        # Turn off the Start Place window
        self.window.destroy()

    def change_confirm_text(self, event):
        if not self.tree.selection():
            return

        item = self.tree.item(self.tree.selection()[0])
        name, address = item['values']
        self.selected_start_place = name
        self.confirm_text.config(text=f"{name}\n{address}")




