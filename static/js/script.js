let isScrolling = false;

// Balloon images array
const balloonImages = [
    'static/images/ballon1.svg',
    'static/images/ballon2.svg',
    'static/images/ballon3.svg',
];

let isGeneratingBalloon = false;

window.addEventListener('scroll', () => {
    if (!isGeneratingBalloon) {
        isGeneratingBalloon = true;
        setTimeout(() => {
            createBalloonsOnScroll();  // Call the function to generate balloons
            isGeneratingBalloon = false;
        }, 500);  // Add a delay of 500ms between each balloon creation
    }
});

// Function to create balloons based on scroll position
function createBalloonsOnScroll() {
    const scrollPosition = window.scrollY;
    const windowHeight = window.innerHeight;

    // Balloon creation conditions based on scroll position
    if (scrollPosition + windowHeight >= 1000 && scrollPosition < 2000) {
        generateBalloon(); // Generate balloon between 1000px and 1500px
    }
    if (scrollPosition + windowHeight >= 2500 && scrollPosition < 3500) {
        generateBalloon(); // Generate balloon between 2000px and 2500px
    }
    if (scrollPosition + windowHeight >= 4000 && scrollPosition < 5000) {
        generateBalloon(); // Generate balloon between 3000px and 3500px
    }
    if (scrollPosition + windowHeight >= 5500 && scrollPosition < 6500) {
        generateBalloon(); // Generate balloon between 4000px and 4500px
    }
    // Add more conditions for other scroll positions if needed
}

// Function to generate a balloon at a random position
function generateBalloon() {
    const randomImage = balloonImages[Math.floor(Math.random() * balloonImages.length)];
    
    const balloon = document.createElement('img');
    balloon.src = randomImage;
    balloon.alt = 'Balloon';
    balloon.style.position = 'absolute';
    balloon.style.left = `${Math.random() * 100}%`; // Randomize horizontal position (0% to 100%)
    balloon.style.top = `${Math.random() * 100}%`; // Randomize vertical start position

    // Append the balloon to the .baloons container
    document.querySelector('.baloons').appendChild(balloon);
}

// Webcam access functionality
const videoElement = document.getElementById('webcam');  // Ensure you have a video element in HTML with this ID

// Check if the browser supports webcam access
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Access the webcam
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            // Set the source of the video element to the webcam stream
            videoElement.srcObject = stream;
        })
        .catch(function(error) {
            console.error("Error accessing the webcam: ", error);
        });
} else {
    alert("Your browser does not support webcam access.");
}
