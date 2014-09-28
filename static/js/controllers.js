var mailbox = angular.module('snailMail', []);

mailbox.controller('mailbox', function ($scope, $http) {
	
  $http.get('/api/mail')
    .success(function(data) {
      console.log(data.mail);
      $scope.letters = data.mail;
    });

  $scope.sendEmail = function() {
    console.log("Test1")
    data = {};
    console.log("TEST");
    data.content = document.getElementById('composeArea').value;
    data.recipient = document.getElementById('composeTo').value;
    data.subject = document.getElementById('composeSubject').value;
    $http.post('/api/send', data).
          success(function(data) {
              alert('Your message should arrive in 1-6 business days');
              document.getElementById('composeArea').value = "";
              document.getElementById('composeTo').value = "";
              document.getElementById('composeSubject').value = ""; 
          });
    };

  $scope.openLetter = function(letter_obj) {
    document.getElementById('letter-from').innerText = letter_obj.sender;
    document.getElementById('letter-date').innerText = letter_obj.date_sent;
    document.getElementById('letter-message').innerText = letter_obj.content;
    document.getElementById('letter-wrapper').style.display = 'block';
  };

});

function closeLetter() {
	document.getElementById('letter-wrapper').style.display = 'none';
}