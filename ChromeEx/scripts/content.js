chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === "getJobDescription") {
    const jobDescription = document.body.textContent;
    sendResponse({ jobDescription });
  }
});