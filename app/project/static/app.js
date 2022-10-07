class Main {
  constructor() {
    this.postPath = window.location.pathname;

    $("#mods").on("click", "button", this.deleteMod.bind(this));
    $(".delete-pic").on("click", this.confirmDelete);
  }

  async deleteMod(e) {
    const index = $(e.target).data("index");
    const url = `${this.postPath}/delete-mod/${index}`;
    const res = await axiosCSRF.delete(url);

    if (res.status == 200) {
      $(e.target).parent().remove();
    } else {
      console.error("Error deleting mod. ", res.status);
    }
  }

  confirmDelete(e) {
    const btn = $(e.target);
    if (!btn.hasClass("btn-secondary")) {
      btn.addClass("btn-secondary");
      btn.html("Cancel");
      btn.next().removeClass("d-none");
    } else {
      btn.removeClass("btn-secondary");
      btn.html("Remove");
      btn.next().addClass("d-none");
    }
  }
}

function start() {
  const app = new Main();
  return app;
}
$(document).ready(start);
