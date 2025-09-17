export function handlePasswordVisibility(e) {
    const passwordInput = e.target.closest(".form__group").querySelector("input");
    
    //Change visibility
    const isPassword = passwordInput.type === "password";
    passwordInput.type = isPassword ? "text" : "password";

    const icon = e.target;
    icon.classList.remove(isPassword ? "ri-eye-fill" : "ri-eye-off-fill");
    icon.classList.add(isPassword ? "ri-eye-off-fill" : "ri-eye-fill");
}