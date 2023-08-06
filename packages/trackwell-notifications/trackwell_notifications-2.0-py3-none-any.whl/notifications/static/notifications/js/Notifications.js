function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function NotificationClient() {
  this.cookieName = 'notifications';
  this.request = null;
  this.options = {};
  this.modalContainer = null;
  this.overlay = null;
  this.notification = null;
}

NotificationClient.prototype = {
  checkCookie: function () {
    var value = '; ' + document.cookie;
    var parts = value.split('; ' + this.cookieName + '=');
    if (parts.length === 2) {
      return parts.pop()
        .split(';')
        .shift()
        .replaceAll('"', '');
    }
  },
  showModal: function (notification) {
    var that = this;

    notification = JSON.parse(notification);
    if (!notification) return;
    this.notification = notification;

    var modalContainer = document.createElement('div');
    if (notification === null || notification === undefined || notification.notification === undefined) {
      // Malformed response, out of synch cache or the like
      return;
    }

    modalContainer.className = 'notification notification-' + notification.notification.look;

    if (notification.notification.look === 'RELEASE_NOTES') {
      var isActive = false;

      var iconButton = document.createElement('button');
      iconButton.className = 'notification-RELEASE_NOTES-button';

      var bellIcon = document.createElement('i');
      bellIcon.className = 'notifications-font-bell';
      bellIcon.style.cssText = "font-size: 16px; color: #ff4a3f;";

      iconButton.appendChild(bellIcon);
      iconButton.onclick = function () {
        if (isActive) {
          this.modalContainer = document.body.removeChild(modalContainer);
          this.iconButton = document.body.removeChild(iconButton);
          that.dismissNotification(true, 'OK');
        } else {
          this.modalContainer = document.body.appendChild(modalContainer);
        }
        isActive = !isActive;
      }

      var titleContainer = document.createElement('div');
      titleContainer.className = 'titleContainer';

      var exitButton = document.createElement('button');
      exitButton.onclick = function () {
        this.modalContainer = document.body.removeChild(modalContainer);
        this.iconButton = document.body.removeChild(iconButton);
        that.dismissNotification(true, 'OK');
        isActive = !isActive;
      };
      exitIcon = document.createElement('i');
      exitIcon.className = 'notifications-font-times';
      exitIcon.style.cssText = "font-size: 24px; color: #636363;";
      exitButton.appendChild(exitIcon);

      var title = document.createElement('h1');
      title.innerHTML = notification.notification.name;
      titleContainer.appendChild(exitButton);
      titleContainer.appendChild(title);
      modalContainer.appendChild(titleContainer);


      var body = document.createElement('div');
      body.className = 'notification-body';
      body.innerHTML = notification.notification.message;
      modalContainer.appendChild(body);

      var overlay = document.createElement('div');
      overlay.className = 'notification-overlay';

      this.iconButton = document.body.appendChild(iconButton);


    } else {
      if (notification.notification.look === 'SIMPLE_OK') {
        var titleContainer = document.createElement('div');
        titleContainer.className = 'titleContainer';

        var exitButton = document.createElement('button');
        exitButton.onclick = function () {
          that.dismissNotification(true, 'OK');
        };
        exitIcon = document.createElement('i');
        exitIcon.className = 'notifications-font-times';
        exitIcon.style.cssText = "font-size: 24px; color: #636363;";
        exitButton.appendChild(exitIcon);

        var title = document.createElement('h1');
        title.innerHTML = notification.notification.name;
        titleContainer.appendChild(exitButton);
        titleContainer.appendChild(title);
        modalContainer.appendChild(titleContainer);
  
      }

      if (notification.notification.image !== null) {
        var imageContainer = document.createElement('img');
        imageContainer.src = notification.notification.image;
        imageContainer.alt = 'Notification image';
        imageContainer.className = 'notification-image';
        modalContainer.appendChild(imageContainer);
      }

      var body = document.createElement('div');
      body.className = 'notification-body';
      body.innerHTML = notification.notification.message;
      modalContainer.appendChild(body);

      var overlay = document.createElement('div');
      overlay.className = 'notification-overlay';


      if (notification.notification.look === 'SIMPLE_OK') {
        var buttonContainer = document.createElement('div');
        buttonContainer.className = 'notification-form-buttons';
        modalContainer.appendChild(buttonContainer);

        var approveButton = document.createElement('button');
        approveButton.innerHTML = gettext('OK');
        approveButton.onclick = function () {
          that.dismissNotification(true, 'OK');
        };
        buttonContainer.appendChild(approveButton);
      }

      if (notification.notification.look === 'SIGN_COMPANY') {
        var formContainer = document.createElement('div');
        formContainer.className = 'notification-form';
        modalContainer.appendChild(formContainer);

        var buttonContainer = document.createElement('div');
        buttonContainer.className = 'notification-form-buttons';
        modalContainer.appendChild(buttonContainer);

        var inputField = document.createElement('input');
        inputField.placeholder = gettext('Company name ');
        var snoozeButton = document.createElement('button');
        snoozeButton.innerHTML = gettext('Not now');
        var approveButton = document.createElement('button');
        approveButton.innerHTML = gettext('Approve');

        snoozeButton.onclick = function () {
          that.dismissNotification(false, inputField.value);
        };
        approveButton.onclick = function () {
          that.dismissNotification(true, inputField.value);
        };
        formContainer.appendChild(inputField);
        formContainer.appendChild(buttonContainer);
        buttonContainer.appendChild(snoozeButton);
        buttonContainer.appendChild(approveButton);
      }
      this.modalContainer = document.body.appendChild(modalContainer);
      this.overlay = document.body.appendChild(overlay);

      if (document.body.offsetWidth < 600) {
        modalContainer.style.left = '0';
      } else {
        modalContainer.style.marginLeft = -this.modalContainer.offsetWidth / 2 + 'px';
      }
    }

  },
  setupRequest: function (onSuccess) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
      if (request.readyState === 4) {
        if (request.status === 200) {
          onSuccess(request);
        } else {
          console.log('An error occurred during your request: ' + request.status + ' ' + request.statusText);
        }
      }
    };
    return request;
  },
  dismissNotification: function (answer, answer_string) {
    var that = this;
    var request = this.setupRequest(function (request) {
      that.modalContainer.parentNode.removeChild(that.modalContainer);
      that.overlay.parentNode.removeChild(that.overlay);
      that.modalContainer = null;
      that.overlay = null;
    });
    request.open('PATCH', '/api2/usernotifications/' + this.notification.id + '/');
    request.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    request.send(JSON.stringify({
      answer: answer,
      answer_string: answer_string
    }));
  },
  checkAndShow: function () {
    var that = this;
    var cookieStatus = this.checkCookie();
    this.cookie = cookieStatus;
    if (cookieStatus) {
      var firstNotification = cookieStatus.split('-')[0];
      var notificationId = firstNotification.split(':')[0];
      var next_show = new Date(parseFloat(cookieStatus.split('-')[0].split(':')[1]));
      var now = new Date();
      if (next_show < now) {
        var request = this.setupRequest(function (request) {
          that.showModal(request.responseText);
        });
        request.open('GET', '/api2/usernotifications/' + notificationId);
        request.send();
      }
    }
  }
};

function ready(callbackFunc) {
  if (document.readyState !== 'loading') {
    // Document is already ready, call the callback directly
    callbackFunc();
  } else if (document.addEventListener) {
    // All modern browsers to register DOMContentLoaded
    document.addEventListener('DOMContentLoaded', callbackFunc);
  } else {
    // Old IE browsers
    document.attachEvent('onreadystatechange', function () {
      if (document.readyState === 'complete') {
        callbackFunc();
      }
    });
  }
}

ready(function () {
  var nc = new NotificationClient();
  nc.typeInName = true;
  nc.checkAndShow();
});
