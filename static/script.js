// ==================== CANVAS SETUP ====================
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const canvasOverlay = document.getElementById('canvasOverlay');
const clearBtn = document.getElementById('clearBtn');
const predictBtn = document.getElementById('predictBtn');
const resultsContent = document.getElementById('resultsContent');
const brushSizeInput = document.getElementById('brushSize');
const brushSizeValue = document.getElementById('brushSizeValue');

// Canvas state
let isDrawing = false;
let hasDrawn = false;
let brushSize = 15;

// Set canvas background
ctx.fillStyle = '#000000';
ctx.fillRect(0, 0, canvas.width, canvas.height);

// ==================== PARTICLES ANIMATION ====================
function createParticles() {
    const particlesContainer = document.getElementById('particles');
    const particleCount = 30;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 20 + 's';
        particle.style.animationDuration = (15 + Math.random() * 10) + 's';
        particlesContainer.appendChild(particle);
    }
}

// ==================== BRUSH SIZE CONTROL ====================
brushSizeInput.addEventListener('input', (e) => {
    brushSize = parseInt(e.target.value);
    brushSizeValue.textContent = brushSize + 'px';
});

// ==================== DRAWING FUNCTIONS ====================
function startDrawing(e) {
    isDrawing = true;
    hasDrawn = true;
    canvasOverlay.classList.add('hidden');
    draw(e);
}

function stopDrawing() {
    isDrawing = false;
    ctx.beginPath();
}

function draw(e) {
    if (!isDrawing) return;

    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    const x = (e.clientX - rect.left) * scaleX;
    const y = (e.clientY - rect.top) * scaleY;

    ctx.lineWidth = brushSize;
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#ffffff';

    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
}

// Touch support for mobile
function getTouchPos(e) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    return {
        x: (e.touches[0].clientX - rect.left) * scaleX,
        y: (e.touches[0].clientY - rect.top) * scaleY
    };
}

function handleTouchStart(e) {
    e.preventDefault();
    isDrawing = true;
    hasDrawn = true;
    canvasOverlay.classList.add('hidden');

    const pos = getTouchPos(e);
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
}

function handleTouchMove(e) {
    e.preventDefault();
    if (!isDrawing) return;

    const pos = getTouchPos(e);
    ctx.lineWidth = brushSize;
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#ffffff';
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
}

function handleTouchEnd(e) {
    e.preventDefault();
    isDrawing = false;
    ctx.beginPath();
}

// ==================== EVENT LISTENERS ====================
// Mouse events
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseleave', stopDrawing);

// Touch events
canvas.addEventListener('touchstart', handleTouchStart, { passive: false });
canvas.addEventListener('touchmove', handleTouchMove, { passive: false });
canvas.addEventListener('touchend', handleTouchEnd, { passive: false });

// Clear button
clearBtn.addEventListener('click', () => {
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    hasDrawn = false;
    canvasOverlay.classList.remove('hidden');

    // Reset results to empty state
    resultsContent.innerHTML = `
        <div class="empty-state">
            <div class="empty-state-icon">
                <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
                    <line x1="12" y1="17" x2="12.01" y2="17"/>
                </svg>
            </div>
            <h3>No Prediction Yet</h3>
            <p>Draw a digit on the canvas and click "Predict Digit" to see the AI's prediction</p>
        </div>
    `;

    // Add animation
    clearBtn.style.transform = 'scale(0.95)';
    setTimeout(() => {
        clearBtn.style.transform = 'scale(1)';
    }, 100);
});

