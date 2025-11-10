// Main JavaScript for Pysra App

// File upload preview
document.addEventListener('DOMContentLoaded', function() {
    // Update file upload labels
    const fileInputs = document.querySelectorAll('input[type="file"]');

    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name || 'Choose file';
            const label = document.querySelector(`label[for="${e.target.id}"]`);
            if (label) {
                const fileNameDiv = label.querySelector('.file-upload-icon + div') || label;
                fileNameDiv.textContent = fileName;
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});

// Smooth scroll for navigation
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
