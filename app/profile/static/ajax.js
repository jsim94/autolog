function uploadPicture() {
  changeProfilePicture.processQueue();
}

function start() {
  $("#submit-picture").on("click", uploadPicture);
}

$(document).ready(start);
