chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
	const jobDescription = message.jobDescription;
	return true;
});


// Add an event listener to the popup button
// document.getElementById('downloadButton').addEventListener('click', function() {
//     // Get the job description or any other required data here

//     // Assuming you have the job description in a variable named 'jobDescription'
    
//     // Fetch and generate the PDF
// 	console.log("HERE!")
//     fetch(`https://resumegen.onrender.com/generate_pdf`, {
//         method: 'GET',
//         headers: {
//             'Content-Type': 'multipart/form-data',
//         }
//     })
//     .then((response) => response.blob())
//     .then((blob) => {
//         const filename = 'job_description.pdf';
//         const reader = new FileReader();
//         reader.onload = () => {
//             const buffer = reader.result;
//             const blobUrl = `data:${blob.type};base64,${btoa(new Uint8Array(buffer).reduce((data, byte) => data + String.fromCharCode(byte), ''))}`;
            
//             // Trigger the download when the PDF is ready
//             chrome.downloads.download({
//                 url: blobUrl,
//                 filename: filename,
//                 saveAs: true,
//                 conflictAction: "uniquify"
//             }, () => {
//                 // Handle the download completion here
//                 console.log('PDF download complete');
//             });
//         };
//         reader.readAsArrayBuffer(blob);
//     })
//     .catch((error) => {
//         // Handle any errors that occur during the PDF generation
//         console.error('Failed to generate PDF:', error);
//     });
// });


