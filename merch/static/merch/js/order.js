/**
 * EYTGaming Merch Order Management
 * Handles dynamic size loading and order submission
 */

// API Endpoints
const API = {
    sizes: '/api/sizes/',
    order: '/api/order/'
};

// DOM Elements
const elements = {
    form: null,
    sizeSelect: null,
    submitBtn: null,
    btnText: null,
    messageContainer: null
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Cache DOM elements
    elements.form = document.getElementById('orderForm');
    elements.sizeSelect = document.getElementById('sizeSelect');
    elements.submitBtn = document.getElementById('submitBtn');
    elements.btnText = document.getElementById('btnText');
    elements.messageContainer = document.getElementById('messageContainer');
    
    // Load available sizes
    loadAvailableSizes();
    
    // Attach form submit handler
    elements.form.addEventListener('submit', handleFormSubmit);
});

/**
 * Load available sizes from API
 */
async function loadAvailableSizes() {
    try {
        const response = await fetch(API.sizes);
        
        if (!response.ok) {
            throw new Error('Failed to load sizes');
        }
        
        const sizes = await response.json();
        populateSizeSelect(sizes);
        
    } catch (error) {
        console.error('Error loading sizes:', error);
        showMessage('Failed to load available sizes. Please refresh the page.', 'error');
    }
}

/**
 * Populate size dropdown with available sizes
 */
function populateSizeSelect(sizes) {
    // Clear existing options except the placeholder
    elements.sizeSelect.innerHTML = '<option disabled selected value="">Choose your size...</option>';
    
    if (sizes.length === 0) {
        const option = document.createElement('option');
        option.disabled = true;
        option.textContent = 'No sizes available';
        elements.sizeSelect.appendChild(option);
        return;
    }
    
    // Size display names
    const sizeNames = {
        'S': 'Small',
        'M': 'Medium',
        'L': 'Large',
        'XL': 'Extra Large',
        '2XL': '2X Large'
    };
    
    // Add available sizes
    sizes.forEach(size => {
        const option = document.createElement('option');
        option.value = size.name;
        
        // Format display text
        const displayName = sizeNames[size.name] || size.name;
        let stockStatus = '';
        
        if (size.available_quantity <= 5) {
            stockStatus = ' — Low Stock';
        } else {
            stockStatus = ' — Available';
        }
        
        option.textContent = `${size.name} (${displayName})${stockStatus}`;
        elements.sizeSelect.appendChild(option);
    });
}

/**
 * Get CSRF token from cookie
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Disable submit button
    setButtonLoading(true);
    
    // Collect form data
    const formData = new FormData(elements.form);
    const orderData = {
        full_name: formData.get('full_name'),
        gamer_tag: formData.get('gamer_tag'),
        preferred_number: formData.get('preferred_number'),
        size: formData.get('size'),
        color: formData.get('color'),
        phone: formData.get('phone') || '',
        email: formData.get('email') || ''
    };
    
    // Validate
    if (!validateOrderData(orderData)) {
        setButtonLoading(false);
        return;
    }
    
    try {
        const response = await fetch(API.order, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(orderData)
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            handleOrderSuccess(result);
        } else {
            handleOrderError(result.error || 'Order submission failed');
        }
        
    } catch (error) {
        console.error('Order submission error:', error);
        handleOrderError('Network error. Please check your connection and try again.');
    } finally {
        setButtonLoading(false);
    }
}

/**
 * Validate order data before submission
 */
function validateOrderData(data) {
    // Check if name/tag fields exist (they may be hidden for authenticated users)
    const nameField = document.getElementById('fullName');
    const tagField = document.getElementById('gamerTag');
    const isAuthenticated = nameField && nameField.type === 'hidden';
    
    // Define required fields based on authentication status
    let requiredFields = ['preferred_number', 'size', 'color'];
    if (!isAuthenticated) {
        requiredFields.push('full_name', 'gamer_tag');
    }
    
    for (const field of requiredFields) {
        if (!data[field] || data[field].trim() === '') {
            showMessage(`Please fill in the ${field.replace('_', ' ')} field.`, 'error');
            return false;
        }
    }
    
    // Validate number range
    const number = parseInt(data.preferred_number);
    if (isNaN(number) || number < 0 || number > 99) {
        showMessage('Jersey number must be between 0 and 99.', 'error');
        return false;
    }
    
    return true;
}

/**
 * Handle successful order submission
 */
function handleOrderSuccess(result) {
    showMessage(
        `🎉 Order confirmed! Your DOJO gear has been registered. Order ID: #EYT-${result.order_id}. We'll contact you shortly for payment and shipping.`,
        'success'
    );
    
    // Reset form after 2 seconds
    setTimeout(() => {
        elements.form.reset();
        // Reload sizes to update stock
        loadAvailableSizes();
    }, 2000);
}

/**
 * Handle order submission error
 */
function handleOrderError(errorMessage) {
    showMessage(`❌ ${errorMessage}`, 'error');
}

/**
 * Set button loading state
 */
function setButtonLoading(isLoading) {
    elements.submitBtn.disabled = isLoading;
    
    if (isLoading) {
        elements.btnText.textContent = 'Processing...';
        elements.submitBtn.classList.add('opacity-70', 'cursor-not-allowed');
    } else {
        elements.btnText.textContent = 'Submit Order';
        elements.submitBtn.classList.remove('opacity-70', 'cursor-not-allowed');
    }
}

/**
 * Show message to user
 */
function showMessage(message, type = 'info') {
    elements.messageContainer.className = '';
    elements.messageContainer.classList.add('mt-4', 'p-4', 'rounded-lg', 'text-sm', 'font-medium');
    
    if (type === 'success') {
        elements.messageContainer.classList.add('bg-emerald-500/10', 'text-emerald-600', 'dark:text-emerald-400', 'border', 'border-emerald-500/20');
    } else if (type === 'error') {
        elements.messageContainer.classList.add('bg-red-500/10', 'text-red-600', 'dark:text-red-400', 'border', 'border-red-500/20');
    } else {
        elements.messageContainer.classList.add('bg-blue-500/10', 'text-blue-600', 'dark:text-blue-400', 'border', 'border-blue-500/20');
    }
    
    elements.messageContainer.textContent = message;
    elements.messageContainer.classList.remove('hidden');
    
    // Auto-hide after 10 seconds
    setTimeout(() => {
        elements.messageContainer.classList.add('hidden');
    }, 10000);
}
