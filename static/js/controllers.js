var mailbox = angular.module('snailMail', []);

mailbox.controller('mailbox', function ($scope) {
	$http.get('/api/mail')
    .success(function(data) {
      $scope.letters = data;
    });
});


function openLetter(letter) {
	document.getElementById('letter-from').innerText = letter.sender;
	document.getElementById('letter-date').innerText = letter.date;
	document.getElementById('letter-message').value = letter.message;
	document.getElementById('letter').style.display = 'block';
	document.getElementById('letter').style.boxShadow = 'block';
}
function closeLetter() {
	document.getElementById('letter').style.display = 'none';
}

function sendMail() {
	data = {}
	data.message = document.getElementById('letter-message').value;
	data.to = document.getElementById('compose-to');
	data.subject = document.getElementById('compose-subject');
	$http.post('/api/send', data).
        success(function(data) {
            alert('Your message should arrive in 1-6 business days')
        });
	}