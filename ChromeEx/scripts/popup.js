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







function downloadPdf(userEmail) {
		// userEmail = null;
		
		jobDescription = null;
		chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
			chrome.tabs.sendMessage(tabs[0].id, { action: "getJobDescription" }, function (response) {
				// console.log(response)
				jobDescription = response.jobDescription;
				// Now, you have the job description content, and you can use it in your popup script
				console.log("Job Description:", jobDescription);
			});
		})

		// Get the job description or any other required data here
		// const jobDescription = "Your job description here"; // Replace with actual data retrieval
		// const email = "user@example.com"; // Replace with actual email retrieval

		// Fetch and generate the PDF
		console.log("HERE!");
		console.log(jobDescription);
		console.log(userEmail);
		// fetch(`https://resumegen.onrender.com/generate_rankedpdf`, {
		const formData = new FormData();

		// Append your data to the FormData object
		formData.append('job_description', jobDescription);
		formData.append('email', userEmail);

		// Make the fetch request with FormData
		console.log(formData)
		// fetch('http://localhost:5000/generate_rankedpdf', {
		//   method: 'POST',
		// body: formData, // Use the FormData object here

		// })
		fetch('https://resumegen.onrender.com/generate_rankedpdf', {
			method: 'POST',
			body: formData // Use the FormData object here
			// headers: {
			// 	        'Content-Type': 'multipart/form-data',
			// 	    }

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
	}













document.addEventListener('DOMContentLoaded', function () {
	// Initialize the Google Sign-In API with your client ID
	// gapi.load('auth2', function () {
	// 	gapi.auth2.init({
	// 		client_id: '1069981472662-oqkfi6ghf9qalvt13rlrnd67rtvbe4gd.apps.googleusercontent.com',
	// 	});
	// });

	// Function to update UI based on sign-in status
	function updateUI(isSignedIn, userEmail) {
		const loginStatus = document.getElementById('loginStatus');
		const buttons = document.getElementById('buttons');

		if (isSignedIn) {
			console.log("signed in")
			loginStatus.innerText = `Signed in as: ${userEmail}`;
			buttons.innerHTML = `
		  <button id="downloadButton">Download PDF</button>
		  <button id="signOutButton">Sign Out</button>
		`;
			document.getElementById('signOutButton').addEventListener('click', signOut);
			document.getElementById('downloadButton').addEventListener('click', function () {
				downloadPdf(userEmail);
			});
		} else {
			console.log("not signed in")
			loginStatus.innerText = 'Not signed in';
			buttons.innerHTML = `
		  <button id="signInButton">Sign In with Google</button>
		`;
			document.getElementById('signInButton').addEventListener('click', signIn);
		}
	}

	// Function to handle sign-in
	function signIn() {
		// gapi.auth2.getAuthInstance().signIn().then(function (user) {
		// 	// Store user's email in Chrome Storage
		// 	chrome.storage.sync.set({ 'userEmail': user.getBasicProfile().getEmail() });
		// 	updateUI(true, user.getBasicProfile().getEmail());
		// });
		chrome.identity.getAuthToken({ interactive: true }, function (token) {
			if (chrome.runtime.lastError) {
			console.error(chrome.runtime.lastError);
			return;
			}
			console.log('Token acquired:', token);
		
			// Make a request to the Google People API
			fetch('https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses', {
			headers: {
				'Authorization': 'Bearer ' + token,
			},
			})
			.then(response => {
				if (!response.ok) {
				throw new Error('Network response was not ok');
				}
				return response.json();
			})
			.then(data => {
				// Handle the response data here
				console.log('Data from People API:', data);
				userEmail = data.emailAddresses[0].value;
				chrome.storage.sync.set({ 'userEmail': userEmail });
				updateUI(true, userEmail);
			})
			.catch(error => {
				console.error('Error making request to People API:', error);
			});
		});

	}

	// // Function to handle sign-out
	// function signOut() {
	// 	gapi.auth2.getAuthInstance().signOut().then(function () {
	// 		// Clear user's email from Chrome Storage
	// 		chrome.storage.sync.remove('userEmail');
	// 		updateUI(false, '');
	// 	});
	// }


	// Function to handle sign-out
function signOut() {
    chrome.identity.getAuthToken({ interactive: false }, function (currentToken) {
        if (!chrome.runtime.lastError) {
            // Revoke the token
            fetch('https://accounts.google.com/o/oauth2/revoke?token=' + currentToken, {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            }).then(function (response) {
                if (response.status === 200) {
                    console.log('Token revoked successfully.');
                } else {
                    console.log('Error revoking token:', response.statusText);
                }
            });
            chrome.identity.removeCachedAuthToken({ token: currentToken }, function () {
                console.log('Token removed from cache.');
            });
            // userEmail = null; // Clear the user's email
			chrome.storage.sync.remove('userEmail');
            updateUI(false, null); // Update the UI to reflect sign-out
        } else {
            console.error(chrome.runtime.lastError);
        }
    });
}


	// // Check if the user is already signed in
	// gapi.load('auth2', function () {
	// 	chrome.storage.sync.get('userEmail', function (data) {
	// 		const userEmail = data.userEmail;
	// 		const isSignedIn = userEmail ? true : false;
	// 		updateUI(isSignedIn, userEmail);
	// 	});
	// });

	chrome.storage.sync.get('userEmail', function (data) {
		const userEmail = data.userEmail;
		const isSignedIn = userEmail ? true : false;
		updateUI(isSignedIn, userEmail);
	  });
});
