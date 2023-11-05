// const BASE_URL = 'http://localhost:5000';
// const BASE_URL = 'https://resumegen.onrender.com';
// const BASE_URL = "https://tailorestest-xk3tn7p6ea-wl.a.run.app";
const BASE_URL = "https://app.tailores.live"


function startScan() {
	chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
		chrome.tabs.sendMessage(tabs[0].id, { action: "startScanning" }, function (response) {
			console.log("Got response from content script:", response)
		})
	}
	)
};



function stopScan() {
	chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
		chrome.tabs.sendMessage(tabs[0].id, { action: "stopScanning" }, function (response) {
			console.log("Got response from content script:", response)
		})
	}
	)
};




function downloadPdf(userEmail) {
	const progress = document.getElementById('progress');
	const progressBar = document.getElementById('progress-bar');

	progress.style.display = '';
	progressBar.style.width = '10%';
	jobDescription = null;
	chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
		console.log("tabs", tabs)
		chrome.tabs.sendMessage(tabs[0].id, { action: "getJobDescription" }, function (response) {
			console.log("Got response from content script:", response)
			if (!response) {
				alert("Please select the job description text before  generating the resume");
				progress.style.display = 'None';
				return;
			}
			startScan();
			jobDescription = response.jobDescription;
			progressBar.style.width = '10%';
			console.log("Job Description:", jobDescription);

			console.log("Job Description:", jobDescription);
			console.log("User Email:", userEmail);
			const formData = new FormData();
			formData.append('job_description', jobDescription);
			formData.append('email', userEmail);
			formData.append('highlight', document.getElementById('highlightKeywordSwitch').checked);
			formData.append('onepage', document.getElementById('singlePageSwitch').checked);
			// get main tab link
			tabUrl = tabs[0].url;
			formData.append('source', tabUrl);
			progressBar.style.width = '50%';
			fetch(`${BASE_URL}/generate_rankedpdf`, {
				method: 'POST',
				body: formData
			})
				.then((response) => response.blob())
				.then((blob) => {
					stopScan();
					progressBar.style.width = '70%';
					const filename = 'resume.pdf';
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
							setTimeout(() => { progress.style.display = 'None'; }, 1000)
							console.log("done");
						});
					};
					reader.readAsArrayBuffer(blob);
					progressBar.style.width = '0%';

				})
				.catch((error) => {
					console.error('Failed to generate PDF:', error);
				});
		})
	});
}


function updateUI(isSignedIn, userEmail) {
	const extensionBody = document.getElementById('extensionBody');
	const topRight = document.getElementById('topRight');
	if (isSignedIn) {
		topRight.innerHTML = `<button id="closeButton" class="mdl-button mdl-js-button mdl-button--icon">
		<i class="material-icons">close</i>
		</button>`
		console.log("signed in")
		extensionBody.innerHTML = `
		<div class="tab-content my-3" id="myTabContent">
			<div class="tab-pane fade show active" id="home" role="tabpanel" aria-labelledby="home-tab">
				<div class="row">
					<div class="col-8">
						<div style="margin-top: 20px">
							<div class="row">
								<div class="form-check form-switch">
									<div class="row">
										<div class="col-10">
											<label class="form-check-label" for="highlightKeywordSwitch">Highlight Keywords</label>
										</div>
										<div class="col-2">
											<input class="form-check-input" type="checkbox" id="highlightKeywordSwitch" style="font-size: 20px">
										</div>
									</div>
								</div>
							</div>
							<div class="row">
								<div class="form-check form-switch">
									<div class="row">
										<div class="col-10">
											<label class="form-check-label" for="singlePageSwitch">Single Page</label>
										</div>
										<div class="col-2">
											<input class="form-check-input" type="checkbox" id="singlePageSwitch" style="font-size: 20px">
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="col-4 align-items-center">
						<button id="downloadButton" class="mdl-button mdl-js-button mdl-button--icon mdl-button--colored" style="color: black; height: 100px; width: 100px;">
						<i class="material-icons" style="font-size: 110px; left: 7%;">download_for_offline</i>
						</button>
					</div>
				</div>
				<div id="progress" class="progress mt-3" style="display: None;">
					<div class="progress-bar progress-bar-striped progress-bar-animated" id="progress-bar" style="width: 0%;"></div>
				</div>
			</div>
			<div class="tab-pane fade" id="info" role="tabpanel" aria-labelledby="info-tab">Info</div>
			<div class="tab-pane fade" id="settings" role="tabpanel" style="width: 80%; margin: auto">
				<div class="row mt-3">
					<button class="mdl-button mdl-js-button mdl-js-ripple-effect settings-options" id="viewProfileButton">View Profile</button>
				</div>
				<div class="row mt-3">
					<button class="mdl-button mdl-js-button mdl-button--raised mdl-button--colored settings-options" id="signOutButton">Sign Out</button>
				</div>
			</div>
		</div>
        `;

		extensionFooter = document.getElementById('extensionFooter');
		extensionFooter.innerHTML = `
		<ul class="nav nav-pills nav-fill my-3" id="myTab" role="tablist">
		<li class="nav-item" role="presentation">
			<button id="homeButton" class="mdl-button mdl-js-button mdl-button--fab nav-link active" data-bs-toggle="tab" data-bs-target="#home" type="button" role="tab" aria-controls="home" aria-selected="true">
			<i class="material-icons">home</i>
			</button>
		</li>
		<!-- <li class="nav-item" role="presentation">
			<button id="infoButton" class="mdl-button mdl-js-button mdl-button--fab nav-link " data-bs-toggle="tab" data-bs-target="#info" type="button" role="tab" aria-controls="home" aria-selected="true">
			<i class="material-icons">info</i>
			</button>
		</li> -->
		<li class="nav-item" role="presentation">
			<button id="settingsButton" class="mdl-button mdl-js-button mdl-button--fab nav-link " data-bs-toggle="tab" data-bs-target="#settings" type="button" role="tab" aria-controls="home" aria-selected="true">
			<i class="material-icons">settings</i>
			</button>
		</li>
	</ul>
	`
		document.getElementById('signOutButton').addEventListener('click', signOut);
		document.getElementById('downloadButton').addEventListener('click', function () {
			ans = downloadPdf(userEmail);

		});
		// document.getElementById('viewProfileButton').addEventListener('click', function () {
		// 	chrome.tabs.create({ url: `${BASE_URL}/profile` });
		// });
		// document.getElementById('settingsButton').addEventListener('click', function () {
		// 	window.location.href = 'profile.html'; // this will change the popup view to page2.html
		// });
		document.getElementById('viewProfileButton').addEventListener('click', function () {
			chrome.tabs.create({ url: `${BASE_URL}/profile` });
		});

		// document.getElementById('signOutButton').addEventListener('click', function () {
		// 	// Add your sign-out functionality here
		// 	signOut();
		// });

		// document.getElementById('backButton').addEventListener('click', function () {
		// 	console.log('back')
		// 	window.location.href = 'popup.html';
		// });


		document.getElementById('closeButton').addEventListener('click', function () {
			window.close();
		});


	} else {

		console.log("not signed in")
		topRight.innerHTML = `
		<button class="gsi-material-button" id="signInButton">
		<div class="gsi-material-button-state"></div>
		<div class="gsi-material-button-content-wrapper">
		  <div class="gsi-material-button-icon">
			<svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" xmlns:xlink="http://www.w3.org/1999/xlink" style="display: block;">
			  <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"></path>
			  <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"></path>
			  <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"></path>
			  <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"></path>
			  <path fill="none" d="M0 0h48v48H0z"></path>
			</svg>
		  </div>
		  <span class="gsi-material-button-contents">Sign in with Google</span>
		  <span style="display: none;">Sign in with Google</span>
		</div>
	  </button>
	  	<div class="spinner-border text-primary" role="status" id="signinLoader">
			<span class="visually-hidden"></span>
		</div>
	`;
		const extensionBody = document.getElementById('extensionBody');
		extensionBody.innerHTML = `
		<div class="extension-body m-4">
			<div class="row">
				<h6>
				Say goodbye one-size-fits-all resumes. <br> Start using TailoRes for free starting now! 
				</h6>
			</div>
		</div>
	`
	const extensionFooter = document.getElementById('extensionFooter');
	extensionFooter.innerHTML = `
	<div class="row mt-3">
	<button class="mdl-button mdl-js-button mdl-button--raised mdl-button--colored" id="signUpButton">Sign Up</button>
</div>
	`;
		document.getElementById('signInButton').addEventListener('click', signIn);
		document.getElementById('signUpButton').addEventListener('click', signUp);
		$("#signinLoader").hide();
	}
}



