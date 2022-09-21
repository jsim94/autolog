const BASE_API_URL = "https://www.carqueryapi.com/api/0.3/?callback=?";
const YEAR_FIELD = $("#year");
const MAKE_FIELD = $("#make");
const MODEL_FIELD = $("#model");
const TRIM_FIELD = $("#trim");
const MODEL_ID_FIELD = $("#model_id");
const HP_FIELD = $("#horsepower");
const TORQUE_FIELD = $("#torque");
const WEIGHT_FIELD = $("#weight");
const ENGINE_FIELD = $("#engine_size");
const DRIVETRAIN_FIELD = $("#drivetrain");

class CarQuery {
  constructor() {
    this.getYears();
    // this.makes = null;
    // this.models = null;
    // this.trims = null;

    this.year = null;
    this.make = null;
    this.model = null;
    this.model_obj = null;

    YEAR_FIELD.change(this.yearChange.bind(this));
    MAKE_FIELD.change(this.makeChange.bind(this));
    MODEL_FIELD.change(this.modelChange.bind(this));
    TRIM_FIELD.change(this.trimChange.bind(this));
  }

  trimChange() {
    this.model_obj = this.trims.find((val) => val.value == TRIM_FIELD.val());
    console.log(this.model_obj);
    MODEL_ID_FIELD.val(this.model_obj.model_id);
    HP_FIELD.val(parseInt(this.model_obj.model_engine_power_ps * 0.986));
    TORQUE_FIELD.val(parseInt(this.model_obj.model_engine_torque_nm * 0.73756));
    WEIGHT_FIELD.val(parseInt(this.model_obj.model_weight_kg));
    ENGINE_FIELD.val(Math.round(this.model_obj.model_engine_cc / 100) / 10);

    let drive = this.model_obj.model_drive.toLowerCase();

    if (drive.includes("front")) {
      drive = "1";
    } else if (drive.includes("rear")) {
      drive = "2";
    } else if (drive.includes("all") || drive.includes("4wd") || drive.includes("awd")) {
      drive = "3";
    }
    DRIVETRAIN_FIELD.val(drive);
  }

  async modelChange() {
    this.clearTrim();
    this.model = MODEL_FIELD.val();
    await this.getTrims();
    this.populateField(TRIM_FIELD, this.trims);
  }

  async makeChange() {
    this.clearModels();
    this.make = MAKE_FIELD.val();
    await this.getModels();
    this.populateField(MODEL_FIELD, this.models);
  }

  async yearChange() {
    this.clearMakes();
    this.year = YEAR_FIELD.val();
    await this.getMakes();
    this.populateField(MAKE_FIELD, this.makes);
  }

  async getYears() {
    const response = await this.callApi("getYears");
    const yearList = [];
    const minYear = parseInt(response.Years.min_year);
    const maxYear = parseInt(response.Years.max_year);

    for (let i = maxYear; i >= minYear; i--) {
      yearList.push({ value: i, display: i });
    }
    this.populateField(YEAR_FIELD, yearList);
    return yearList;
  }

  async getMakes() {
    const response = await this.callApi("getMakes", this.year);
    const makeList = [];

    for (let make of response.Makes) {
      if (make.make_is_common == 1) {
        makeList.push({ value: make.make_id, display: make.make_display });
      }
    }
    for (let make of response.Makes) {
      if (make.make_is_common == 0) {
        makeList.push({ value: make.make_id, display: make.make_display });
      }
    }
    this.makes = makeList;
  }

  async getModels() {
    const response = await this.callApi("getModels", this.year, this.make);
    const modelList = [];

    for (let model of response.Models) {
      modelList.push({ value: model.model_name, display: model.model_name });
    }
    this.models = modelList;
  }

  async getTrims() {
    const response = await this.callApi("getTrims", this.year, this.make, this.model);
    const trimList = [];

    for (trim of response.Trims) {
      trimList.push({ value: trim.model_id, display: trim.model_trim ? trim.model_trim : "Default", ...trim });
    }
    this.trims = trimList;
  }

  clearMakes() {
    this.clearModels();
    this.makes = null;
    MAKE_FIELD.empty();
  }

  clearModels() {
    this.clearTrim();
    this.models = null;
    MODEL_FIELD.empty();
  }

  clearTrim() {
    this.trim = null;
    TRIM_FIELD.empty();
  }

  async callApi(cmd, year, make, model) {
    return $.getJSON(BASE_API_URL, { cmd: cmd, year: year, make: make, model: model, sold_in_us: 1 }, (data) => {
      return data;
    });
  }

  populateField(field, options) {
    let optionList = '<option value=""></option>';
    for (let option of options) {
      optionList += `<option value="${option.value}">${option.display}</option>`;
    }
    field.append(optionList);
  }
}

function start() {
  const app = new CarQuery();
  return app;
}
$(document).ready(start);
