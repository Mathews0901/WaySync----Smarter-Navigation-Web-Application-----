// LOGIN
const loginForm = document.getElementById('loginForm');
if (loginForm) {
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const res = await fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: document.getElementById('loginEmail').value,
        password: document.getElementById('loginPassword').value
      })
    });
    const data = await res.json();
    if (data.token) {
      localStorage.setItem('token', data.token);
      alert('Login successful!');
      window.location.href = '/dashboard';
    } else {
      alert(data.msg || 'Login failed');
    }
  });
}

// REGISTER
const registerForm = document.getElementById('registerForm');
if (registerForm) {
  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const res = await fetch('/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: document.getElementById('registerUsername').value,
        email: document.getElementById('registerEmail').value,
        password: document.getElementById('registerPassword').value
      })
    });
    const data = await res.json();
    alert(data.msg || 'Registration complete!');
  });
}

// GOOGLE MAPS FUNCTIONS
let map;
let directionsRenderer;
let directionsService;

function initMap() {
  const center = { lat: 28.6139, lng: 77.2090 }; // New Delhi

  // Initialize map
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: center,
  });

  // Initialize directions services
  directionsService = new google.maps.DirectionsService();
  directionsRenderer = new google.maps.DirectionsRenderer();
  directionsRenderer.setMap(map);

  // Load markers from backend
  fetch("/api/markers")
    .then(res => res.json())
    .then(data => {
      data.forEach(marker => {
        new google.maps.Marker({
          position: { lat: marker.lat, lng: marker.lng },
          map,
          title: marker.label
        });
      });
    })
    .catch(err => console.error("Error loading markers:", err));
}

function getRoute() {
  const origin = document.getElementById("origin").value;
  const destination = document.getElementById("destination").value;

  if (!origin || !destination) {
    alert("Please enter both origin and destination.");
    return;
  }

  fetch(`/api/directions?origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(destination)}`)
    .then(res => res.json())
    .then(data => {
      if (data.routes && data.routes.length > 0) {
        directionsRenderer.setDirections(data);
      } else {
        alert("No route found.");
      }
    })
    .catch(err => console.error("Error fetching directions:", err));
}