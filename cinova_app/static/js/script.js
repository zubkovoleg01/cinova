// code for the slide carousel
document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.carousel-container');
    const slides = document.querySelectorAll('.carousel-slide');
    const prevBtn = document.querySelector('.carousel-prev');
    const nextBtn = document.querySelector('.carousel-next');

    let index = 0;

    // updating the slide position
    function updateSlidePosition() {
        container.style.transform = `translateX(-${index * 100}%)`;
    }

    // displaying a specific slide by index
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

    // automatic slide switching after a certain time interval
    setInterval(nextSlide, 5000);

});

// code for slider of popular and new blocks
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

        // for slide scrolling animation
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

    // initializing sliders by their ID
    initializeSlider('popular-slider');
    initializeSlider('new-slider');
});

// code for button up
document.addEventListener('DOMContentLoaded', function() {
    let scrollButton = document.getElementById('myBtn');

    // for smooth scrolling of the page to the top
    function scrollToTop() {
        let position = document.documentElement.scrollTop || document.body.scrollTop;

        if (position > 0) {
            window.requestAnimationFrame(scrollToTop);
            window.scrollTo(0, position - 80); // smooth page scrolling 80 pixels up
        }
    }

    // scrolling is only available at > 900 pixels
    window.onscroll = function() {
        if (document.body.scrollTop > 900 || document.documentElement.scrollTop > 900) {
            scrollButton.parentNode.classList.add('show');
        } else {
            scrollButton.parentNode.classList.remove('show');
        }
    };

    scrollButton.addEventListener('click', scrollToTop);
});

// code for slider of genre block
document.addEventListener('DOMContentLoaded', function() {
    var genreSection = document.querySelector('.genres-section');
    var genreBlocks = document.querySelectorAll('.genre-block');
    var prevArrow = document.querySelector('.prev-arrow');
    var nextArrow = document.querySelector('.next-arrow');
    var currentIndex = 0;
    var slidesPerPage = 8;

    function showSlides(startIndex) {
        genreBlocks.forEach(function(block, i) {
            if (i >= startIndex && i < startIndex + slidesPerPage) {
                block.style.display = 'inline-block';
            } else {
                block.style.display = 'none';
            }
        });
    }

    prevArrow.addEventListener('click', function() {
        currentIndex = (currentIndex <= 0) ? genreBlocks.length - slidesPerPage : currentIndex - slidesPerPage;
        showSlides(currentIndex);
    });

    nextArrow.addEventListener('click', function() {
        currentIndex = (currentIndex >= genreBlocks.length - slidesPerPage) ? 0 : currentIndex + slidesPerPage;
        showSlides(currentIndex);
    });

    showSlides(currentIndex);
});

// code for slider of persons block
document.addEventListener('DOMContentLoaded', function() {
    var personSlide = document.querySelector('.person-slide');
    var prevButtonP = document.querySelector('.prev-button-p');
    var nextButtonP = document.querySelector('.next-button-p');
    var slidesPerPage = 4;
    var currentOffset = 0;

    function showSlides() {
        var slides = personSlide.querySelectorAll('.slide');
        slides.forEach(function(slide, i) {
            slide.style.display = i >= currentOffset && i < currentOffset + slidesPerPage ? 'block' : 'none';
        });
    }

    function nextSlides() {
        currentOffset += slidesPerPage;
        if (currentOffset >= personSlide.children.length) {
            currentOffset = 0;
        }
        showSlides();
    }

    function prevSlides() {
        currentOffset -= slidesPerPage;
        if (currentOffset < 0) {
            currentOffset = personSlide.children.length - slidesPerPage;
        }
        showSlides();
    }

    prevButtonP.addEventListener('click', prevSlides);
    nextButtonP.addEventListener('click', nextSlides);

    showSlides();
});

