<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card elevation="4">
          <v-card-title>Login</v-card-title>
          <v-card-text>
            <v-alert v-if="error" type="error" dense>{{ error }}</v-alert>
            <v-form @submit.prevent="handleLogin">
              <v-text-field v-model="form.username" label="Usuário" />
              <v-text-field v-model="form.password" label="Senha" type="password" />
              <v-btn type="submit" color="primary" :loading="loading" block>
                Entrar
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const form = ref({ username: '', password: '', scope: 'profile' });
const loading = ref(false);
const error = ref(null);

async function handleLogin() {
  loading.value = true;
  error.value = null;

  try {
    const response = await axios.post(
      'http://localhost:5000/oauth/token',
      new URLSearchParams({
        grant_type: 'password',
        username: form.value.username,
        password: form.value.password,
        scope: form.value.scope,
      }),
      {
        auth: {
          username: 'client-app',
          password: 'client-secret',
        },
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    );

    const token = response.data.access_token;
    localStorage.setItem('access_token', token);
    router.push('/');
  } catch (err) {
    console.error('Erro ao autenticar:', err);
    error.value = err.response?.data?.error_description || 'Erro ao autenticar.';
  } finally {
    loading.value = false;
  }
}
</script>
