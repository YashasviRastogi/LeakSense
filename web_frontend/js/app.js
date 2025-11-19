// LeakSense Dashboard JavaScript

// Configuration
const API_BASE_URL = window.location.origin;
const UPDATE_INTERVAL = 5000; // 5 seconds
const CHART_UPDATE_INTERVAL = 10000; // 10 seconds

// Thresholds
const THRESHOLDS = {
    moisture: { warning: 60, danger: 70 },
    acoustic: { warning: 70, danger: 75 },
    pressure: { min: 20, max: 80 }
};

// Global state
let updateTimer = null;
let chartUpdateTimer = null;
let currentTimeRange = 24;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 LeakSense Dashboard Initializing...');
    initializeGauges();
    initializeChart();
    startDataUpdates();
    checkHealth();
});

// Check API health
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            updateStatus('connected', 'Connected');
        } else {
            updateStatus('disconnected', 'Disconnected');
        }
    } catch (error) {
        console.error('Health check failed:', error);
        updateStatus('disconnected', 'Connection Error');
    }
}

// Update connection status
function updateStatus(status, text) {
    const statusDot = document.getElementById('statusDot');
    const statusText = document.getElementById('statusText');
    
    statusDot.className = 'status-dot';
    if (status === 'disconnected') {
        statusDot.classList.add('disconnected');
    }
    statusText.textContent = text;
}

// Start periodic data updates
function startDataUpdates() {
    fetchLatestData();
    fetchStatistics();
    fetchChartData();
    
    updateTimer = setInterval(fetchLatestData, UPDATE_INTERVAL);
    chartUpdateTimer = setInterval(fetchChartData, CHART_UPDATE_INTERVAL);
}

// Fetch latest sensor reading
async function fetchLatestData() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/sensors/latest`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        
        const data = await response.json();
        updateSensorValues(data);
        updateLastUpdate(data.timestamp);
        checkAlerts(data);
        
    } catch (error) {
        console.error('Error fetching latest data:', error);
        updateStatus('disconnected', 'Connection Error');
    }
}

// Update sensor values on dashboard
function updateSensorValues(data) {
    // Update pressure
    const pressureValue = parseFloat(data.pressure).toFixed(1);
    document.getElementById('pressureValue').textContent = pressureValue;
    updateGauge('pressureGauge', pressureValue, 0, 100);
    
    // Update moisture
    const moistureValue = parseFloat(data.moisture).toFixed(1);
    document.getElementById('moistureValue').textContent = moistureValue;
    updateGauge('moistureGauge', moistureValue, 0, 100);
    
    // Update acoustic
    const acousticValue = parseFloat(data.acoustic).toFixed(1);
    document.getElementById('acousticValue').textContent = acousticValue;
    updateGauge('acousticGauge', acousticValue, 30, 100);
    
    // Update signal strength
    if (data.rssi) {
        const rssi = parseInt(data.rssi);
        let signalQuality = 'Excellent';
        if (rssi < -100) signalQuality = 'Poor';
        else if (rssi < -90) signalQuality = 'Fair';
        else if (rssi < -80) signalQuality = 'Good';
        
        document.getElementById('signalStrength').textContent = `${rssi} dBm (${signalQuality})`;
    }
    
    updateStatus('connected', 'Connected');
}

// Fetch and update statistics
async function fetchStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/sensors/statistics?hours=24`);
        const stats = await response.json();
        
        if (stats.total_readings) {
            // Update pressure stats
            document.getElementById('pressureMin').textContent = stats.min_pressure?.toFixed(1) || '--';
            document.getElementById('pressureAvg').textContent = stats.avg_pressure?.toFixed(1) || '--';
            document.getElementById('pressureMax').textContent = stats.max_pressure?.toFixed(1) || '--';
            
            // Update moisture stats
            document.getElementById('moistureMin').textContent = stats.min_moisture?.toFixed(1) || '--';
            document.getElementById('moistureAvg').textContent = stats.avg_moisture?.toFixed(1) || '--';
            document.getElementById('moistureMax').textContent = stats.max_moisture?.toFixed(1) || '--';
            
            // Update acoustic stats
            document.getElementById('acousticMin').textContent = stats.min_acoustic?.toFixed(1) || '--';
            document.getElementById('acousticAvg').textContent = stats.avg_acoustic?.toFixed(1) || '--';
            document.getElementById('acousticMax').textContent = stats.max_acoustic?.toFixed(1) || '--';
            
            // Update total readings
            document.getElementById('totalReadings').textContent = stats.total_readings.toLocaleString();
        }
    } catch (error) {
        console.error('Error fetching statistics:', error);
    }
}

