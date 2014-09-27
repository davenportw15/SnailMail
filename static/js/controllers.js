var mailbox = angular.module('snailMail', []);

mailbox.controller('mailbox', function ($scope) {
	$http.get('/api/mail')
    .success(function(data) {
      $scope.letters = data;
    });
});


function openLetter(id) {
	$http.get('/api/message/'+ id).
        success(function(data) {
            document.getElementById('letter-from').innerText = data[0].from;
			document.getElementById('letter-date').innerText = data[0].date;
			document.getElementById('letter-message').value = data[0].message;
        });
	}

function sendMail() {
	data = {}
	data.message = document.getElementById('letter-message').value;
	data.to = document.getElementById('compose-to');
	data.subject = document.getElementById('compose-subject');
	$http.post('/api/send', data).
        success(function(data) {
            alert('the deed is done')
        });
	}