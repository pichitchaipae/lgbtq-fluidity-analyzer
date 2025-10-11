// ***********************************************************
// This support file is processed and loaded automatically before test files.
// You can change the location of this file or turn off automatically serving
// support files with the 'supportFile' configuration option.
// ***********************************************************

// Import Cypress commands
import './commands'

// Hide fetch/XHR requests from command log for cleaner output
const app = window.top;
if (!app.document.head.querySelector('[data-hide-command-log-request]')) {
  const style = app.document.createElement('style');
  style.innerHTML =
    '.command-name-request, .command-name-xhr { display: none }';
  style.setAttribute('data-hide-command-log-request', '');
  app.document.head.appendChild(style);
}

// Custom error handler
Cypress.on('uncaught:exception', (err, runnable) => {
  // Returning false prevents Cypress from failing the test
  // Add specific error messages you want to ignore
  if (err.message.includes('ResizeObserver')) {
    return false
  }
  return true
})
