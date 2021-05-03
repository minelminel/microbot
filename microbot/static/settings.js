console.log(`Loaded settings.js`);

$(document).ready(function () {
  
  /**
   * Toggle existing spinner between visible & hidden to provide
   * feedback about long-running processes.
   */
  function isLoading(show) {
    $(`#spinner`).fadeToggle(show);
  }

  /* Fetch and apply latest state from backend */
  $("#sync").on("click", function() {
    isLoading(true);
    location.reload();
  });

});
