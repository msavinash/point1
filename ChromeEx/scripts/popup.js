function downloadPdf(userEmail, progressBar) {
	jobDescription = null;
	chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
		chrome.tabs.sendMessage(tabs[0].id, { action: "getJobDescription" }, function (response) {
			jobDescription = response.jobDescription;
			progressBar.style.width = '10%';
			console.log("Job Description:", jobDescription);

	console.log("Job Description:", jobDescription);
	console.log("User Email:", userEmail);
	const formData = new FormData();
	formData.append('job_description', jobDescription);
	formData.append('email', userEmail);
	progressBar.style.width = '50%';
	fetch('https://resumegen.onrender.com/generate_rankedpdf', {
		method: 'POST',
		body: formData
	})
		.then((response) => response.blob())
		.then((blob) => {
			progressBar.style.width = '70%';
			const filename = 'job_description.pdf';
			const reader = new FileReader();
			reader.onload = () => {
				progressBar.style.width = '80%';
				const buffer = reader.result;
				const blobUrl = `data:${blob.type};base64,${btoa(new Uint8Array(buffer).reduce((data, byte) => data + String.fromCharCode(byte), ''))}`;
				chrome.downloads.download({
					url: blobUrl,
					filename: filename,
					saveAs: true,
					conflictAction: "uniquify"
				}, () => {
					progressBar.style.width = '100%';
					console.log('PDF download complete');
				});
			};
			reader.readAsArrayBuffer(blob);
			progressBar.style.width = '0%';

		})
		.catch((error) => {
			console.error('Failed to generate PDF:', error);
		});
	});
});
}


document.addEventListener('DOMContentLoaded', function () {
	const progress = document.getElementById('progress');
  	const progressBar = document.getElementById('progress-bar');
	  progress.style.display = '';
	// progressBar.style.width = '50%';
	// $(".progress-bar").css("width", 50 + "%");
	console.log("progress bar", progressBar.style.width);

	function updateUI(isSignedIn, userEmail) {
		const loginStatus = document.getElementById('loginStatus');
		const buttons = document.getElementById('buttons');

		if (isSignedIn) {
			console.log("signed in")
			loginStatus.innerText = `Signed in as: ${userEmail}`;
			buttons.innerHTML = `
		  <button class="btn btn-success" id="downloadButton">Download PDF</button>
		  <button class="btn btn-danger" id="signOutButton">Sign Out</button>
		`;
			document.getElementById('signOutButton').addEventListener('click', signOut);
			document.getElementById('downloadButton').addEventListener('click', function () {
				downloadPdf(userEmail, progressBar);
			progressBar.style.width = '0%';

			});
		} else {
			console.log("not signed in")
			loginStatus.innerText = 'Not signed in';
			buttons.innerHTML = `
		  <button class="btn btn-primary" id="signInButton">Sign In with Google</button>
		`;
			document.getElementById('signInButton').addEventListener('click', signIn);
		}
	}

	function signIn() {
		chrome.identity.getAuthToken({ interactive: true }, function (token) {
			if (chrome.runtime.lastError) {
				console.error(chrome.runtime.lastError);
				return;
			}
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
					userEmail = data.emailAddresses[0].value;
					chrome.storage.sync.set({ 'userEmail': userEmail });
					updateUI(true, userEmail);
				})
				.catch(error => {
					console.error('Error making request to People API:', error);
				});
		});

	}

	function signOut() {
		chrome.identity.getAuthToken({ interactive: false }, function (currentToken) {
			if (!chrome.runtime.lastError) {
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
				chrome.storage.sync.remove('userEmail');
				updateUI(false, null);
			} else {
				console.error(chrome.runtime.lastError);
			}
		});
	}

	chrome.storage.sync.get('userEmail', function (data) {
		const userEmail = data.userEmail;
		const isSignedIn = userEmail ? true : false;
		updateUI(isSignedIn, userEmail);
	});
});
