chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === "getJobDescription") {
    
    // Get the selected text
    function getSelectedText() {
      let selectedText = "";

      if (window.getSelection) {
        // Modern browsers
        const selection = window.getSelection();
        selectedText = selection.toString();
      } else if (document.selection && document.selection.type != "Control") {
        // IE 8 and earlier
        selectedText = document.selection.createRange().text;
      }

      return selectedText;
    }

    // Call the function to get the selected text
    const selectedText = getSelectedText();

    if (selectedText) {
    //   console.log("Selected Text: ", selectedText);
    jobDescription = selectedText;
    console.log("Job Description:", jobDescription);
    sendResponse({ jobDescription });
    } else {
      console.log("No text selected.");
    }

  }
});