# Travel Route Recommendation System

A Python-based desktop application that helps users plan optimal travel routes through Vancouver attractions using Google Maps API and TSP (Traveling Salesman Problem) algorithms.

## 🎯 Project Overview

This application provides an intelligent travel planning solution that:
- Recommends popular Vancouver attractions based on ratings and user reviews
- Allows users to search for custom locations as starting points
- Optimizes travel routes using TSP algorithms to minimize travel time
- Provides an intuitive GUI for easy interaction
- Generates Google Maps directions for the optimized route

## ✨ Features

### 🏙️ Attraction Database
- Pre-loaded database of 40 popular Vancouver attractions
- Sorted by Google ratings and user review counts
- Includes addresses and detailed information for each location

### 🔍 Smart Search
- Search for custom starting locations using Google Places API
- Real-time location suggestions with addresses
- Geocoding support for accurate location data

### 🛣️ Route Optimization
- Implements Traveling Salesman Problem (TSP) algorithms
- Calculates optimal travel routes to minimize total travel time
- Uses Google Maps Directions API for real-time traffic data
- Generates clickable Google Maps URLs for navigation

### 🎨 User-Friendly Interface
- Modern GUI built with ttkbootstrap
- Intuitive drag-and-drop style attraction selection
- Category-based filtering (Art, Nature, Entertainment, etc.)
- Real-time route visualization

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- Google Maps API key with the following APIs enabled:
  - Places API
  - Directions API
  - Geocoding API

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Travel-Route-Recommendation
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key**
   - Get a Google Maps API key from [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the required APIs (Places, Directions, Geocoding)
   - Create a `.env` file in the project root directory
   - Add your API key to the `.env` file:
     ```
     GOOGLE_MAPS_API_KEY=your_actual_api_key_here
     ```
   - **Important**: Never commit your `.env` file to version control

4. **Run the application**
   ```bash
   python main.py
   ```

## 🚀 Usage

### Getting Started
1. Launch the application using `python main.py`
2. Enter your starting address in the search box
3. Click "Search" to find your location
4. Select attractions from the recommendations or search for custom places
5. Choose your preferred categories using the filter buttons
6. Click "Generate Route" to optimize your travel path
7. Click "Open in Google Maps" to view the route in your browser

### Features Walkthrough

#### Search for Starting Location
- Type any address or landmark in Vancouver
- The app will suggest matching locations
- Select your preferred starting point

#### Select Attractions
- Browse through pre-loaded Vancouver attractions
- Use category filters to find specific types of places
- Add attractions to your itinerary
- Remove unwanted locations from your list

#### Route Optimization
- The app automatically calculates the optimal route
- Uses real-time travel time data from Google Maps
- Minimizes total travel time between attractions
- Provides a complete round-trip route

## 📁 Project Structure

```
Travel-Route-Recommendation/
├── main.py                      # Main application entry point
├── SearchUI.py                  # Main GUI interface
├── StartPlaceSelector.py        # Starting location selector
├── tsp_solver.py               # TSP algorithm implementation
├── attractions_rating.py       # Attraction data processing
├── vancouver_attractions_sorted.csv  # Attraction database
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API keys)
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🔧 Technical Details

### Core Components

#### SearchUI.py
- Main GUI class using ttkbootstrap
- Handles user interactions and data flow
- Manages attraction selection and filtering
- Integrates with Google Maps APIs

#### tsp_solver.py
- Implements nearest neighbor TSP algorithm
- Calculates distance matrices using Google Directions API
- Generates optimized travel routes
- Creates Google Maps navigation URLs

#### StartPlaceSelector.py
- Modal dialog for selecting starting locations
- Google Places API integration
- Address validation and geocoding

### Algorithms Used

#### Traveling Salesman Problem (TSP)
- **Algorithm**: Nearest Neighbor Heuristic
- **Optimization**: Minimizes total travel time
- **Input**: Distance matrix from Google Maps API
- **Output**: Optimized route sequence

#### Distance Calculation
- Uses Google Maps Directions API
- Real-time traffic consideration
- Travel time in minutes
- Symmetric distance matrix

## 📊 Data Sources

### Vancouver Attractions Database
- **Source**: Google Places API
- **Fields**: Name, Address, Rating, User Ratings Count
- **Sorting**: By rating (descending) then by user count (descending)
- **Total Attractions**: 40+ locations

### Real-time Data
- **Travel Times**: Google Maps Directions API
- **Location Data**: Google Places API
- **Geocoding**: Google Geocoding API

## 🎨 UI/UX Features

### Design Principles
- **Modern Interface**: Clean, professional appearance
- **Responsive Layout**: Adapts to different screen sizes
- **Intuitive Navigation**: Easy-to-understand controls
- **Visual Feedback**: Clear indication of selections and actions

### Color Scheme
- **Primary**: #0279B1 (Blue)
- **Background**: #F4FAFD (Light Blue)
- **Text**: Dark gray for readability
- **Accents**: White and light gray for contrast

## 🔒 Security & Privacy

### API Key Management
- API keys are stored securely in `.env` files
- `.env` files are excluded from version control via `.gitignore`
- Never commit API keys to version control
- Use environment variables for production deployment

### Data Privacy
- No personal data is stored locally
- All location data is processed through Google APIs
- No tracking or analytics collection

## 📞 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Contact the development team
- Check the troubleshooting section above

---

**Happy Traveling! 🗺️✈️** 