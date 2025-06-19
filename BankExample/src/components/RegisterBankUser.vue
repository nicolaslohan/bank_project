<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-card elevation="2">
          <v-card-title>Cadastrar Administrador</v-card-title>
          <v-card-text>
            <v-alert v-if="error" type="error" dense>{{ error }}</v-alert>
            <v-alert v-if="success" type="success" dense>{{ success }}</v-alert>

            <v-form @submit.prevent="handleRegister">
              <v-text-field
                v-model="form.username"
                label="Nome de usuário"
                required
              />
              <v-text-field
                v-model="form.password"
                label="Senha"
                type="password"
                required
              />

              <v-select
                v-model="form.bank_id"
                :items="banks"
                item-title="name"
                item-value="id"
                label="Banco"
                required
              ></v-select>

              <v-select
                v-model="form.profile_id"
                :items="profiles"
                item-title="title"
                item-value="id"
                label="Perfil"
                required
              />

              <v-btn type="submit" color="primary" :loading="loading" block>
                Cadastrar
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const form = ref({
  username: '',
  password: '',
  bank_id: null,
  profile_id: null,
});

const profiles = ref([]);
const banks = ref([]);
const loading = ref(false);
const error = ref(null);
const success = ref(null);

onMounted(() => {
  fetchRoles();
  fetchBanks();
});

async function fetchRoles() {
  try {
    const token = localStorage.getItem('access_token');
    const response = await axios.get('http://localhost:5000/user_profiles/all', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    profiles.value = response.data;
  } catch (err) {
    error.value = 'Erro ao carregar perfis.';
  }
}

async function fetchBanks() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost:5000/banks/all', {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        console.log(response.data);
        banks.value = response.data;
    } catch (err) {
        error.value = 'Erro ao carregar bancos.';
    }
}

async function handleRegister() {
  loading.value = true;
  error.value = null;
  success.value = null;

  try {
    const token = localStorage.getItem('access_token');

    const response = await axios.post(
      'http://localhost:5000/register/user',
      form.value,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    success.value = 'Administrador cadastrado com sucesso!';
    form.value = { username: '', password: '', bank_id: null, profile_id: null };
  } catch (err) {
    console.error('Erro ao cadastrar:', err);
    error.value = err.response?.data?.message || 'Erro ao cadastrar.';
  } finally {
    loading.value = false;
  }
}
</script>
