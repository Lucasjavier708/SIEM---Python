class TypeWriter {
  constructor(element) {
    this.element = element;
    this.text = 'Lucas Javier Pizarro';
    this.speed = 80;
    this.index = 0;
    setTimeout(() => this.type(), 300);
  }

  type() {
    if (this.index < this.text.length) {
      this.element.textContent += this.text.charAt(this.index);
      this.index++;
      setTimeout(() => this.type(), this.speed);
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const typingElement = document.querySelector('.typing-text');
  if (typingElement) {
    new TypeWriter(typingElement);
  }

  initProyectos();
  initSmoothScroll();
  initLogoAnimation();
  initLabSlideshow();
  createMatrixEffects();
});

function initProyectos() {
  const proyCards = document.querySelectorAll('.proyecto-card');
  const imgDisplay = document.getElementById('proyImgDisplay');
  const proyectosCardsWrapper = document.querySelector('.proyectos-cards-wrapper');
  
  if (proyCards.length > 0 && imgDisplay) {
    proyCards[0].classList.add('active');
  }
  
  proyCards.forEach((card) => {
    card.addEventListener('mouseenter', () => {
      const imgUrl = card.getAttribute('data-img');
      if (imgUrl) {
        imgDisplay.style.opacity = '0';
        setTimeout(() => {
          imgDisplay.src = imgUrl;
          imgDisplay.style.opacity = '1';
        }, 250);
      }
    });
  });

  // Scroll fade effect
  if (proyectosCardsWrapper) {
    const scrollContainer = proyectosCardsWrapper.querySelector('.proyectos-cards');
    if (scrollContainer) {
      scrollContainer.addEventListener('scroll', () => {
        proyCards.forEach((card) => {
          const rect = card.getBoundingClientRect();
          const containerRect = scrollContainer.getBoundingClientRect();
          
          // Calcular distancia desde el top
          const distanceFromTop = rect.top - containerRect.top;
          const maxDistance = 150;
          
          if (distanceFromTop < 0) {
            // Tarjeta sale por arriba - fade out
            const opacity = Math.max(0, 1 + (distanceFromTop / maxDistance));
            card.style.opacity = opacity;
          } else if (rect.bottom > containerRect.bottom) {
            // Tarjeta sale por abajo - fade out
            const overflow = rect.bottom - containerRect.bottom;
            const opacity = Math.max(0, 1 - (overflow / maxDistance));
            card.style.opacity = opacity;
          } else {
            // Tarjeta visible - opacity 1
            card.style.opacity = '1';
          }
        });
      });
    }
  }
}

function initSmoothScroll() {
  const links = document.querySelectorAll('a[href^="#"]');
  links.forEach(link => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      if (href === '#') return;
      e.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        const offsetTop = target.offsetTop - 80;
        window.scrollTo({ top: offsetTop, behavior: 'smooth' });
      }
    });
  });
}

function initLogoAnimation() {
  const logo = document.getElementById('animLogo');
  if (!logo) return;
  window.addEventListener('scroll', throttle(() => {
    const scrollPos = window.pageYOffset;
    const bounceAmount = Math.sin(scrollPos / 50) * 10;
    logo.style.transform = `translateY(${bounceAmount}px)`;
  }, 30));
}

function initLabSlideshow() {
  const slides = document.querySelectorAll('.lab-slide');
  if (slides.length === 0) return;
  
  let currentSlide = 0;
  setInterval(() => {
    slides.forEach(slide => slide.style.opacity = '0');
    slides[currentSlide].style.opacity = '1';
    currentSlide = (currentSlide + 1) % slides.length;
  }, 5000);
}