function signUp() {
	chrome.tabs.create({ url: `${BASE_URL}/newuser` });
}


function signIn() {
	// signOut();
	$("#signInButton").hide();
	$("#signinLoader").show();
	// console.log("signing in");
	// signOut();
	chrome.identity.getAuthToken({ interactive: true }, function (token) {
		console.log("token", token)
		fetch('https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses', {
			headers: {
				'Authorization': 'Bearer ' + token,
			},
		})
			.then(response => {
				// console.log("got response")
				if (!response.ok) {
					throw new Error('Network response was not ok');
				}
				return response.json();
			})
			.then(data => {
				console.log("got data")
				console.log(data);
				userEmail = data.emailAddresses[0].value;
				checkMyUserExists(userEmail).then((userExists) => {
					if (userExists) {
						chrome.storage.sync.set({ 'userEmail': userEmail });
						updateUI(true, userEmail);
					}
					else {
						signUp();
					}
				});
			})
			.catch(error => {
				console.error('Error making request to People API:', error);
			});
	});

}

function signOut() {
	// chrome.storage.sync.remove('userEmail');
	chrome.identity.getAuthToken({ interactive: false }, function (currentToken) {
		if (!chrome.runtime.lastError) {
			fetch('https://accounts.google.com/o/oauth2/revoke?token=' + currentToken, {
				method: 'post',
				mode: 'cors',
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
				},
			}).then(function (response) {
				chrome.identity.removeCachedAuthToken({ token: currentToken }, function () {
					console.log('Token removed from cache.');
				});
				chrome.storage.sync.remove('userEmail');
				if (response.status === 200) {
					console.log('Token revoked successfully.');
				} else {
					console.log('Error revoking token:', response.statusText);
				}
				location.reload();
			});

		} else {
			alert(chrome.runtime.lastError.message)
			console.error(chrome.runtime.lastError);
		}
	});
}


function checkMyUserExists(userEmail) {
	console.log("checking if user exists");
	const url = `${BASE_URL}/checkmyuserexists?email=${userEmail}`;
	return fetch(url)
		.then((response) => response.text())
		.then((data) => {
			console.log(data);
			if (data == "false") {
				console.log("user does not exist");
				return false;
			} else {
				console.log("user exists");
				return true;
			}
		})
		.catch((error) => {
			console.error('Error:', error);
			throw error;
		});
}


document.addEventListener('DOMContentLoaded', function () {
	chrome.storage.sync.get('userEmail', function (data) {
		const userEmail = data.userEmail;
		const isSignedIn = userEmail ? true : false;
		updateUI(isSignedIn, userEmail);
	});
});









































