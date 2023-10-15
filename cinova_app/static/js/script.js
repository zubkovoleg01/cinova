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

document.addEventListener('DOMContentLoaded', function() {
    function initializeSlider(sliderId) {
        const sliderContainer = document.querySelector(`#${sliderId} .slider-container`);
        const articles = sliderContainer.querySelectorAll('article.slider');
        const prevButton = document.querySelector(`#${sliderId} .prev-button`);
        const nextButton = document.querySelector(`#${sliderId} .next-button`);
        let currentSlide = 0;
        const slidesToShow = 4;
        const slidesToScroll = 1;
        const autoSlideInterval = 20000;
        let animationFrame;

        function showSlides(startIndex) {
            for (let i = 0; i < articles.length; i++) {
                const isVisible = i >= startIndex && i < startIndex + slidesToShow;
                articles[i].style.display = isVisible ? 'block' : 'none';
            }
        }

        function nextSlides() {
            currentSlide += slidesToScroll;

            if (currentSlide >= articles.length - slidesToShow + 1) {
                currentSlide = 0;
            }

            animateSlides();
        }

        function prevSlides() {
            currentSlide -= slidesToScroll;

            if (currentSlide < 0) {
                currentSlide = articles.length - slidesToShow;
            }

            animateSlides();
        }

        function animateSlides() {
            let start = null;
            const startIndex = currentSlide;

            function step(timestamp) {
                if (!start) start = timestamp;
                const progress = timestamp - start;

                showSlides(startIndex + Math.min(1, progress / 300) * slidesToScroll);

                if (progress < 300) {
                    animationFrame = requestAnimationFrame(step);
                }
            }

            if (animationFrame) {
                cancelAnimationFrame(animationFrame);
            }

            animationFrame = requestAnimationFrame(step);
        }

        function autoSlide() {
            nextSlides();
            setTimeout(autoSlide, autoSlideInterval);
        }

        showSlides(currentSlide);

        nextButton.addEventListener('click', nextSlides);
        prevButton.addEventListener('click', prevSlides);

        setTimeout(autoSlide, autoSlideInterval);
    }

    initializeSlider('popular-slider');
    initializeSlider('new-slider');
});

document.addEventListener('DOMContentLoaded', function() {
    let scrollButton = document.getElementById('myBtn');

    function scrollToTop() {
        let position = document.documentElement.scrollTop || document.body.scrollTop;

        if (position > 0) {
            window.requestAnimationFrame(scrollToTop);
            window.scrollTo(0, position - 80);
        }
    }

    window.onscroll = function() {
        if (document.body.scrollTop > 1100 || document.documentElement.scrollTop > 1100) {
            scrollButton.parentNode.classList.add('show');
        } else {
            scrollButton.parentNode.classList.remove('show');
        }
    };

    scrollButton.addEventListener('click', scrollToTop);
});



