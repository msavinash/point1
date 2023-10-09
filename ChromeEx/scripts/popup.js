// // document.addEventListener("DOMContentLoaded", function () {
// //     const downloadButton = document.getElementById("downloadButton");

// //     downloadButton.addEventListener("click", function () {
// //       chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
// //         const activeTab = tabs[0];
// //         const jobDescription = document.body.textContent; // Replace with the job description you want to send to the API

// //         chrome.runtime.sendMessage({ jobDescription }, function (response) {
// //           if (response.success) {
// //             // Handle the success response, e.g., display a success message.
// //           } else {
// //             // Handle the error response, e.g., display an error message.
// //           }
// //         });
// //       });
// //     });
// //   });




// document.getElementById('downloadButton').addEventListener('click', function () {
// 	// Send a message to the content script to get the job description
// 	// chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
// 	// 	chrome.tabs.sendMessage(tabs[0].id, { action: "getJobDescription" }, function (response) {
// 	// 		// console.log(response)
// 	// 		const jobDescription = response.jobDescription;
// 	// 		// Now, you have the job description content, and you can use it in your popup script
// 	// 		console.log("Job Description:", jobDescription);
// 	// 	});
// 	// });

// 	// Define the URL of the endpoint
// 	// const url = 'http://localhost:5000/'; // Replace with your actual endpoint URL
// 	// const url = 'https://resumegen.onrender.com/';

// 	// Make a GET request using fetch
// 	fetch(url)
// 		.then(response => {
// 			// Check if the response status is OK (200)
// 			if (response.ok) {
// 				// Parse the response JSON or text depending on the content type
// 				return response.text(); // Use response.json() if the response contains JSON
// 			} else {
// 				// Handle non-OK response (e.g., server error)
// 				throw new Error('Failed to fetch message');
// 			}
// 		})
// 		.then(message => {
// 			// Print the message
// 			console.log(message);
// 		})
// 		.catch(error => {
// 			// Handle any errors that occur during the request
// 			console.error('Error:', error);
// 		});

// });









document.getElementById('downloadButton').addEventListener('click', function () {


	chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
		chrome.tabs.sendMessage(tabs[0].id, { action: "getJobDescription" }, function (response) {
			// console.log(response)
			const jobDescription1 = response.jobDescription;
			// Now, you have the job description content, and you can use it in your popup script
			console.log("Job Description:", jobDescription1);
		});
	})

	// Get the job description or any other required data here
	const jobDescription = "Your job description here"; // Replace with actual data retrieval
	// const email = "user@example.com"; // Replace with actual email retrieval
	const email = "msavinash1139@gmail.com";

	// Fetch and generate the PDF
	console.log("HERE!");
	// fetch(`https://resumegen.onrender.com/generate_rankedpdf`, {
	const formData = new FormData();

	// Append your data to the FormData object
	formData.append('job_description', jobDescription);
	formData.append('email', email);

	// Make the fetch request with FormData
	console.log(formData)
	// fetch('http://localhost:5000/generate_rankedpdf', {
	//   method: 'POST',
	// body: formData, // Use the FormData object here

	// })
	fetch('http://localhost:5000/generate_getrankedpdf', {
		method: 'GET',
		// body: formData, // Use the FormData object here
		headers: {
			        'Content-Type': 'multipart/form-data',
			    }

	})
	.then((response) => response.blob())
	.then((blob) => {
		console.log("HERE2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		const filename = 'job_description.pdf';
		const reader = new FileReader();
		reader.onload = () => {
			const buffer = reader.result;
			const blobUrl = `data:${blob.type};base64,${btoa(new Uint8Array(buffer).reduce((data, byte) => data + String.fromCharCode(byte), ''))}`;

			// Trigger the download when the PDF is ready
			chrome.downloads.download({
				url: blobUrl,
				filename: filename,
				saveAs: true,
				conflictAction: "uniquify"
			}, () => {
				// Handle the download completion here
				console.log('PDF download complete');
			});
		};
		reader.readAsArrayBuffer(blob);
	})
	.catch((error) => {
		// Handle any errors that occur during the PDF generation
		console.error('Failed to generate PDF:', error);
	});
});