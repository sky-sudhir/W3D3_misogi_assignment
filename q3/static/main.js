// Main JavaScript file for Adaptive Prompt Optimizer

// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded");

  // Add a class to indicate the page is ready
  document.body.classList.add("page-loaded");

  // Make sure the form exists before adding event listeners
  const form = document.getElementById("optimizeForm");
  if (form) {
    console.log("Form found, adding event listeners");
  } else {
    console.error("Form not found!");
  }

  // Check if the tools are available in the template
  const toolOptions = document.querySelectorAll("#tool option");
  console.log(`Found ${toolOptions.length} tool options`);

  // Add debugging for API calls
  window.debugFetch = async function (url, options) {
    console.log(`Making fetch request to: ${url}`);
    console.log("Request options:", options);

    try {
      const response = await fetch(url, options);
      console.log("Response status:", response.status);
      const data = await response.json();
      console.log("Response data:", data);
      return { response, data };
    } catch (error) {
      console.error("Fetch error:", error);
      throw error;
    }
  };
});
