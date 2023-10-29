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
    else
    if(request.action === "startScanning") {
        console.log("Start Scanning");
        startScanning();
        sendResponse({status: "ok"})
    }
    else
    if(request.action === "stopScanning") {
        console.log("Stop Scanning");
        if (scanningRectangle) {
            scanningRectangle.remove();
        }
        sendResponse({status: "ok"})
    }

});




let isSelecting = false;
let startX, startY;
let scanningRectangle = null;

// document.addEventListener('mousedown', function (event) {
//   isSelecting = true;
//   startX = event.clientX;
//   startY = event.clientY;
// });



function startScanning() {
    const selection = window.getSelection();
    if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();
    
        if (scanningRectangle) {
            scanningRectangle.remove();
        }

        var scanOffset = 20;

        scanningRectangle = document.createElement('div');
        scanningRectangle.className = 'highlight-rectangle';
        // scanningRectangle.style.top = rect.top-20 + 'px';
        // scanningRectangle.style.left = rect.left-20 + 'px';
        // scanningRectangle.style.width = rect.width+40 + 'px';
        // scanningRectangle.style.height = rect.height+40 + 'px';


        // Calculate scroll offsets
        const scrollX = window.scrollX;
        const scrollY = window.scrollY;

        scanningRectangle.style.top = rect.top +scrollY-scanOffset+ 'px';
        scanningRectangle.style.left = rect.left +scrollX-scanOffset+ 'px';
        scanningRectangle.style.width = rect.width + 2*scanOffset+ 'px';
        scanningRectangle.style.height = rect.height +2*scanOffset+ 'px';

        const scanningLine = document.createElement('div');
        scanningLine.className = 'scanning-line';
        scanningRectangle.appendChild(scanningLine);

        document.body.appendChild(scanningRectangle);
    }
    sendResponse({status: "ok"})
};




const styleElement = document.createElement('style');
styleElement.type = 'text/css';

// Define your CSS
const css = `
  .highlight-rectangle {
    position: absolute;
    pointer-events: none;
    box-shadow: inset 0 0 20px gray;
    overflow: hidden;
    border-radius: 20px;
  }

  .scanning-line {
    position: absolute;
    width: 100%;
    height: 2px;
    background: gray;
    animation: scan 1s linear infinite alternate;
  }

  @keyframes scan {
    0% {
      top: 0;
    }
    100% {
      top: 100%;
    }
  }
`;

// Set the CSS code in the <style> element
styleElement.textContent = css;

// Append the <style> element to the document's <head>
document.head.appendChild(styleElement);