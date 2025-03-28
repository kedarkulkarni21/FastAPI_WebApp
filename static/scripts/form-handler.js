// static/scripts/form-handler.js

// Simple client-side form handling
document.querySelector('#contactForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');
    
    // Hide any previous messages
    errorMessage.style.display = 'none';
    successMessage.style.display = 'none';
    
    try {
        const response = await fetch('/submit-form', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            // Show success message
            successMessage.style.display = 'block';
            // Reset the form
            this.reset();
        } else {
            // Show error message
            errorMessage.style.display = 'block';
        }
    } catch (error) {
        console.error('Error:', error);
        errorMessage.style.display = 'block';
    }
});