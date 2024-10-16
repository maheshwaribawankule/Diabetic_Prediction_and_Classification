// script.js

document.addEventListener("DOMContentLoaded", () => {
      const form = document.getElementById("predictionForm");
      
      // Toggle for dark mode
      const switchMode = document.getElementById("switch-mode");
      switchMode.addEventListener("change", () => {
          document.body.classList.toggle("dark-mode");
      });
  
      // Form submission handler
      form.addEventListener("submit", function(event) {
          // Basic validation for positive numbers
          const inputs = form.querySelectorAll("input[type='number']");
          for (let input of inputs) {
              if (input.value < 0) {
                  alert(`${input.placeholder} must be a positive number.`);
                  event.preventDefault(); // Prevent form submission
                  return;
              }
          }
  
          // Optional: Display a confirmation message (can be styled as needed)
          alert("Form submitted successfully!");
      });
  });
  