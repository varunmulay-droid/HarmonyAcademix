// Project Harmony Hands - Main JavaScript File

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Main application initialization
function initializeApp() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize STU ID validation
    initializeSTUIDValidation();
    
    // Initialize file upload handlers
    initializeFileUploads();
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize print functionality
    initializePrint();
    
    // Initialize auto-save for forms
    initializeAutoSave();
    
    console.log('Project Harmony Hands ERP initialized successfully');
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Form validation enhancement
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Show first invalid field
                const firstInvalidField = form.querySelector(':invalid');
                if (firstInvalidField) {
                    firstInvalidField.focus();
                    firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

// STU ID validation and availability checking
function initializeSTUIDValidation() {
    const stuIdInputs = document.querySelectorAll('input[data-stu-id-check]');
    
    stuIdInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const stuId = this.value.trim();
            if (stuId && stuId.match(/^STU\d{3}$/)) {
                checkSTUIDAvailability(stuId, this);
            }
        });
    });
}

// Check if STU ID is available
async function checkSTUIDAvailability(stuId, inputElement) {
    try {
        const response = await fetch(`/api/check_stu_id/${stuId}`);
        const data = await response.json();
        
        const feedbackElement = inputElement.parentNode.querySelector('.stu-id-feedback') ||
                               createFeedbackElement(inputElement);
        
        if (data.available) {
            inputElement.classList.remove('is-invalid');
            inputElement.classList.add('is-valid');
            feedbackElement.textContent = 'STU ID उपलब्ध आहे';
            feedbackElement.className = 'stu-id-feedback valid-feedback';
        } else {
            inputElement.classList.remove('is-valid');
            inputElement.classList.add('is-invalid');
            feedbackElement.textContent = 'हा STU ID आधीच वापरात आहे';
            feedbackElement.className = 'stu-id-feedback invalid-feedback';
        }
        
        feedbackElement.style.display = 'block';
    } catch (error) {
        console.error('Error checking STU ID availability:', error);
    }
}

// Create feedback element for STU ID validation
function createFeedbackElement(inputElement) {
    const feedbackElement = document.createElement('div');
    feedbackElement.className = 'stu-id-feedback';
    inputElement.parentNode.appendChild(feedbackElement);
    return feedbackElement;
}

// File upload enhancements
function initializeFileUploads() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            validateFileUpload(this);
            showFilePreview(this);
        });
    });
}

// Validate file uploads
function validateFileUpload(input) {
    const file = input.files[0];
    if (!file) return;
    
    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'application/pdf'];
    
    let isValid = true;
    let errorMessage = '';
    
    if (file.size > maxSize) {
        isValid = false;
        errorMessage = 'फाइल साइज 16MB पेक्षा कमी असावी';
    }
    
    if (!allowedTypes.includes(file.type)) {
        isValid = false;
        errorMessage = 'फक्त JPG, PNG, GIF, PDF फाइल्स स्वीकारल्या जातात';
    }
    
    const feedbackElement = input.parentNode.querySelector('.file-feedback') ||
                           createFileFeedbackElement(input);
    
    if (isValid) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        feedbackElement.textContent = `फाइल निवडली: ${file.name}`;
        feedbackElement.className = 'file-feedback valid-feedback';
    } else {
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
        feedbackElement.textContent = errorMessage;
        feedbackElement.className = 'file-feedback invalid-feedback';
        input.value = '';
    }
    
    feedbackElement.style.display = 'block';
}

// Create file feedback element
function createFileFeedbackElement(inputElement) {
    const feedbackElement = document.createElement('div');
    feedbackElement.className = 'file-feedback';
    inputElement.parentNode.appendChild(feedbackElement);
    return feedbackElement;
}

// Show file preview for images
function showFilePreview(input) {
    const file = input.files[0];
    if (!file || !file.type.startsWith('image/')) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        let previewElement = input.parentNode.querySelector('.file-preview');
        
        if (!previewElement) {
            previewElement = document.createElement('div');
            previewElement.className = 'file-preview mt-2';
            input.parentNode.appendChild(previewElement);
        }
        
        previewElement.innerHTML = `
            <img src="${e.target.result}" alt="File Preview" 
                 class="img-thumbnail" style="max-width: 200px; max-height: 200px;">
            <button type="button" class="btn btn-sm btn-outline-danger ms-2" 
                    onclick="removeFilePreview(this)">
                <i class="fas fa-times"></i> काढा
            </button>
        `;
    };
    
    reader.readAsDataURL(file);
}

// Remove file preview
function removeFilePreview(button) {
    const previewElement = button.parentNode;
    const input = previewElement.parentNode.querySelector('input[type="file"]');
    
    input.value = '';
    input.classList.remove('is-valid', 'is-invalid');
    previewElement.remove();
    
    const feedbackElement = input.parentNode.querySelector('.file-feedback');
    if (feedbackElement) {
        feedbackElement.style.display = 'none';
    }
}

// Initialize search functionality
function initializeSearch() {
    const searchInputs = document.querySelectorAll('[data-search-target]');
    
    searchInputs.forEach(input => {
        input.addEventListener('input', debounce(function() {
            const targetSelector = this.dataset.searchTarget;
            const searchTerm = this.value.toLowerCase();
            performSearch(targetSelector, searchTerm);
        }, 300));
    });
}

// Perform search in table or list
function performSearch(targetSelector, searchTerm) {
    const targetElement = document.querySelector(targetSelector);
    if (!targetElement) return;
    
    const searchableElements = targetElement.querySelectorAll('[data-searchable]');
    
    searchableElements.forEach(element => {
        const searchableText = element.textContent.toLowerCase();
        const shouldShow = !searchTerm || searchableText.includes(searchTerm);
        
        element.style.display = shouldShow ? '' : 'none';
    });
    
    // Update search result count
    updateSearchResultCount(targetElement, searchTerm);
}

