const steps = document.querySelectorAll(".stepper .step")
const radios = document.querySelectorAll('input[name="steps"]');
const sections = document.querySelectorAll('.main__step');

export function goStep(direction) {
    // Find the current index
    let currentIndex = Array.from(radios).findIndex(r => r.checked);

    // Determine the new index
    let newIndex;
    if (direction === 'next') {
        newIndex = Math.min(currentIndex + 1, radios.length - 1);
    }else if (typeof direction === 'number') {
        newIndex = Math.min(Math.max(direction - 1, 0), radios.length - 1);
    }else {
        return;
    }

    // Update radios
    radios.forEach((r, i) => r.checked = i === newIndex);

    // Update section visibility
    sections.forEach((s, i) => s.style.display = i === newIndex ? 'flex' : 'none');

    // Update visual stepper
    steps.forEach((s, i) => s.classList.toggle('step--active', i === newIndex));
}