// ==================== PREDICTION FUNCTION ====================
predictBtn.addEventListener('click', async () => {
    if (!hasDrawn) {
        showNotification('Please draw a digit first!', 'warning');
        return;
    }

    // Show loading state
    resultsContent.innerHTML = `
        <div style="text-align: center;">
            <div class="loading"></div>
            <p style="margin-top: 1rem; color: var(--text-secondary);">Analyzing your digit...</p>
        </div>
    `;

    // Add button animation
    predictBtn.style.transform = 'scale(0.95)';
    setTimeout(() => {
        predictBtn.style.transform = 'scale(1)';
    }, 100);

    try {
        // Get canvas image data
        const imageData = canvas.toDataURL('image/png');

        // Send to backend - use /api/predict-digit for Vercel
        const response = await fetch('/api/predict-digit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: imageData })
        });

        if (!response.ok) {
            throw new Error('Prediction failed');
        }

        const data = await response.json();
        displayPrediction(data.prediction, data.confidence);

    } catch (error) {
        console.error('Error:', error);
        resultsContent.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">
                    <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="15" y1="9" x2="9" y2="15"/>
                        <line x1="9" y1="9" x2="15" y2="15"/>
                    </svg>
                </div>
                <h3>Prediction Failed</h3>
                <p>There was an error processing your digit. Please try again.</p>
            </div>
        `;
        showNotification('Error making prediction. Please try again.', 'error');
    }
});

// ==================== DISPLAY PREDICTION ====================
function displayPrediction(digit, confidence) {
    // Use actual confidence from backend
    const confidencePercent = parseFloat(confidence) || 0;

    resultsContent.innerHTML = `
        <div class="prediction-display">
            <div class="prediction-digit">${digit}</div>
            <div class="prediction-label">Predicted Digit</div>
            
            <div class="confidence-section">
                <div class="confidence-label">Confidence Score</div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: 0%"></div>
                </div>
                <div class="confidence-value">${confidencePercent.toFixed(1)}%</div>
            </div>
        </div>
    `;

    // Animate confidence bar
    setTimeout(() => {
        const fillElement = resultsContent.querySelector('.confidence-fill');
        if (fillElement) {
            fillElement.style.width = confidencePercent + '%';
        }
    }, 100);

    // Trigger confetti effect for high confidence
    if (confidencePercent > 90) {
        createConfetti();
    }
}

// ==================== NOTIFICATION SYSTEM ====================
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'error' ? 'linear-gradient(135deg, #f5576c 0%, #f093fb 100%)' : 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'};
        color: white;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        animation: slideInRight 0.3s ease;
        font-weight: 600;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ==================== CONFETTI EFFECT ====================
function createConfetti() {
    const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'];
    const confettiCount = 50;

    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.style.cssText = `
            position: fixed;
            width: 10px;
            height: 10px;
            background: ${colors[Math.floor(Math.random() * colors.length)]};
            top: 50%;
            left: 50%;
            opacity: 1;
            border-radius: 50%;
            pointer-events: none;
            z-index: 999;
        `;
        document.body.appendChild(confetti);

        const angle = (Math.PI * 2 * i) / confettiCount;
        const velocity = 5 + Math.random() * 5;
        const vx = Math.cos(angle) * velocity;
        const vy = Math.sin(angle) * velocity;

        let x = 0;
        let y = 0;
        let opacity = 1;

        const animate = () => {
            x += vx;
            y += vy + 2; // gravity
            opacity -= 0.02;

            confetti.style.transform = `translate(${x}px, ${y}px) rotate(${x * 2}deg)`;
            confetti.style.opacity = opacity;

            if (opacity > 0) {
                requestAnimationFrame(animate);
            } else {
                confetti.remove();
            }
        };

        animate();
    }
}

// ==================== KEYBOARD SHORTCUTS ====================
document.addEventListener('keydown', (e) => {
    // Clear canvas with 'C' key
    if (e.key.toLowerCase() === 'c' && !e.ctrlKey && !e.metaKey) {
        clearBtn.click();
    }

    // Predict with 'Enter' key
    if (e.key === 'Enter' && hasDrawn) {
        predictBtn.click();
    }
});

// ==================== INITIALIZE ====================
document.addEventListener('DOMContentLoaded', () => {
    createParticles();

    // Add CSS for animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});

// ==================== PREVENT CONTEXT MENU ON CANVAS ====================
canvas.addEventListener('contextmenu', (e) => {
    e.preventDefault();
});
