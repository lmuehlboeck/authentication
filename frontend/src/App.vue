<template>
  <RouterView />
</template>

<script>

export default {
  name: 'LayoutDefault'
}
</script>

<style>
@font-face {
  font-family: "Montserrat";
  src: local("Montserrat"),   url(../public/fonts/Montserrat-Regular.ttf) format("truetype");
}

@font-face {
  font-family: "Montserrat bold";
  src: local("Montserrat bold"),   url(../public/fonts/Montserrat-SemiBold.ttf) format("truetype");
}

* {
  font-family: "Montserrat";
}

html {
  background-color: #F8F8F8;
  overflow-x: hidden;
}

.bold {
  font-family: "Montserrat bold";
}

h1, h2, h3s {
  margin-top: 0 !important;
  line-height: normal !important;
}
h1 {
  font-size: 2rem !important;
  padding: 5px 0;
  border-bottom: 2px solid var(--q-primary);
}
h2 {
  font-size: 1.5rem !important;
}
h3 {
  font-size: 1.125rem !important;
}
h4 {
  font-size: 1rem !important;
  margin: 0 !important;
  padding: 0 !important;
  font-family: "Montserrat bold";
}
</style>