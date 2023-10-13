// const BASE_URL = 'http://localhost:5000';
const BASE_URL = 'https://resumegen.onrender.com';

function downloadPdf(userEmail) {
	const progress = document.getElementById('progress');
	const progressBar = document.getElementById('progress-bar');
	console.log(document.getElementById('toggleSwitch').checked);

	progress.style.display = '';
	progressBar.style.width = '10%';
	jobDescription = null;
	chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
		console.log("tabs", tabs)
		chrome.tabs.sendMessage(tabs[0].id, { action: "getJobDescription" }, function (response) {
			console.log("Got response from content script:", response)
			if(!response){
				alert("Please select text before using the buttons.");
				progress.style.display = 'None';
				return;
			}
			progressBar.style.width = '10%';
			console.log("Job Description:", jobDescription);

			console.log("Job Description:", jobDescription);
			console.log("User Email:", userEmail);
			const formData = new FormData();
			formData.append('job_description', jobDescription);
			formData.append('email', userEmail);
			formData.append('highlight', document.getElementById('toggleSwitch').checked);
			progressBar.style.width = '50%';
			fetch(`${BASE_URL}/generate_rankedpdf`, {
				method: 'POST',
				body: formData
			})
				.then((response) => response.blob())
				.then((blob) => {
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
	const loginStatus = document.getElementById('loginStatus');
	const buttons = document.getElementById('buttons');
	const profileOptions = document.getElementById('profile_options');

	if (isSignedIn) {
		console.log("signed in")
		// loginStatus.innerText = `Signed in as: ${userEmail}`;
		profileOptions.innerHTML = `<button id="profilePageButton" class="mdl-button mdl-js-button mdl-button--icon mdl-button--colored" style="color: black; height: 40px; width: 40px;">
										<i class="material-icons" style="font-size: 45px; left: 20%;">account_circle</i>
									</button>`;
		buttons.innerHTML = `
		<div class="row">
			<div class="col">
				<div class="form-check form-switch">
					<label class="form-check-label" for="toggleSwitch">Highlight keywords</label>
					<input class="form-check-input" type="checkbox" id="toggleSwitch" style="font-size: 20px">
				</div>
			</div>
			<div class="col align-items-center">
				<button id="downloadButton" class="mdl-button mdl-js-button mdl-button--icon mdl-button--colored" style="color: green; height: 100px; width: 100px;">
					<i class="material-icons" style="font-size: 110px; left: 7%;">download_for_offline</i>
				</button>
			</div>
		</div>

            <div id="progress" class="progress mt-3" style="display: None;">
				<div class="progress-bar progress-bar-striped progress-bar-animated" id="progress-bar" style="width: 0;"></div>
			</div>
        `;
		// document.getElementById('signOutButton').addEventListener('click', signOut);
		document.getElementById('downloadButton').addEventListener('click', function () {
			ans = downloadPdf(userEmail);

		});
		// document.getElementById('viewProfileButton').addEventListener('click', function () {
		// 	chrome.tabs.create({ url: `${BASE_URL}/profile` });
		// });
		document.getElementById('profilePageButton').addEventListener('click', function () {
            window.location.href = 'profile.html'; // this will change the popup view to page2.html
        });


	} else {
		console.log("not signed in")
		loginStatus.innerText = 'Not signed in';
		buttons.innerHTML = `
		<button class="btn btn-primary" id="signInButton">Sign In with Google</button>
		<button class="btn btn-secondary" id="signUpButton">Sign Up</button>
	`;
		document.getElementById('signInButton').addEventListener('click', signIn);
		document.getElementById('signUpButton').addEventListener('click', signUp);
	}
}



function signUp() {
	chrome.tabs.create({ url: `${BASE_URL}/newuser` });
}


function signIn() {
	signOut();
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
	chrome.storage.sync.remove('userEmail');
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
			// chrome.storage.sync.remove('userEmail');
			updateUI(false, null);
		} else {
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