// Check for alerts
function checkAlerts(data) {
    const alerts = [];
    
    if (data.moisture > THRESHOLDS.moisture.danger) {
        alerts.push('⚠️ Critical moisture level detected!');
    } else if (data.moisture > THRESHOLDS.moisture.warning) {
        alerts.push('⚠️ High moisture level detected!');
    }
    
    if (data.acoustic > THRESHOLDS.acoustic.danger) {
        alerts.push('⚠️ Critical acoustic level detected!');
    } else if (data.acoustic > THRESHOLDS.acoustic.warning) {
        alerts.push('⚠️ High acoustic level detected!');
    }
    
    if (data.pressure < THRESHOLDS.pressure.min) {
        alerts.push('⚠️ Low pressure detected!');
    } else if (data.pressure > THRESHOLDS.pressure.max) {
        alerts.push('⚠️ High pressure detected!');
    }
    
    // Update active alerts count
    document.getElementById('activeAlerts').textContent = alerts.length;
    
    // Show alert banner if there are alerts
    if (alerts.length > 0) {
        showAlert(alerts.join(' '));
    }
}

// Show alert banner
function showAlert(message) {
    const alertBanner = document.getElementById('alertBanner');
    const alertText = document.getElementById('alertText');
    
    alertText.textContent = message;
    alertBanner.style.display = 'flex';
}

// Close alert banner
function closeAlert() {
    const alertBanner = document.getElementById('alertBanner');
    alertBanner.style.display = 'none';
}

// Update last update time
function updateLastUpdate(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000); // seconds
    
    let timeAgo;
    if (diff < 60) {
        timeAgo = `${diff}s ago`;
    } else if (diff < 3600) {
        timeAgo = `${Math.floor(diff / 60)}m ago`;
    } else {
        timeAgo = `${Math.floor(diff / 3600)}h ago`;
    }
    
    document.getElementById('lastUpdate').textContent = timeAgo;
}

// Update time range for chart
function updateTimeRange() {
    const select = document.getElementById('timeRange');
    currentTimeRange = parseInt(select.value);
    fetchChartData();
}

