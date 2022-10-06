class Main {
  constructor() {
    this.postPath = window.location.pathname;

    $("#mods").on("click", "button", this.deleteMod.bind(this));
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
}

function start() {
  const app = new Main();
  return app;
}
$(document).ready(start);
