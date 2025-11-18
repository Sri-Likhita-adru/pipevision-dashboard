# PipeVision - Wastewater Infrastructure Monitoring Dashboard

A comprehensive web-based dashboard for monitoring wastewater pipe infrastructure using AI-powered analysis, real-time sensor data, and interactive visualizations.

## Features

- **System Overview Dashboard**: Key metrics, quality distribution charts, age analysis, and recent activity feed
- **Interactive Map View**: Leaflet-based map showing pipe segments color-coded by quality with detailed popups
- **Raw Data View**: Sensor readings table with search, filtering, and CSV export functionality
- **AI Analysis**: Corrosion detection results and maintenance recommendations with confidence scores
- **Alerts System**: Critical alerts sorted by severity with detailed tracking

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Charts**: Chart.js
- **Maps**: Leaflet with OpenStreetMap tiles
- **Icons**: Font Awesome 6

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
.
├── app.py                      # Flask application with API routes
├── requirements.txt            # Python dependencies
├── templates/
│   ├── base.html              # Base template with navigation
│   ├── dashboard.html         # System overview page
│   ├── map.html               # Interactive map view
│   ├── raw-data.html          # Sensor readings table
│   ├── ai-analysis.html       # AI insights and recommendations
│   └── alerts.html            # Active alerts page
└── README.md                  # This file
```

## API Endpoints

- `GET /api/pipe-segments` - Returns all pipe segment data
- `GET /api/sensor-readings` - Returns sensor readings
- `GET /api/ai-analysis` - Returns AI analysis results
- `GET /api/alerts` - Returns active alerts
- `GET /api/metrics` - Returns system-wide metrics
- `GET /api/recent-activity` - Returns recent activity feed

## Design System

The dashboard follows a Material Design inspired aesthetic with:

- **Typography**: Inter for UI, JetBrains Mono for data/metrics
- **Color Scheme**: Light mode with neutral grays, blue primary, destructive red
- **Layout**: Fixed sidebar navigation with responsive main content area
- **Components**: Cards, tables, badges, buttons with consistent spacing and styling

## Features by Page

### Dashboard (/)
- Total pipe length, average age, quality metrics
- Pie chart for quality distribution
- Bar charts for age distribution and pipe types
- Recent activity feed

### Map View (/map)
- Interactive Leaflet map centered on Ann Arbor, MI
- Color-coded pipe segments by quality
- Alert markers for poor quality pipes
- Detailed popups with pipe specifications

### Raw Data (/raw-data)
- Table of sensor readings (temperature, sound, flow rate)
- Search by pipe segment
- Filter by sensor type
- Export to CSV functionality

### AI Analysis (/ai-analysis)
- Critical findings and high-risk segment counts
- Accordion-style corrosion detection results
- Prioritized maintenance recommendations
- Confidence scores and predicted failure timelines

### Alerts (/alerts)
- Critical, high priority, and total active alert counts
- Sortable table by severity
- Detailed alert messages and timestamps
- View details action buttons

## Customization

### Mock Data
The application uses mock data generated in `app.py`. You can modify the data generators to:
- Adjust the number of pipe segments
- Change quality distributions
- Modify sensor reading ranges
- Customize alert messages

### Styling
All styles are embedded in the templates. Key variables are defined in `:root` CSS for easy customization:
- Colors: `--primary`, `--destructive`, `--chart-1` through `--chart-5`
- Typography: `--font-sans`, `--font-mono`
- Spacing: Uses consistent 4px/8px/12px/16px/24px spacing units

### Map
The map is centered on Ann Arbor, MI by default. Change coordinates in `map.html`:
```javascript
map.setView([42.2808, -83.7430], 13);
```

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## License

MIT License - feel free to use this dashboard for your infrastructure monitoring needs.

## Credits

Designed and developed based on enterprise dashboard patterns from Linear, Salesforce, and modern analytics platforms.