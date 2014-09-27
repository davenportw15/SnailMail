var mailbox = angular.module('snailMail', []);

mailbox.controller('mailbox', function ($scope) {
	$http.get('/api/mail').
        success(function(data) {
            $scope.letters = data;
        });
	}
});


function openLetter(id) {
	$http.get('/api/message/'+ id).
        success(function(data) {
            document.getElementById('letter-from').innerText = data[0].from;
			document.getElementById('letter-date').innerText = data[0].date;
			document.getElementById('letter-message').innerText = data[0].message;
        });
	}
	document.getElementById('letter-from').innerText = '';
	document.getElementById('letter-date').innerText = '';
	document.getElementById('letter-message').innerText = '';
}