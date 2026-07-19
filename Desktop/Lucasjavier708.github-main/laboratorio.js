// GALERÍA AUTOMÁTICA
const galleryImages = [
  './_DSC3268.JPG',
  './_DSC3301.jpg',
  './_DSC3271.jpg'
];

let currentGalleryIndex = 0;
const mainGalleryImg = document.getElementById('mainGalleryImg');

function nextGalleryImage() {
  mainGalleryImg.style.opacity = '0';
  setTimeout(() => {
    currentGalleryIndex = (currentGalleryIndex + 1) % galleryImages.length;
    mainGalleryImg.src = galleryImages[currentGalleryIndex];
    mainGalleryImg.style.opacity = '1';
  }, 400);
}

// Cambiar imagen cada 5 segundos
setInterval(nextGalleryImage, 5000);

// Agregar transición smooth
mainGalleryImg.style.transition = 'opacity 0.4s ease';

// CARRUSEL EQUIPOS (MÁQUINAS + DISPOSITIVOS) - INFINITO SIN GAPS
let equipmentIndex = 0;
const equipmentCards = document.querySelectorAll('.equipment-card');
const equipmentTrack = document.getElementById('equipmentTrack');
const totalEquipment = equipmentCards.length;

// Clonar tarjetas para efecto infinito
function cloneCardsForInfinite() {
  const firstCard = equipmentCards[0].cloneNode(true);
  const lastCard = equipmentCards[totalEquipment - 1].cloneNode(true);
  
  equipmentTrack.appendChild(firstCard);
  equipmentTrack.insertBefore(lastCard, equipmentTrack.firstChild);
}

function nextEquipment() {
  equipmentIndex++;
  updateEquipmentCarousel();
  
  // Cuando llega al final, vuelve al inicio sin transición
  if (equipmentIndex >= totalEquipment) {
    setTimeout(() => {
      equipmentTrack.style.transition = 'none';
      equipmentIndex = 0;
      updateEquipmentCarousel();
      setTimeout(() => {
        equipmentTrack.style.transition = 'transform 0.4s ease';
      }, 50);
    }, 400);
  }
}

function prevEquipment() {
  equipmentIndex--;
  
  if (equipmentIndex < 0) {
    equipmentTrack.style.transition = 'none';
    equipmentIndex = totalEquipment - 1;
    updateEquipmentCarousel();
    setTimeout(() => {
      equipmentTrack.style.transition = 'transform 0.4s ease';
      nextEquipment();
    }, 50);
  } else {
    updateEquipmentCarousel();
  }
}

function updateEquipmentCarousel() {
  const cardWidth = 280;
  const gap = 24;
  const offset = -(equipmentIndex + 1) * (cardWidth + gap);
  equipmentTrack.style.transform = `translateX(${offset}px)`;
  equipmentTrack.style.transition = 'transform 0.4s ease';
}

// Inicializar clones
cloneCardsForInfinite();

// CARRUSEL SOC
let socIndex = 0;
const socImages = document.querySelectorAll('.soc-image');
const socTrack = document.getElementById('socTrack');

function nextSoc() {
  socIndex = (socIndex + 1) % socImages.length;
  updateSocCarousel();
}

function prevSoc() {
  socIndex = (socIndex - 1 + socImages.length) % socImages.length;
  updateSocCarousel();
}

function updateSocCarousel() {
  const offset = -socIndex * 100; // 100% width
  socTrack.style.transform = `translateX(${offset}%)`;
}

// LOGO ANIMATION
window.addEventListener('scroll', throttle(() => {
  const logo = document.getElementById('animLogo');
  if (logo) {
    const scrollPos = window.pageYOffset;
    const bounceAmount = Math.sin(scrollPos / 50) * 10;
    logo.style.transform = `translateY(${bounceAmount}px)`;
  }
}, 30));

function throttle(func, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// KEYBOARD NAVIGATION
document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowLeft') prevEquipment();
  if (e.key === 'ArrowRight') nextEquipment();
});

console.log('%cREDLABORATORIO', 'font-size: 16px; font-weight: bold; color: #00d9ff;');
console.log('%cPurple Team Operations', 'font-size: 12px; color: #ff1493;');
