const app = require("./app");
const config = require("./config");

app.listen(config.port, () => {
  console.log(`Medical assistant server running at http://localhost:${config.port}`);
});
