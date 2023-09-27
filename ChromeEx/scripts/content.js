const jobDescription = document.body.textContent;
console.log(jobDescription)
chrome.runtime.sendMessage({ jobDescription });
