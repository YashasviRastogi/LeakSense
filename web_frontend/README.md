# LeakSense Web Frontend

## Overview
Mobile-friendly, multi-page web application for real-time sensor monitoring, issue reporting, and community engagement.

## Pages

### 1. Dashboard (Main Page)
Real-time sensor monitoring interface with:
- 🎨 Modern dark theme with gradient animations
- 📊 Real-time gauge charts for each sensor
- 📈 Interactive line charts with multiple axes
- ⚡ Live data updates every 5 seconds
- 🚨 Alert notifications for threshold breaches
- 📱 Fully responsive design
- ✨ Smooth animations and transitions

### 2. Report Issue Page
Community reporting system featuring:
- 📝 Comprehensive issue reporting form
- 🏷️ Multiple issue types (leak, pressure, moisture, acoustic, sensor, other)
- 📍 Location tracking
- ⚠️ Severity levels (low, medium, high, critical)
- 📋 Recent reports feed
- ✅ Success confirmation modal

### 3. Community Leaderboard Page
Gamified engagement system with:
- 🏆 Top contributors ranking
- 📊 Community statistics
- 🎖️ Achievement badges system
- 💰 Monthly prize information
- ⚡ Points-based rewards
- 👥 User profiles and badges

## Technologies
- **HTML5** - Semantic markup with mobile meta tags
- **CSS3** - Modern styling with animations and responsive breakpoints
- **JavaScript (ES6+)** - Dynamic functionality with localStorage
- **Chart.js** - Data visualization

## Mobile Features
- 📱 **Touch-Optimized**: All interactions work smoothly on mobile devices
- 🍔 **Hamburger Menu**: Collapsible navigation for small screens
- 📐 **Responsive Grid**: Adapts to all screen sizes (320px - 4K)
- 👆 **Large Touch Targets**: Buttons and links sized for easy tapping
- 🔄 **Swipe Gestures**: Natural mobile navigation
- ⚡ **Fast Loading**: Optimized for mobile networks
- 💾 **Offline Storage**: Uses localStorage for reports and leaderboard

## File Structure
```
web_frontend/
├── index.html          # Single-page application with 3 pages
├── css/
│   └── style.css      # Styles, animations, and mobile responsive
└── js/
    ├── app.js         # App logic, navigation, reports, leaderboard
    └── charts.js      # Chart configurations
```

## Navigation System

### Desktop Navigation
- **Side Navigation Menu**: Fixed left sidebar with page links
- **Always Visible**: Navigation stays visible on large screens
- **Active Indicators**: Highlights current page

### Mobile Navigation
- **Hamburger Menu**: Tap to open/close navigation
- **Overlay Menu**: Slides in from left
- **Touch-Friendly**: Large tap targets for easy navigation
- **Auto-Close**: Menu closes after page selection

### Page Management
Pages are managed via JavaScript without page reloads:
```javascript
showPage('dashboard')  // Show dashboard
showPage('report')     // Show report issue page
showPage('community')  // Show community leaderboard
```

## Features Breakdown

### Dashboard Page Features
**Real-Time Gauges:**
- Pressure gauge (0-100 PSI)
- Moisture gauge (0-100%)
- Acoustic gauge (30-100 dB)
- Color-coded thresholds
- Smooth value transitions

**Interactive Charts:**
- Multi-axis line chart
- Time range selection (1h, 6h, 24h)
- Hover tooltips
- Responsive scaling

**Alert System:**
- Automatic threshold monitoring
- Visual alert banner
- Alert count indicator
- Dismissible notifications

**Statistics Display:**
- Min/Max/Average values
- Total readings count
- Last update timestamp
- Signal strength indicator

### Report Issue Page Features
**Report Form:**
- 6 issue types with icons
- Location input field
- 4 severity levels
- Rich text description
- Reporter information
- Form validation

**Recent Reports Feed:**
- Last 10 reports displayed
- Time ago formatting
- Severity badges
- Reporter attribution
- Hover effects

**Success Feedback:**
- Animated success modal
- Confirmation message
- Auto-clear form

### Community Leaderboard Features
**Rankings Table:**
- Top contributors list
- Rank badges (gold/silver/bronze)
- Points display
- Report count
- User badges

**Statistics Cards:**
- Total reports counter
- Fastest response time
- Issues resolved count
- Animated hover effects

**Achievements System:**
- 6 unique achievements
- Point values displayed
- Icon-based badges
- Hover animations

**Prize Information:**
- Monthly prize tiers
- Gift card amounts
- Badge rewards
- Visual prize cards

## Configuration

### API Endpoint
Edit in `js/app.js`:
```javascript
const API_BASE_URL = 'http://your-server:5000';
```

### Update Intervals
```javascript
const UPDATE_INTERVAL = 5000;        // 5 seconds
const CHART_UPDATE_INTERVAL = 10000; // 10 seconds
```

### Alert Thresholds
```javascript
const THRESHOLDS = {
    moisture: { warning: 60, danger: 70 },
    acoustic: { warning: 70, danger: 75 },
    pressure: { min: 20, max: 80 }
};
```

## Customization

### Colors
Edit CSS variables in `css/style.css`:
```css
:root {
    --primary-color: #3b82f6;
    --secondary-color: #8b5cf6;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
}
```

### Animations
Modify animation durations:
```css
@keyframes fadeInUp {
    /* Custom animation */
}
```

## Usage Examples

### Submitting a Report
```javascript
// User fills form and clicks submit
// Data is stored in localStorage
{
  issueType: 'leak',
  location: 'Building A, Floor 2',
  severity: 'high',
  description: 'Water leak detected in ceiling',
  reporterName: 'John Doe',
  timestamp: '2024-01-15T10:30:00Z'
}

// Points are automatically calculated:
// - High severity = 50 points
// - Added to user's leaderboard score
```

### Viewing Leaderboard
```javascript
// Leaderboard automatically updates
// Shows top contributors with:
// - Rank (1st, 2nd, 3rd, etc.)
// - Name
// - Total reports
// - Points earned
// - Badges (gold/silver/bronze)
```

## Responsive Breakpoints

### Desktop (1024px+)
- Side navigation always visible
- 3-column sensor grid
- Full-width charts
- 3-column info grid

### Tablet (768px - 1024px)
- Hamburger menu
- 2-column sensor grid
- Responsive charts
- 2-column info grid

### Mobile (< 768px)
- Hamburger menu
- Single-column layout
- Touch-optimized controls
- Stacked elements
- Full-width buttons

### Small Mobile (< 480px)
- Compact spacing
- Smaller fonts
- Optimized table display
- Single-column everything

## Browser Support
- Chrome 90+ ✅
- Firefox 88+ ✅
- Safari 14+ ✅
- Edge 90+ ✅
- Mobile Safari ✅
- Chrome Mobile ✅

## Performance
- Optimized chart rendering
- Efficient data updates
- Minimal DOM manipulation
- Lazy loading for large datasets

## Accessibility
- Semantic HTML
- ARIA labels
- Keyboard navigation
- Screen reader friendly

## Development

### Local Testing
Simply open `index.html` in a browser, or use a local server:

```bash
# Python
python -m http.server 8000

# Node.js
npx http-server

# PHP
php -S localhost:8000
```

### Production Build
For production, serve through Flask backend or any web server.

## Troubleshooting

### Data Not Loading
- Check API endpoint URL
- Verify CORS settings
- Check browser console for errors

### Charts Not Rendering
- Ensure Chart.js CDN is accessible
- Check canvas element IDs
- Verify data format

### Animations Not Working
- Check CSS animation support
- Verify browser compatibility
- Disable hardware acceleration if needed
