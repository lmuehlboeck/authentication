<template>
    <main class="q-my-lg">
        <div class="q-pa-md">
            <div class="bg-white shadow-4 rounded-borders q-mx-auto q-pa-lg" style="max-width: 500px">
                <q-skeleton type="text" class="text-h1" v-if="loading" />
                <h1 v-if="!loading">Willkommen, {{ username }}!</h1>
                <q-skeleton type="text" class="text-h3" v-if="loading" />
                <h3 v-if="!loading">Herzliche Gratulation, Sie haben sich angemeldet!</h3>
                <q-skeleton type="text" class="text-h3" v-if="loading" />
                <h3 v-if="!loading">Berechtigungen: {{ role }}</h3>
                <div class="q-mt-lg row">
                    <q-btn @click="logout" label="Abmelden" class="full-width" />
                </div>
                <div class="q-mt-md row">
                    <q-btn @click="confirm = true" color="negative" icon="delete" label="Benutzer löschen" class="full-width" />
                </div>
            </div>
        </div>

        <q-dialog v-model="confirm">
            <q-card>
                <q-card-section class="row items-center no-wrap">
                    <q-avatar icon="warning" color="primary" text-color="white" />
                    <span class="q-ml-sm">Möchten Sie diesen Benutzer wirklich unwiderruflich löschen?</span>
                </q-card-section>

                <q-card-actions align="right">
                    <q-btn label="Abbrechen" color="primary" v-close-popup />
                    <q-btn flat @click="delete_user" label="Löschen" color="primary" v-close-popup />
                </q-card-actions>
            </q-card>
        </q-dialog>
    </main>
</template>

<script>
import { useToast } from "vue-toastification"

export default {
    name: 'UserView',
    inject: ['$globals'],

    created() {
        this.$globals.fetchAuthenticated("/user", "GET").then(response => {
            return response.json()
        }).then(data => {
            this.loading = false
            this.username = data.username
            this.role = this.roles[data.role]
        }).catch(err => {
            this.loading = false
            if(localStorage.getItem("access_token"))
                useToast().warning(err.toString())
            this.$router.push("/login")
        })
    },

    methods: {
        logout() {
            this.$globals.fetchAuthenticated("/session", "DELETE").then(() => {
                localStorage.clear()
                useToast().success("Sie wurden abgemeldet")
            }).catch(err => {
                useToast().warning(err.toString())
            })
            this.$router.push("/login")
        },
        delete_user() {
            this.$globals.fetchAuthenticated("/user", "DELETE").then(() => {
                localStorage.clear()
                useToast().success("Ihr Benutzer wurde gelöscht")
            }).catch(err => {
                useToast().warning(err.toString())
            })
            this.$router.push("/login")
        }
    },

    data() {
        return {
            username: "",
            roles: ["Standard", "Erhöht", "Administrator"],
            role: 0,
            confirm: false,
            loading: true
        }
    }
}
</script>

<style>

</style>