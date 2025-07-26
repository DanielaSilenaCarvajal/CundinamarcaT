document.addEventListener('DOMContentLoaded', function() {
    // 1. Actualizar año en el footer
    const updateYear = () => {
        document.getElementById('year').textContent = new Date().getFullYear();
    };

    // 2. Configuración del carrusel
    const setupCarousel = () => {
        const carousel = document.querySelector('.carousel');
        const slides = document.querySelectorAll('.carousel-slide');
        const dotsContainer = document.querySelector('.carousel-dots');
        let currentSlide = 0;
        const slideCount = slides.length;
        let carouselInterval;

        // Crear puntos de navegación
        const createDots = () => {
            slides.forEach((_, index) => {
                const dot = document.createElement('span');
                dot.classList.add('dot');
                dot.dataset.slide = index;
                dotsContainer.appendChild(dot);
            });
        };

        // Actualizar estado activo
        const updateActiveState = (slideIndex) => {
            document.querySelectorAll('.dot').forEach(dot => {
                dot.classList.toggle('active', parseInt(dot.dataset.slide) === slideIndex);
            });
        };

        // Ir a slide específico
        const goToSlide = (slideIndex) => {
            carousel.style.transform = `translateX(-${slideIndex * 100}%)`;
            currentSlide = slideIndex;
            updateActiveState(slideIndex);
        };

        // Slide siguiente
        const nextSlide = () => goToSlide((currentSlide + 1) % slideCount);
        
        // Slide anterior
        const prevSlide = () => goToSlide((currentSlide - 1 + slideCount) % slideCount);

        // Iniciar autoplay
        const startAutoplay = () => {
            carouselInterval = setInterval(nextSlide, 5000);
        };

        // Configurar eventos
        const setupEvents = () => {
            document.querySelector('.next').addEventListener('click', () => {
                nextSlide();
                resetAutoplay();
            });
            
            document.querySelector('.prev').addEventListener('click', () => {
                prevSlide();
                resetAutoplay();
            });

            document.querySelectorAll('.dot').forEach(dot => {
                dot.addEventListener('click', () => {
                    goToSlide(parseInt(dot.dataset.slide));
                    resetAutoplay();
                });
            });
        };

        // Reiniciar autoplay
        const resetAutoplay = () => {
            clearInterval(carouselInterval);
            startAutoplay();
        };

        // Inicializar
        createDots();
        updateActiveState(0);
        setupEvents();
        startAutoplay();
    };

    // 3. Funcionalidad de los botones "Ver más"
    const setupAttractionButtons = () => {
        document.querySelectorAll('.attraction-card').forEach(card => {
            card.addEventListener('click', (e) => {
                // Verificar si el clic no fue en un enlace interno
                if (!e.target.closest('.btn-link')) {
                    const link = card.querySelector('a[href]');
                    if (link) {
                        window.location.href = link.getAttribute('href');
                    }
                }
            });
        });
    };

    // 4. Efecto de carga suave
    const setupPageTransition = () => {
        document.body.style.opacity = '0';
        setTimeout(() => {
            document.body.style.transition = 'opacity 0.5s ease';
            document.body.style.opacity = '1';
        }, 100);
    };

    // Inicializar todas las funciones
    updateYear();
    setupCarousel();
    setupAttractionButtons();
    setupPageTransition();
});