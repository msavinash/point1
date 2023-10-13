const BASE_URL = 'https://resumegen.onrender.com';
// const BASE_URL = 'http://localhost:5000';


document.getElementById('viewProfileButton').addEventListener('click', function () {
    chrome.tabs.create({ url: `${BASE_URL}/profile` });
});

document.getElementById('signOutButton').addEventListener('click', function () {
    // Add your sign-out functionality here
    signOut();
});

document.getElementById('backButton').addEventListener('click', function () {
    console.log('back')
    window.location.href = 'popup.html';
});




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
    window.location.href = 'popup.html';
}