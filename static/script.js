document.addEventListener("DOMContentLoaded", function() {
    const links = document.querySelectorAll("a");
    links.forEach(link => {
        link.addEventListener("click", function(event) {
            event.preventDefault();
            const href = this.href;
            document.body.style.animation = "pageFadeOut 0.5s ease-in-out";
            setTimeout(() => {
                window.location = href;
            }, 500);
        });
    });
});
