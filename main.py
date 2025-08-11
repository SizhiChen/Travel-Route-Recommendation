# main.py
from SearchUI import *
import googlemaps
import pandas as pd

# Google API key Setup
API_KEY = ''
gmaps = googlemaps.Client(key=API_KEY)

# Get the Rating dataFrame
attractionData = pd.read_csv("vancouver_attractions_sorted.csv")

def main():

    # GUI using Tkinter
    root = tb.Window(themename="flatly")
    app = SearchUI(root, attractionData)
    root.mainloop()
    print(app)
    return

if __name__ == '__main__':
    main()