// Update search result count
function updateSearchResultCount(container, searchTerm) {
    const countElement = document.querySelector('[data-search-count]');
    if (!countElement) return;
    
    const visibleElements = container.querySelectorAll('[data-searchable]:not([style*="display: none"])');
    const totalElements = container.querySelectorAll('[data-searchable]');
    
    if (searchTerm) {
        countElement.textContent = `${visibleElements.length} of ${totalElements.length} results`;
    } else {
        countElement.textContent = `${totalElements.length} total`;
    }
}

// Initialize print functionality
function initializePrint() {
    const printButtons = document.querySelectorAll('[data-print]');
    
    printButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetSelector = this.dataset.print;
            printElement(targetSelector);
        });
    });
}

// Print specific element
function printElement(selector) {
    const element = document.querySelector(selector);
    if (!element) return;
    
    const printWindow = window.open('', '_blank');
    const printDocument = printWindow.document;
    
    printDocument.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Print - Project Harmony Hands</title>
            <meta charset="UTF-8">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                @media print {
                    .no-print { display: none !important; }
                    body { margin: 0; padding: 20px; }
                    .card { border: 1px solid #ddd; box-shadow: none; }
                }
                body { font-family: 'Noto Sans Devanagari', sans-serif; }
            </style>
        </head>
        <body>
            ${element.outerHTML}
            <script>
                window.onload = function() {
                    window.print();
                    window.onafterprint = function() {
                        window.close();
                    };
                };
            </script>
        </body>
        </html>
    `);
    
    printDocument.close();
}

// Initialize auto-save for forms
function initializeAutoSave() {
    const autoSaveForms = document.querySelectorAll('[data-auto-save]');
    
    autoSaveForms.forEach(form => {
        const formId = form.dataset.autoSave;
        
        // Load saved data
        loadAutoSavedData(form, formId);
        
        // Save data on input
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('input', debounce(function() {
                saveFormData(form, formId);
            }, 1000));
        });
    });
}

// Save form data to localStorage
function saveFormData(form, formId) {
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    localStorage.setItem(`harmony_hands_${formId}`, JSON.stringify(data));
    showAutoSaveIndicator();
}

// Load auto-saved data
function loadAutoSavedData(form, formId) {
    const savedData = localStorage.getItem(`harmony_hands_${formId}`);
    if (!savedData) return;
    
    try {
        const data = JSON.parse(savedData);
        
        Object.keys(data).forEach(key => {
            const input = form.querySelector(`[name="${key}"]`);
            if (input && input.type !== 'file') {
                input.value = data[key];
            }
        });
        
        showAutoSaveNotification('पूर्वी सेव्ह केलेला डेटा लोड केला गेला');
    } catch (error) {
        console.error('Error loading auto-saved data:', error);
    }
}

// Show auto-save indicator
function showAutoSaveIndicator() {
    let indicator = document.querySelector('.auto-save-indicator');
    
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.className = 'auto-save-indicator position-fixed';
        indicator.style.cssText = `
            top: 20px; right: 20px; z-index: 9999;
            background: #28a745; color: white; padding: 8px 16px;
            border-radius: 4px; font-size: 14px; opacity: 0;
            transition: opacity 0.3s;
        `;
        indicator.innerHTML = '<i class="fas fa-check me-1"></i>ऑटो सेव्ह';
        document.body.appendChild(indicator);
    }
    
    indicator.style.opacity = '1';
    setTimeout(() => {
        indicator.style.opacity = '0';
    }, 2000);
}

// Show auto-save notification
function showAutoSaveNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'alert alert-info alert-dismissible fade show position-fixed';
    notification.style.cssText = 'top: 20px; left: 20px; z-index: 9999; max-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Clear auto-saved data
function clearAutoSavedData(formId) {
    localStorage.removeItem(`harmony_hands_${formId}`);
}

// Utility function: Debounce
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        
        if (callNow) func.apply(context, args);
    };
}

// Utility function: Show loading spinner
function showLoadingSpinner(element, message = 'लोड करत आहे...') {
    element.innerHTML = `
        <div class="text-center py-4">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-2 text-muted">${message}</p>
        </div>
    `;
}

// Utility function: Format date for display
function formatDate(dateString, locale = 'mr-IN') {
    if (!dateString) return '-';
    
    const date = new Date(dateString);
    return date.toLocaleDateString(locale, {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Utility function: Format STU ID
function formatSTUID(stuId) {
    if (!stuId) return '-';
    return stuId.toUpperCase();
}

// Utility function: Validate Marathi input
function validateMarathiInput(input) {
    // Marathi Unicode range: 0900-097F
    const marathiRegex = /^[\u0900-\u097F\s]*$/;
    return marathiRegex.test(input);
}

// Utility function: Show toast notification
function showToast(message, type = 'info', duration = 3000) {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" 
                    data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast, { delay: duration });
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

// Create toast container if it doesn't exist
function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

// Handle network errors gracefully
function handleNetworkError(error) {
    console.error('Network error:', error);
    showToast('नेटवर्क त्रुटी - कृपया पुन्हा प्रयत्न करा', 'danger');
}

// Initialize service worker for offline functionality (if needed)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('ServiceWorker registered successfully');
            })
            .catch(error => {
                console.log('ServiceWorker registration failed');
            });
    });
}

// Export functions for global use
window.HarmonyHands = {
    showToast,
    formatDate,
    formatSTUID,
    validateMarathiInput,
    showLoadingSpinner,
    clearAutoSavedData,
    handleNetworkError,
    checkSTUIDAvailability,
    printElement
};
