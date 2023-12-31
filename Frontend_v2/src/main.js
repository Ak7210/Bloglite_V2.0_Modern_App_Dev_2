import "bootstrap/dist/css/bootstrap.css";
import 'bootstrap/dist/css/bootstrap.min.css';

import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import * as bootstrap from "bootstrap";
import vueApexcharts from "vue3-apexcharts";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(bootstrap);
app.use(vueApexcharts)
app.mount("#app");

import 'bootstrap/dist/js/bootstrap.js';
import 'bootstrap/dist/js/bootstrap.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css';

