const postPath = window.location.pathname;
const USER_INPUTS = $("#updates, #comments, #mods");

async function deleteMod(e) {
  const index = $(e.target).data("index");
  const url = `${postPath}/delete-mod/${index}`;
  const res = await axiosCSRF.delete(url);

  if (res.status == 200) {
    $(e.target).parent().remove();
  } else {
    console.error("Error deleting mod. ", res.status);
  }
}

function confirmDelete(e) {
  const btn = $(e.target);
  if (!btn.hasClass("btn-secondary")) {
    btn.addClass("btn-secondary").removeClass("btn-outline-secondary").html("Cancel").next().removeClass("d-none");
  } else {
    btn.removeClass("btn-secondary").addClass("btn-outline-secondary").html("Remove").next().addClass("d-none");
  }
}

function linkify() {
  // Turns plaintext links into anchor tags
  const regex = /(\b((https?:\/\/)|(www\.))[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gi;
  USER_INPUTS.each((i, element) => {
    $(element).html(function (i, html) {
      return html.replace(regex, function (link, i, i, http) {
        return `<a href="${!http ? "http://" : ""}${link}" rel="nofollow noreferrer">${link}</a>`;
      });
    });
  });
}

async function populateModal(e) {
  const type = $(e.relatedTarget).data("modal-type");
  const updateId = $(e.relatedTarget).data("update-id");
  const commentId = $(e.relatedTarget).data("comment-id");
  const modalContent = $("#modal .modal-content");

  const res = await axiosCSRF.get(`${postPath}/get-form`, {
    params: {
      form: type,
      updateId: updateId,
      commentId: commentId,
    },
  });
  modalContent.html(res.data);
}

function start() {
  linkify();

  $("#mods").on("click", "button", deleteMod);
  $(".delete-pic").on("click", confirmDelete);

  $("#addModModal").on("hidden.bs.modal", () => {
    location.reload();
  });

  $("#modal").on("show.bs.modal", populateModal);

  $("#deleteModal").on("show.bs.modal", (e) => {
    $(this).find("#confirm-delete").attr("href", $(e.relatedTarget).data("href"));
  });

  // initialize tooltips
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  const tooltipList = [...tooltipTriggerList].map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl));
}
$(document).ready(start);
