<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Bank Auth App</v-toolbar-title>
      <v-spacer></v-spacer>
      <div v-if="isAuthenticated">
        <v-btn text @click="logout">Sair</v-btn>
      </div>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

const isAuthenticated = computed(() => {
  return !!localStorage.getItem('access_token');
});

function logout() {
  localStorage.removeItem('access_token');
  router.push('/login');
}
</script>

<style>
html,
body,
#app {
  height: 100%;
  margin: 0;
}
</style>
