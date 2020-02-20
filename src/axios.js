// axios
import axios from "axios";

const domain = "https://rest-bot-dev.herokuapp.com/vendor/";

export default axios.create({
  baseURL: domain
  // You can add your headers here
});
