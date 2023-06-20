<template>
    <main class="q-my-lg">
        <div class="q-pa-md">
            <div class="bg-white shadow-4 rounded-borders q-mx-auto q-pa-lg" style="max-width: 500px">
                <div class="q-mb-lg row justify-center">
                    <img style="width: 150px; height: 150px;" ref="gif" />
                </div>
                <h4 class="text-center">Der Benutzer wurde erfolgreich angelegt!</h4>
                <div class="q-mt-lg row justify-center">
                    <q-btn outline color="primary" label="Zum Login" to="/login" />
                </div>
            </div>
        </div>
    </main>
</template> 

<script>
export default {
    name: 'RegisterSuccessView',
    mounted() {
        this.$refs.gif.src = '/img/success.gif'
    }
}
</script>

<style>

</style>