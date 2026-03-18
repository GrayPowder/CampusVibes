const header = document.querySelector(".header");
window.addEventListener("scroll", () => {
    header.classList.toggle("sticky", window.scrollY > 0);
});

const profileToggle = document.getElementById("profileToggle");
const profileDropdown = document.getElementById("profileDropdown");
profileToggle.addEventListener("click", () => {
    profileDropdown.style.display = profileDropdown.style.display === "block" ? "none" : "block";
});
window.addEventListener("click", (e) => {
    if (!profileToggle.contains(e.target) && !profileDropdown.contains(e.target)) {
        profileDropdown.style.display = "none";
    }
});

const modal = document.getElementById("imgModal");
const modalImg = document.getElementById("modalImg");
const captionText = document.getElementById("caption");
const modalClose = document.querySelector(".modal-close");

document.querySelectorAll(".team-img").forEach(img => {
    img.addEventListener("click", () => {
        modal.style.display = "block";
        modalImg.src = img.src;
        captionText.innerText = img.alt;
    });
});

modalClose.addEventListener("click", () => modal.style.display = "none");
modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.style.display = "none";
});