let currentStep = 0;
const steps = document.querySelectorAll(".form-step");
const nextBtn = document.getElementById("nextBtn");
const prevBtn = document.getElementById("prevBtn");
const submitBtn = document.getElementById("submitBtn");

function showStep(n) {
    steps.forEach((step, index) => {
        step.classList.remove("active");
        if (index === n) step.classList.add("active");
    });

    prevBtn.classList.toggle("hidden", n === 0);
    nextBtn.classList.toggle("hidden", n === steps.length - 1);
    submitBtn.classList.toggle("hidden", n !== steps.length - 1);
}

nextBtn.addEventListener("click", () => {
    if (currentStep < steps.length - 1) currentStep++;
    showStep(currentStep);
});

prevBtn.addEventListener("click", () => {
    if (currentStep > 0) currentStep--;
    showStep(currentStep);
});

showStep(currentStep);

// Soumettre le formulaire quand on clique sur "S’inscrire"
submitBtn.addEventListener("click", function (e) {
    e.preventDefault(); // empêche tout bug d'affichage
    document.getElementById("registerForm").submit(); // soumission réelle du formulaire
});
