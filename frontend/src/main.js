import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { Quasar } from 'quasar'
import quasarUserOptions from './quasar-user-options'
import { globals } from './globals'
import Toast, { TYPE } from "vue-toastification";
import "vue-toastification/dist/index.css";


createApp(App)
    .provide('$globals', globals)
    .use(Quasar, quasarUserOptions)
    .use(Toast, { 
        transition: "Vue-Toastification__bounce",
        maxToasts: 20,
        newestOnTop: true,
        toastDefaults: {
            [TYPE.ERROR]: {
                timeout: 6000,
                showCloseButtonOnHover: true,
                hideProgressBar: true,
            },
            [TYPE.WARNING]: {
                timeout: 4500,
                showCloseButtonOnHover: true,
                hideProgressBar: true,
            },
            [TYPE.SUCCESS]: {
                timeout: 3000,
                showCloseButtonOnHover: true,
                hideProgressBar: true,
            }
        }
     })
    .use(router).mount('#app')
