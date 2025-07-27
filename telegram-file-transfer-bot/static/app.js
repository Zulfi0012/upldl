// File Transfer Bot - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Initialize dashboard features if on dashboard page
    if (document.getElementById('activityChart')) {
        initializeDashboard();
    }
});

// Copy to clipboard function
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showToast('Copied to clipboard!', 'success');
    }).catch(function(err) {
        console.error('Failed to copy text: ', err);
        showToast('Failed to copy to clipboard', 'error');
    });
}

// Show toast notification
function showToast(message, type = 'info') {
    // Create toast element
    const toastHtml = `
        <div class="toast align-items-center text-white bg-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'primary'} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'exclamation-triangle' : 'info-circle'}"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;

    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }

    // Add toast to container
    const toastElement = document.createElement('div');
    toastElement.innerHTML = toastHtml;
    toastContainer.appendChild(toastElement.firstElementChild);

    // Initialize and show toast
    const toast = new bootstrap.Toast(toastContainer.lastElementChild);
    toast.show();

    // Remove toast element after it's hidden
    toastContainer.lastElementChild.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

// Refresh stats function for dashboard
function refreshStats() {
    const refreshBtn = document.querySelector('button[onclick="refreshStats()"]');
    if (refreshBtn) {
        // Show loading state
        const originalContent = refreshBtn.innerHTML;
        refreshBtn.innerHTML = '<i class="fas fa-sync-alt fa-spin"></i> Refreshing...';
        refreshBtn.disabled = true;

        // Reload page after a short delay to show the loading state
        setTimeout(() => {
            location.reload();
        }, 500);
    }
}

// Dashboard initialization
function initializeDashboard() {
    // Update uptime
    updateUptime();
    setInterval(updateUptime, 60000); // Update every minute

    // Initialize real-time updates (if WebSocket is available)
    if (typeof WebSocket !== 'undefined') {
        initializeWebSocket();
    }
}

// Update uptime display
function updateUptime() {
    const uptimeElement = document.getElementById('uptime');
    if (uptimeElement) {
        const now = new Date();
        const uptimeText = 'Active since ' + now.toLocaleTimeString();
        uptimeElement.textContent = uptimeText;
    }
}

// Initialize WebSocket for real-time updates (if implemented)
function initializeWebSocket() {
    // This would connect to a WebSocket endpoint for real-time stats
    // For now, we'll just poll for updates periodically
    setInterval(() => {
        // Could implement AJAX polling here for real-time stats
        // fetch('/api/stats').then(response => response.json()).then(updateStats);
    }, 30000); // Poll every 30 seconds
}

// Form validation helpers
function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        }
    });

    return isValid;
}

// URL validation
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

// File size formatter
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Time formatter
function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString();
}

// Animate counters on dashboard
function animateCounter(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = Math.floor(progress * (end - start) + start);
        element.textContent = value;
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Initialize counters animation on page load
document.addEventListener('DOMContentLoaded', function() {
    const counters = document.querySelectorAll('.card-body h3');
    counters.forEach(counter => {
        const target = parseInt(counter.textContent);
        if (!isNaN(target)) {
            counter.textContent = '0';
            animateCounter(counter, 0, target, 1000);
        }
    });
});

// Handle connection status
function updateConnectionStatus(isOnline) {
    const statusElements = document.querySelectorAll('.status-item');
    if (statusElements.length > 0) {
        statusElements[0].querySelector('.badge').className = 
            `badge ${isOnline ? 'bg-success' : 'bg-danger'}`;
        statusElements[0].querySelector('.badge i').className = 
            `fas ${isOnline ? 'fa-check' : 'fa-times'}`;
        statusElements[0].querySelector('.badge').textContent = 
            isOnline ? ' Online' : ' Offline';
    }
}

// Monitor online/offline status
window.addEventListener('online', () => updateConnectionStatus(true));
window.addEventListener('offline', () => updateConnectionStatus(false));

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl+R or F5 for refresh (on dashboard)
    if ((e.ctrlKey && e.key === 'r') || e.key === 'F5') {
        if (document.getElementById('activityChart')) {
            e.preventDefault();
            refreshStats();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) bsModal.hide();
        });
    }
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Progressive enhancement for JavaScript-dependent features
if ('serviceWorker' in navigator) {
    // Could register a service worker for offline functionality
    console.log('Service Worker support detected');
}

// Error handling for unhandled promise rejections
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    showToast('An unexpected error occurred', 'error');
});

// Global error handler
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    // Don't show toast for every error, just log it
});