function createMatrixEffects() {
  const container = document.querySelector('body');
  
  // Destellos neón
  setInterval(() => {
    const destello = document.createElement('div');
    destello.style.position = 'fixed';
    destello.style.pointerEvents = 'none';
    destello.style.zIndex = '0';
    destello.style.width = '40px';
    destello.style.height = '40px';
    destello.style.borderRadius = '50%';
    destello.style.background = 'radial-gradient(circle, ' + 
      (Math.random() > 0.5 ? '#00d9ff' : '#ff1493') + ', transparent)';
    destello.style.filter = 'blur(10px)';
    destello.style.left = Math.random() * 100 + '%';
    destello.style.top = Math.random() * 100 + '%';
    
    container.appendChild(destello);
    
    let opacity = 1;
    const fade = setInterval(() => {
      opacity -= 0.08;
      destello.style.opacity = opacity;
      if (opacity <= 0) {
        clearInterval(fade);
        destello.remove();
      }
    }, 60);
  }, 3500);

  // CIRCUIT PARTICLES - Símbolos de circuitos cayendo (MATRIX LLUVIA)
  const circuitChars = ['║', '═', '╭', '╮', '╰', '╯', '╬', '┼', '█', '▮', '▐', '▌', '[', ']', '(', ')', '↓', '↑', '→', '←', '●', '◉', '◆', '▼', '▲', '○'];
  
  setInterval(() => {
    const particle = document.createElement('div');
    particle.classList.add('binary-particle');
    particle.textContent = circuitChars[Math.floor(Math.random() * circuitChars.length)];
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = '-50px';
    
    const duration = 3 + Math.random() * 2;
    particle.style.animationDuration = duration + 's';
    
    // GLOW AZUL PURO (como circuitos)
    const blueGlow = '#21ff09';
    particle.style.color = blueGlow;
    particle.style.textShadow = `0 0 10px ${blueGlow}, 0 0 20px ${blueGlow}, 0 0 30px rgba(0, 217, 255, 0.5)`;
    particle.style.fontWeight = '700';
    particle.style.fontSize = '1.4rem';
    
    container.appendChild(particle);
    
    setTimeout(() => particle.remove(), duration * 1000);
  }, 300);
}

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

// FUNCIONES DE SCROLL PROYECTOS
function scrollProyectosUp() {
  const scrollContainer = document.querySelector('.proyectos-cards');
  if (scrollContainer) {
    scrollContainer.scrollBy({
      top: -150,
      behavior: 'smooth'
    });
  }
}

function scrollProyectosDown() {
  const scrollContainer = document.querySelector('.proyectos-cards');
  if (scrollContainer) {
    scrollContainer.scrollBy({
      top: 150,
      behavior: 'smooth'
    });
  }
}

// ANIMACIÓN DE PUNTITO REBOTANDO EN ONDA SINUSOIDAL
function initBouncingPulse() {
  const dividers = document.querySelectorAll('.animated-divider');
  
  dividers.forEach(divider => {
    const pulse = divider.querySelector('.tunnel-pulse');
    if (!pulse) return;
    
    let time = 0;
    let speed = Math.random() * 0.000 + 0.001; // velocidad más lenta
    let waveAmplitude = 1.5; // altura de la onda (0-1)
    let waveFrequency = Math.random() *1.5 + 10.3; // frecuencia de la onda
    
    function animate() {
      const maxHeight = divider.offsetHeight - 14;
      const maxWidth = divider.offsetWidth - 14;
      
      // Movimiento horizontal continuo
      time += speed;
      if (time > 1) {
        time = 0; // reiniciar ciclo
      }
      
      // Posición X (de lado a lado)
      const posX = time;
      
      // Posición Y (onda sinusoidal)
      const posY = 0.5 + Math.sin(time * Math.PI * 2 * waveFrequency) * waveAmplitude;
      
      // Crear destellos ocasionalmente
      if (Math.random() > 0.88) {
        createTrail(divider, posX * maxWidth, posY * maxHeight);
      }
      
      pulse.style.left = (posX * maxWidth) + 'px';
      pulse.style.top = (posY * maxHeight) + 'px';
      requestAnimationFrame(animate);
    }
    
    animate();
  });
  
  function createTrail(divider, xPos, yPos) {
    const trail = document.createElement('div');
    trail.className = 'pulse-trail';
    trail.style.left = xPos + 'px';
    trail.style.top = yPos + 'px';
    divider.appendChild(trail);
    
    setTimeout(() => trail.remove(), 800);
  }
}

// Inicializar cuando cargue el DOM
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initBouncingPulse);
} else {
  initBouncingPulse();
}

console.log('%cLucas Javier Pizarro', 'font-size: 20px; font-weight: bold; color: #00d9ff;');
console.log('%cCybersecurity & SOC L1 Specialist', 'font-size: 14px; color: #ff1493;');
console.log('%cGitHub: github.com/lucasjavier708', 'font-size: 12px; color: #00d9ff;');
