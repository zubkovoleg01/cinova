document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.carousel-container');
    const slides = document.querySelectorAll('.carousel-slide');
    const prevBtn = document.querySelector('.carousel-prev');
    const nextBtn = document.querySelector('.carousel-next');

    let index = 0;

    function updateSlidePosition() {
        container.style.transform = `translateX(-${index * 100}%)`;
    }

    function showSlide(i) {
        index = i;
        updateSlidePosition();
    }

    function nextSlide() {
        if (index < slides.length - 1) {
            index++;
        } else {
            index = 0;
        }
        updateSlidePosition();
    }

    function prevSlide() {
        if (index > 0) {
            index--;
        } else {
            index = slides.length - 1;
        }
        updateSlidePosition();
    }

    prevBtn.addEventListener('click', prevSlide);

    nextBtn.addEventListener('click', nextSlide);

    
    setInterval(nextSlide, 5000);

});


