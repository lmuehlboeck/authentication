<template>
    <main class="q-my-lg">
        <div class="q-pa-md">
            <div class="bg-white shadow-4 rounded-borders q-mx-auto q-pa-lg" style="max-width: 500px">
                <q-form @submit="onSubmit">
                    <q-btn-group class="q-mb-xl" style="height: 40px" spread>
                        <q-btn color="primary" label="Login" icon="login" />
                        <q-btn color="white" text-color="black" label="Registrieren" icon="person_add" to="/register" />
                    </q-btn-group>
                    <q-input filled v-model="username" label="Benutzername" class="q-my-sm"/>
                    <q-input filled type="password" v-model="password" label="Passwort" class="q-my-sm"/>
                    <div class="q-mt-lg row">
                        <q-btn type="submit" color="primary" label="Anmelden" class="full-width" />
                    </div>
                </q-form>
            </div>
        </div>
    </main>
</template>

<script>
import { useToast } from "vue-toastification";

export default {
    name: 'LoginView',
    inject: ['$globals'],

    methods: {
        onSubmit() {
            if(this.username.length > 0 && this.password.length > 0) {
                this.$globals.fetch('/session', "POST", {
                    username: this.username,
                    password: this.password
                }).then(response => {
                    if(response.ok) {
                        return response.json()
                    } else if(response.status == 401) {
                        this.password = ""
                        throw "Ungültige Anmeldedaten"
                    } else {
                        throw "Etwas ist schiefgelaufen"
                    }
                }).then(data => {
                    localStorage.setItem("access_token", data.access_token)
                    this.$router.push("/")
                }).catch(err => {
                    useToast().error(err.toString())
                })
            } else {
                useToast().error("Füllen Sie jedes Feld aus")
            }
        }
    },

    data() {
        return {
            username: '',
            password: ''
        }
    }
}
</script>

<style>

</style>