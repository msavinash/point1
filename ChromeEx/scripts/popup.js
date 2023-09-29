// document.addEventListener("DOMContentLoaded", function () {
//     const downloadButton = document.getElementById("downloadButton");
  
//     downloadButton.addEventListener("click", function () {
//       chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
//         const activeTab = tabs[0];
//         const jobDescription = document.body.textContent; // Replace with the job description you want to send to the API
  
//         chrome.runtime.sendMessage({ jobDescription }, function (response) {
//           if (response.success) {
//             // Handle the success response, e.g., display a success message.
//           } else {
//             // Handle the error response, e.g., display an error message.
//           }
//         });
//       });
//     });
//   });




  document.getElementById('downloadButton').addEventListener('click', function() {
    // Send a message to the content script to get the job description
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    chrome.tabs.sendMessage(tabs[0].id, { action: "getJobDescription" }, function (response) {
        // console.log(response)
      const jobDescription = response.jobDescription;
      // Now, you have the job description content, and you can use it in your popup script
      console.log("Job Description:", jobDescription);
    });
  });
    // Get the job description or any other required data here

    // Assuming you have the job description in a variable named 'jobDescription'
    
    // Fetch and generate the PDF
	// console.log("HERE!")
    // const jobDescription = document.body.textContent;
    // console.log(jobDescription)
    // fetch(`https://resumegen.onrender.com/generate_pdf`, {
    //     method: 'GET',
    //     headers: {
    //         'Content-Type': 'multipart/form-data',
    //     }
    // })
    // .then((response) => response.blob())
    // .then((blob) => {
    //     const filename = 'job_description.pdf';
    //     const reader = new FileReader();
    //     reader.onload = () => {
    //         const buffer = reader.result;
    //         const blobUrl = `data:${blob.type};base64,${btoa(new Uint8Array(buffer).reduce((data, byte) => data + String.fromCharCode(byte), ''))}`;
            
    //         // Trigger the download when the PDF is ready
    //         chrome.downloads.download({
    //             url: blobUrl,
    //             filename: filename,
    //             saveAs: true,
    //             conflictAction: "uniquify"
    //         }, () => {
    //             // Handle the download completion here
    //             console.log('PDF download complete');
    //         });
    //     };
    //     reader.readAsArrayBuffer(blob);
    // })
    // .catch((error) => {
    //     // Handle any errors that occur during the PDF generation
    //     console.error('Failed to generate PDF:', error);
    // });
});