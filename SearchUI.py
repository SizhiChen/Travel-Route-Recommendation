# SearchUI.py
import webbrowser
from tkinter import messagebox
from main import gmaps
from StartPlaceSelector import StartPlaceSelector
from tsp_solver import get_distance_matrix, tsp, get_route_url
import ttkbootstrap as tb
import webview

class SearchUI:

    def __init__(self, root, attraction_data):
        self.root = root
        self.attractionData = attraction_data
        self.selected_places_list = []
        self.search_results = None
        self.start_point = None
        self.cached = {}

        # ====== Window Setup ======
        window_width = 1000
        window_height = 750
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.title('Search UI')
        self.root.configure(background="#F4FAFD")

        # ====== Style Setup ======
        self.style = tb.Style()
        self.style.configure('Header.TFrame', background='#0279B1')
        self.style.configure('HeaderH1.TLabel', background='#0279B1',
                        font=('Times New Roman', 30, 'bold'), foreground='white')
        self.style.configure('Other.TFrame', background='#F4FAFD')
        self.style.configure('Other.TLabel', background='#F4FAFD')
        self.style.configure('Preference.TLabel', background='#F4FAFD',
                             font=('Times New Roman', 18, 'bold'))
        self.style.configure('Preference.TButton', font=('Times New Roman', 12, 'bold'),)
        self.style.configure('Address.TLabel', background='#F4FAFD',
                             font=('Times New Roman', 12))
        self.style.configure('Treeview', font=('Times New Roman', 11), rowheight=28)
        self.style.configure('Treeview.Heading', font=('Times New Roman', 12, 'bold'))
        self.style.configure('Button.TButton', background='#F4FAFD', relief='sunken')
        # self.style.configure('Test.TFrame', background='green')

        # ====== Header ======
        self.header = tb.Frame(self.root, style='Header.TFrame', padding=20)
        self.header.pack(fill='x')
        tb.Label(self.header, text="Travel Route Recommendation!!",
                  style='HeaderH1.TLabel', anchor='center', justify='center').pack(fill='x')

        # ====== Input Area ======
        self.input = tb.Frame(self.root, style='Other.TFrame', padding=10)
        self.input.pack(anchor='center')

        tb.Label(self.input, text="Enter Address:", style='Other.TLabel',
                  font=('Times New Roman', 15, 'bold')).grid(row=0, column=0, sticky='w')
        self.entry = tb.Entry(self.input, width=50)
        self.entry.grid(row=0, column=1, padx=10)
        self.search_btn = tb.Button(self.input, text="Search")
        self.search_btn.bind('<Button-1>', self.search_place)
        self.search_btn.grid(row=0, column=2, padx=10)

        # ====== Display Area ======
        self.display = tb.Frame(self.root, style='Other.TFrame', padding=10)
        self.display.pack(fill='both', expand=True)
        # Grid configuration
        self.display.columnconfigure(0, weight=1)
        self.display.columnconfigure(1, weight=1)
        self.display.columnconfigure(2, weight=1)
        self.display.rowconfigure(0, weight=1)
        # Labels filling their grid cells
        self.chose1 = tb.Label(self.display, text=" \n \n ", anchor='center', style='Other.TLabel',
                               wraplength=250,)
        self.chose1.grid(row=0, column=0, sticky='nsew')
        self.chose2 = tb.Label(self.display, text=" \n \n ", anchor='center', style='Other.TLabel',
                               wraplength=250,)
        self.chose2.grid(row=0, column=1, sticky='nsew')
        self.chose3 = tb.Label(self.display, text=" \n \n ", anchor='center', style='Other.TLabel',
                               wraplength=250,)
        self.chose3.grid(row=0, column=2, sticky='nsew')

        # ====== Separator ======
        separator = tb.Separator(self.root, orient='horizontal')
        separator.pack(fill='x')

        # ====== Preference Area ======
        self.preference = tb.Frame(self.root, style='Other.TFrame')
        self.preference.pack(fill='x', expand=True)
        tb.Label(self.preference, text="Selected Preference", anchor='center', style='Preference.TLabel'
                 ).grid(row=0, column=0, columnspan=5, sticky='nsew', pady=(0, 10))

        # Set equal weight to each column for center alignment
        for i in range(5):
            self.preference.columnconfigure(i, weight=1)

        # Equal width buttons
        self.art_btn = tb.Button(self.preference, text="ART", width=20, style='Preference.TButton')
        self.culture_btn = tb.Button(self.preference, text="CULTURE", width=20, style='Preference.TButton')
        self.nature_btn = tb.Button(self.preference, text="NATURE", width=20, style='Preference.TButton')
        self.entertainment_btn = tb.Button(self.preference, text="ENTERTAINMENT", width=20, style='Preference.TButton')
        self.food_btn = tb.Button(self.preference, text="FOOD", width=20, style='Preference.TButton')

        self.art_btn.grid(row=1, column=0, padx=10)
        self.culture_btn.grid(row=1, column=1, padx=10)
        self.nature_btn.grid(row=1, column=2, padx=10)
        self.entertainment_btn.grid(row=1, column=3, padx=10)
        self.food_btn.grid(row=1, column=4, padx=10)

        self.art_btn.config(command=lambda: self.filter_places_by_category('art'))
        self.culture_btn.config(command=lambda: self.filter_places_by_category('culture'))
        self.nature_btn.config(command=lambda: self.filter_places_by_category('nature'))
        self.entertainment_btn.config(command=lambda: self.filter_places_by_category('entertainment'))
        self.food_btn.config(command=lambda: self.filter_places_by_category('food'))

        # ====== Scroll Area ======
        self.recommendation = tb.Frame(self.root, style='Other.TFrame', padding=5)
        self.recommendation.pack(fill='x')
        tb.Label(self.recommendation, text="Recommended  Places", style='Other.TLabel',
                  font=('Times New Roman', 12, 'bold')).grid(
            row=0, column=0, columnspan=2, sticky='n', pady=(0, 5))
        tb.Label(self.recommendation, text="Selected  Places", style='Other.TLabel',
                  font=('Times New Roman', 12, 'bold')).grid(
            row=0, column=2, columnspan=2, sticky='n', pady=(0, 5))

        # Make grid layout stretchable
        self.recommendation.columnconfigure(0, weight=1)
        self.recommendation.columnconfigure(2, weight=1)

        # ------ Treeview 1 - Recommendation ------
        columns = ("name", "rating", "reviews")
        self.tree = tb.Treeview(self.recommendation, columns=columns, show="headings", height=10)
        self.tree.grid(row=1, column=0, sticky='nsew', padx=5)
        self.tree.bind("<Double-Button-1>", self.add_selected_place_from_recommendation)

        scrollbar = tb.Scrollbar(self.recommendation, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.heading("name", text="Name")
        self.tree.heading("rating", text="Rating")
        self.tree.heading("reviews", text="Review Count")
        self.tree.column("name", width=250)
        self.tree.column("rating", width=70, anchor='center')
        self.tree.column("reviews", width=100, anchor='center')

        self.tree.tag_configure('oddrow', background='white')
        self.tree.tag_configure('evenrow', background='#f0f0f0')

        for idx, row in self.attractionData.iterrows():
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            name = row["Place_Name"]
            rating = row["Rating"]
            reviews = f"{int(row['User_Ratings']):,}"
            self.tree.insert('', tb.END, values=(name, rating, reviews), tags=(tag,))

        # ------ Treeview 2 - Selection ------
        self.tree1 = tb.Treeview(self.recommendation, columns=columns, show="headings", height=10)
        self.tree1.grid(row=1, column=2, sticky='new', padx=(20, 5))
        self.tree1.bind("<Double-Button-1>", self.remove_selected_place)

        scrollbar1 = tb.Scrollbar(self.recommendation, orient="vertical", command=self.tree1.yview)
        scrollbar1.grid(row=1, column=3, sticky='ns')
        self.tree1.configure(yscrollcommand=scrollbar1.set)
        # Set header, size and color
        self.tree1.heading("name", text="Name")
        self.tree1.heading("rating", text="Rating")
        self.tree1.heading("reviews", text="Review Count")
        self.tree1.column("name", width=250)
        self.tree1.column("rating", width=70, anchor='center')
        self.tree1.column("reviews", width=100, anchor='center')
        self.tree1.tag_configure('evenrow', background='white')
        self.tree1.tag_configure('oddrow', background='#f0f0f0')

        # ====== TSP Area ======
        self.tsp = tb.Frame(self.root, style='Other.TFrame')
        self.tsp.pack(fill='both', expand=True)

        # advise text
        self.search_text = 'We recommend to choose no more than 8 places!!'
        tb.Label(self.tsp, text=self.search_text, anchor='center', style='Preference.TLabel'
                 ).grid(row=0, column=0, columnspan=3, sticky='nsew', padx=5)

        # start place button
        self.setup_start_btn = tb.Button(self.tsp, text='Start Place', width=20, style='Preference.TButton')
        self.setup_start_btn.grid(row=1, column=0, sticky='w', padx=10)
        self.setup_start_btn.config(command=self.click_start_place)

        # start place text
        self.setup_start_text = tb.Label(self.tsp, text='Please select a Start Place',
                                         style='Address.TLabel', anchor='center')
        self.setup_start_text.grid(row=1, column=1, sticky='nsew', padx=5)

        # get tour button
        self.tour_btn = tb.Button(self.tsp, text='Generate Route', width=20, style='Preference.TButton')
        self.tour_btn.grid(row=1, column=2, sticky='e', padx=10)
        self.tour_btn.config(command=self.run_tsp)

        # Set column weights for alignment
        self.tsp.columnconfigure(0, weight=1)
        self.tsp.columnconfigure(1, weight=1)
        self.tsp.columnconfigure(2, weight=1)

    def search_place(self, event):
        query = self.entry.get().strip()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a keyword.")
            return

        try:
            response = gmaps.places(query=query, location=(49.2827, -123.1207), radius=10000)
            self.search_results = response.get("results", [])[:3]

            labels = [self.chose1, self.chose2, self.chose3]
            for i, label in enumerate(labels):
                if i < len(self.search_results):
                    place = self.search_results[i]
                    name = place.get("name", "")
                    rating = place.get("rating", "N/A")
                    label.config(text=f"{name}\nGoogle Map Rating: {rating}")
                    label.bind('<Double-Button-1>', self.add_selected_place_from_search)
                else:
                    label.config(text="")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to search: {e}")

    def add_selected_place_from_recommendation(self, event):
        if not self.tree.selection():
            return

        item = self.tree.item(self.tree.selection())
        name, rating, reviews = item['values']

        for child in self.tree1.get_children():
            if self.tree1.item(child)['values'][0] == name:
                messagebox.showinfo("Info", "This place is already selected.")
                return

        tag = 'oddrow' if len(self.tree1.get_children()) % 2 == 0 else 'evenrow'
        self.tree1.insert('', 'end', values=(name, rating, reviews), tags=(tag,))
        self.selected_places_list.append({"name": name, "rating": rating, "reviews": reviews})
        print(self.selected_places_list)

    def add_selected_place_from_search(self, event):
        widget = event.widget
        idx = {self.chose1: 0, self.chose2: 1, self.chose3: 2}.get(widget, None)
        if idx is None or idx >= len(self.search_results):
            return

        item = self.search_results[idx]
        name = item.get("name", "")
        rating = item.get("rating", "N/A")
        reviews = f"{int(item.get('user_ratings_total', 0)):,}"

        for child in self.tree1.get_children():
            if self.tree1.item(child)['values'][0] == name:
                messagebox.showinfo("Info", "This place is already selected.")
                return

        tag = 'oddrow' if len(self.tree1.get_children()) % 2 == 0 else 'evenrow'
        self.tree1.insert('', 'end', values=(name, rating, reviews), tags=(tag,))
        self.selected_places_list.append({"name": name, "rating": rating, "reviews": reviews})
        print(self.selected_places_list)

    def remove_selected_place(self, event):
        selected_item = self.tree1.selection()
        if not selected_item:
            return

        item_id = selected_item[0]
        values = self.tree1.item(item_id)['values']
        name = values[0]  # Get the name of the place to be deleted

        confirm = messagebox.askyesno("Remove", f"Are you sure you want to remove '{name}'?")
        if confirm:
            self.tree1.delete(item_id)

            # Synchronously delete the corresponding place in self.selected_places_list
            self.selected_places_list = [
                place for place in self.selected_places_list if place.get("name") != name
            ]
        print(self.selected_places_list)

    def filter_places_by_category(self, category):
        if category in self.cached:
            sorted_results = self.cached[category]
        else:
            type_mapping = {
                'art_gallery': ['art'],
                'museum': ['art', 'culture'],
                'tourist_attraction': ['culture'],
                'park': ['nature'],
                'amusement_park': ['entertainment'],
                'restaurant': ['food'],
                'food': ['food'],
                'church': ['culture'],
                'university': ['culture'],
                'stadium': ['entertainment'],
                'zoo': ['nature', 'entertainment'],
                'aquarium': ['nature', 'entertainment'],
                'night_club': ['entertainment'],
                'casino': ['entertainment']
            }

            keywords = [k for k, v in type_mapping.items() if category.lower() in v]

            results_all = []
            for keyword in keywords:
                try:
                    response = gmaps.places(query=keyword, location=(49.2827, -123.1207), radius=10000)
                    results = response.get("results", [])
                    for place in results:
                        user_ratings = place.get("user_ratings_total", 0)
                        if user_ratings > 1000:
                            results_all.append(place)
                except Exception as e:
                    print(f"Error fetching {keyword}: {e}")

            # Deduplication (by name)
            unique = {}
            for r in results_all:
                name = r.get("name", "")
                if name not in unique:
                    unique[name] = r
                else:
                    # Keep the version with the most comments
                    if r.get("user_ratings_total", 0) > unique[name].get("user_ratings_total", 0):
                        unique[name] = r

            sorted_results = sorted(unique.values(), key=lambda x: x.get("rating", 0), reverse=True)[:20]
            self.cached[category] = sorted_results

        # Update TreeView
        for row in self.tree.get_children():
            self.tree.delete(row)

        for idx, place in enumerate(sorted_results):
            name = place.get('name', 'Unknown')
            rating = place.get('rating', 'N/A')
            reviews = f"{place.get('user_ratings_total', 0):,}"
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=(name, rating, reviews), tags=(tag,))

    def run_tsp(self):
        if not self.start_point:
            messagebox.showwarning("No Selection", "Please select a Start Place.")
            return
        if len(self.selected_places_list) == 0:
            messagebox.showwarning("No Selection", "Select at least one Attraction.")
            return

        tsp_places = self.selected_places_list.copy()
        tsp_places.append({'name': self.start_point})
        duration_matrix = get_distance_matrix(tsp_places)
        tour = tsp(duration_matrix, self.start_point)
        url = get_route_url(tour)
        webbrowser.open(url)
        # webview.create_window("Map Viewer", url, width=1500, height=1000)
        # webview.start()

    def set_start_point(self, selected_name):
        self.start_point = selected_name

    def set_start_text(self, selected_name):
        self.setup_start_text.config(text=f"Start Point: {selected_name}")

    def click_start_place(self):
        StartPlaceSelector(self.root, gmaps, self.set_start_point, self.set_start_text)
