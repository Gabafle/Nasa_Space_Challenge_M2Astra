<script setup lang="ts">
</script>

<template>
  <v-app-bar
    app
    elevation="2"
    class="header-bar"
  >
    <v-container fluid class="container-header">
      <!-- Section gauche : logo + titre -->
      <div class="d-flex align-center">
        <v-img
          src="@/assets/logo_app_head.png"
          class="logo"
          contain
        ></v-img>
        <v-app-bar-title class="title">AstroMetric</v-app-bar-title>
      </div>

      <!-- Section droite : boutons -->
      <div class="btn-container">
        <v-btn class="btn-menu" to="/">
          <v-icon class="icon-btn">mdi-home</v-icon>
          Home
        </v-btn>
        <v-btn class="btn-menu">
          <v-icon class="icon-btn">mdi-account
          </v-icon>
          Login
        </v-btn>
        <v-btn class="btn-menu" to="/FAQ/page_faq">
          <v-icon class="icon-btn">mdi-magnify</v-icon>
          FAQ
        </v-btn>

      </div>
    </v-container>
  </v-app-bar>
</template>

<style scoped>

.container-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #222222;
}

.header-bar {

  color: #fff;
  padding: 0; /* Supprime tout espacement interne */
  margin: 0; /* Supprime toute marge autour */
}

.logo {
  width: 48px;
  height: 48px;

}

.title {
  font-family: 'Poppins', sans-serif;
  font-weight: 600;
  font-size: 1.4rem;
  color: #cbffed;
}

.title :deep(.v-toolbar-title__placeholder) {
  overflow: visible;
}
.btn-container{
  display: flex;
  align-items: center;
  justify-content: space-around;
  width: 25%;
}
.btn-menu{
  background: transparent;
  color: #cbffed;
  transition: all 0.3s ease;
  background: transparent;

}

.icon-btn{
  margin-right: 7px;
}

</style>
