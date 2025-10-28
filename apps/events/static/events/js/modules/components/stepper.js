const steps = document.querySelectorAll(".stepper .step")
const radios = document.querySelectorAll('input[name="stepper"]');
const sections = document.querySelectorAll('.main__step');

export function goStep(direction) {
    // Find the current index
    let currentIndex = Array.from(radios).findIndex(r => r.checked);
    if (currentIndex < 0) currentIndex = 0;

    // Determine the new index
    let newIndex;

    if (direction === 'next') {
        newIndex = Math.min(currentIndex + 1, radios.length - 1);
    }else if(direction === 'prev') {
        newIndex = Math.max(currentIndex - 1, 0);
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

export const skipHandler = () => goStep("next");
export const goToListHandler = url => window.location.href = url

export function toggleSkip(button, enable, saveHandler) {
    if (enable) {
        button.setAttribute("data-skip", "");
        button.textContent = "Omitir";
        button.onclick = skipHandler
    } else {
        button.removeAttribute("data-skip");
        button.textContent = "Guardar";
        button.onclick = saveHandler || null;
    }
}

export function finishStepHandler(button, isSkippable, callback, url) {
    button.onclick = null;
    button.onclick = !isSkippable ? callback : goToListHandler.bind(null, url);
}