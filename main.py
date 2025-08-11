# main.py
from SearchUI import *
import googlemaps
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google API key Setup
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
if not API_KEY:
    raise ValueError("GOOGLE_MAPS_API_KEY not found in environment variables. Please check your .env file.")

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
