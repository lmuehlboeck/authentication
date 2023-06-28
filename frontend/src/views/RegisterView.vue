<template>
    <main class="q-my-lg">
        <div class="q-pa-md">
            <div class="bg-white shadow-4 rounded-borders q-mx-auto q-pa-lg" style="max-width: 500px">
                <q-form @submit="onSubmit">
                    <q-btn-group class="q-mb-xl" style="height: 40px" spread>
                        <q-btn color="white" text-color="black" label="Login" icon="login" to="/login" no-wrap />
                        <q-btn color="primary" label="Registrieren" icon="person_add" no-wrap />
                    </q-btn-group>
                    <q-input filled lazy-rules v-model="username" label="Benutzername" class="q-my-sm" hint="Maximal 30 Zeichen" ref="username"
                        :rules="[
                            val => val && val.length > 0 || 'Bitte etwas eingeben',
                            val => val.length <= 30 || 'Maximal 30 Zeichen erlaubt'
                        ]" />
                    <q-input filled lazy-rules type="password" v-model="password" label="Passwort" class="q-my-sm" hint="Mindestens 6 Zeichen"
                        :rules="[
                            val => val && val.length > 0 || 'Bitte etwas eingeben',
                            val => val.length >= 6 || 'Mindestens 6 Zeichen gefordert'
                        ]" />
                    <q-input filled lazy-rules type="password" v-model="password_confirm" label="Passwort bestätigen" class="q-my-sm"
                        :rules="[
                            val => val && val.length > 0 || 'Bitte etwas eingeben',
                            val => val === password || 'Passwort stimmt nicht überein'
                        ]" />
                    <div class="q-mt-lg row">
                        <q-btn type="submit" color="primary" label="Registrieren" class="full-width" :loading="loading" />
                    </div>
                </q-form>
            </div>
        </div>
    </main>
</template>

<script>
import { useToast } from "vue-toastification";

export default {
    name: 'RegisterView',
    inject: ['$globals'],

    methods: {
        onSubmit() {
            this.loading = true
            this.$globals.fetch('/user', "POST", {
                username: this.username,
                password: this.password
            }).then(response => {
                this.loading = false
                if(response.ok) {
                    this.$router.push('/register/success')
                } else if(response.status == 409) {
                    this.$refs.username.focus()
                    throw "Der Benutzername ist bereits vergeben"
                } else {
                    throw "Etwas ist schiefgelaufen"
                }
            }).catch(err => {
                this.loading = false
                useToast().error(err.toString())
            })
        }
    },

    data() {
        return {
            username: '',
            password: '',
            password_confirm: '',
            loading: false
        }
    }
}
</script>

<style>

</style>