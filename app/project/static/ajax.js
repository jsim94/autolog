const MODS = $("#mods");

class Main {
  constructor() {
    this.postPath = window.location.pathname;

    MODS.on("click", "button", this.deleteMod.bind(this));
  }

  async deleteMod(e) {
    const index = $(e.target).data("index");
    const url = `${this.postPath}/delete-mod/${index}`;

    const res = await axios.delete(url);
    console.log($(e.target).parent());
    if (res.status == 200) {
      $(e.target).parent().remove();
    }
  }
}

function start() {
  const app = new Main();
  return app;
}
$(document).ready(start);