// Fetch chart data
async function fetchChartData() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/sensors/chart-data?hours=${currentTimeRange}`);
        const data = await response.json();
        
        updateMainChart(data);
    } catch (error) {
        console.error('Error fetching chart data:', error);
    }
}

// Format number with animation
function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = current.toFixed(1);
    }, 16);
}

// Add smooth transitions to value updates
function updateValueWithAnimation(elementId, newValue) {
    const element = document.getElementById(elementId);
    const oldValue = parseFloat(element.textContent) || 0;
    animateValue(element, oldValue, newValue, 500);
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (updateTimer) clearInterval(updateTimer);
    if (chartUpdateTimer) clearInterval(chartUpdateTimer);
});

// Error handling for fetch requests
async function fetchWithRetry(url, retries = 3) {
    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(url);
            if (response.ok) return response;
        } catch (error) {
            if (i === retries - 1) throw error;
            await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
        }
    }
}

// Page Navigation
function showPage(pageName) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // Show selected page
    const pageId = pageName + 'Page';
    const page = document.getElementById(pageId);
    if (page) {
        page.classList.add('active');
    }
    
    // Update navigation links
    document.querySelectorAll('.nav-link, .desktop-nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.page === pageName) {
            link.classList.add('active');
        }
    });
    
    // Close mobile menu if open
    const navMenu = document.getElementById('navMenu');
    const backdrop = document.getElementById('mobileMenuBackdrop');
    if (navMenu.classList.contains('active')) {
        navMenu.classList.remove('active');
        backdrop.classList.remove('show');
        document.body.style.overflow = '';
    }
    
    // Load page-specific data
    if (pageName === 'report') {
        loadRecentReports();
    } else if (pageName === 'community') {
        updateLeaderboard();
    }
}

// Mobile Menu Toggle
function toggleMobileMenu() {
    const navMenu = document.getElementById('navMenu');
    const backdrop = document.getElementById('mobileMenuBackdrop');
    
    navMenu.classList.toggle('active');
    backdrop.classList.toggle('show');
    
    // Prevent body scroll when menu is open
    if (navMenu.classList.contains('active')) {
        document.body.style.overflow = 'hidden';
    } else {
        document.body.style.overflow = '';
    }
}

// Report Form Functions
function submitReport(event) {
    event.preventDefault();
    
    const formData = {
        issueType: document.getElementById('issueType').value,
        location: document.getElementById('location').value,
        severity: document.getElementById('severity').value,
        description: document.getElementById('description').value,
        reporterName: document.getElementById('reporterName').value,
        reporterContact: document.getElementById('reporterContact').value,
        timestamp: new Date().toISOString()
    };
    
    // Store in localStorage (in production, send to API)
    let reports = JSON.parse(localStorage.getItem('leaksense_reports') || '[]');
    reports.unshift(formData);
    localStorage.setItem('leaksense_reports', JSON.stringify(reports));
    
    // Update leaderboard
    updateLeaderboardData(formData.reporterName);
    
    // Show success modal
    showSuccessModal('Report submitted successfully! Thank you for helping keep our system safe.');
    
    // Reset form
    resetReportForm();
    
    // Reload recent reports
    loadRecentReports();
}

function resetReportForm() {
    document.getElementById('reportForm').reset();
}

function loadRecentReports() {
    const reports = JSON.parse(localStorage.getItem('leaksense_reports') || '[]');
    const reportsList = document.getElementById('recentReportsList');
    
    if (reports.length === 0) {
        reportsList.innerHTML = '<p style="text-align: center; color: var(--text-secondary); padding: 40px;">No reports yet. Be the first to report an issue!</p>';
        return;
    }
    
    reportsList.innerHTML = reports.slice(0, 10).map(report => {
        const date = new Date(report.timestamp);
        const timeAgo = getTimeAgo(date);
        
        return `
            <div class="report-item">
                <div class="report-header">
                    <div>
                        <div class="report-type">${getIssueTypeLabel(report.issueType)}</div>
                        <div style="font-size: 14px; color: var(--text-secondary); margin-top: 4px;">
                            📍 ${report.location}
                        </div>
                    </div>
                    <div class="report-time">${timeAgo}</div>
                </div>
                <p style="margin: 12px 0; color: var(--text-secondary);">${report.description}</p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="report-severity severity-${report.severity}">${report.severity.toUpperCase()}</span>
                    <span style="font-size: 13px; color: var(--text-secondary);">Reported by: ${report.reporterName}</span>
                </div>
            </div>
        `;
    }).join('');
}

function getIssueTypeLabel(type) {
    const labels = {
        'leak': '💧 Water Leak',
        'pressure': '⚡ Abnormal Pressure',
        'moisture': '💦 High Moisture',
        'acoustic': '🔊 Unusual Sound',
        'sensor': '🔧 Sensor Issue',
        'other': '❓ Other'
    };
    return labels[type] || type;
}

function getTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);
    
    if (seconds < 60) return `${seconds}s ago`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    return `${Math.floor(seconds / 86400)}d ago`;
}

// Leaderboard Functions
function updateLeaderboard() {
    const period = document.getElementById('leaderboardPeriod')?.value || 'month';
    const leaderboard = getLeaderboardData(period);
    
    // Update stats
    document.getElementById('totalReports').textContent = leaderboard.totalReports;
    document.getElementById('fastestResponse').textContent = leaderboard.fastestResponse;
    document.getElementById('issuesResolved').textContent = leaderboard.issuesResolved;
    
    // Update table
    const tbody = document.getElementById('leaderboardBody');
    if (leaderboard.users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 40px; color: var(--text-secondary);">No data yet. Start reporting to appear on the leaderboard!</td></tr>';
        return;
    }
    
    tbody.innerHTML = leaderboard.users.map((user, index) => {
        const rank = index + 1;
        const rankClass = rank <= 3 ? `rank-${rank}` : 'rank-other';
        const badge = rank === 1 ? 'gold' : rank === 2 ? 'silver' : rank === 3 ? 'bronze' : '';
        
        return `
            <tr>
                <td><span class="rank-badge ${rankClass}">${rank}</span></td>
                <td><strong>${user.name}</strong></td>
                <td>${user.reports}</td>
                <td><strong>${user.points}</strong></td>
                <td>${badge ? `<span class="user-badge badge-${badge}">${badge.toUpperCase()}</span>` : '-'}</td>
            </tr>
        `;
    }).join('');
}

function getLeaderboardData(period) {
    const reports = JSON.parse(localStorage.getItem('leaksense_reports') || '[]');
    const leaderboardData = JSON.parse(localStorage.getItem('leaksense_leaderboard') || '{}');
    
    // Calculate stats
    const userStats = {};
    reports.forEach(report => {
        const name = report.reporterName;
        if (!userStats[name]) {
            userStats[name] = { name, reports: 0, points: 0 };
        }
        userStats[name].reports++;
        
        // Calculate points based on severity
        const severityPoints = {
            'low': 10,
            'medium': 25,
            'high': 50,
            'critical': 100
        };
        userStats[name].points += severityPoints[report.severity] || 10;
    });
    
    // Sort by points
    const users = Object.values(userStats).sort((a, b) => b.points - a.points);
    
    return {
        totalReports: reports.length,
        fastestResponse: reports.length > 0 ? '< 5 min' : '--',
        issuesResolved: Math.floor(reports.length * 0.8),
        users: users
    };
}

function updateLeaderboardData(reporterName) {
    const leaderboard = JSON.parse(localStorage.getItem('leaksense_leaderboard') || '{}');
    
    if (!leaderboard[reporterName]) {
        leaderboard[reporterName] = {
            name: reporterName,
            reports: 0,
            points: 0,
            badges: []
        };
    }
    
    leaderboard[reporterName].reports++;
    leaderboard[reporterName].points += 10;
    
    localStorage.setItem('leaksense_leaderboard', JSON.stringify(leaderboard));
}

// Modal Functions
function showSuccessModal(message) {
    const modal = document.getElementById('successModal');
    const modalMessage = document.getElementById('modalMessage');
    modalMessage.textContent = message;
    modal.classList.add('show');
}

function closeModal() {
    const modal = document.getElementById('successModal');
    modal.classList.remove('show');
}

// Close modal on outside click
window.onclick = function(event) {
    const modal = document.getElementById('successModal');
    if (event.target === modal) {
        closeModal();
    }
};

// Export functions for global access
window.closeAlert = closeAlert;
window.updateTimeRange = updateTimeRange;
window.showPage = showPage;
window.toggleMobileMenu = toggleMobileMenu;
window.submitReport = submitReport;
window.resetReportForm = resetReportForm;
window.updateLeaderboard = updateLeaderboard;
window.closeModal = closeModal;

console.log('✅ LeakSense Dashboard Initialized');
