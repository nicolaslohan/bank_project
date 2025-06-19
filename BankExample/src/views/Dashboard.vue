<template>
  <v-container>
    <h1>Bem-vindo(a)!</h1>
    <v-btn color="error" @click="logout">Sair</v-btn>
  </v-container>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Dados do Usuário</v-card-title>
          <v-card-text>
            <p><strong>Usuário:</strong> {{ username }}</p>
            <p><strong>Perfil:</strong> {{ profile }}</p>
            <p><strong>Banco:</strong> {{ bank }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" lg="12" md="6">
        <v-card>
          <v-card-title>Ações</v-card-title>
          <v-card-text>
            <p>Você pode gerenciar seus dados e realizar outras ações aqui.</p>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="router.push('/usuarios')">Gerenciar Usuários</v-btn>
            <v-btn color="primary" @click="router.push('/manageBanks')">Gerenciar Bancos</v-btn>
            <v-btn color="primary" @click="router.push('/perfis')">Gerenciar Perfis</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();

const username = ref();
const profile = ref();
const bank = ref();

onMounted(() => {
  fetchUserData();
})

async function fetchUserData() {
  try {
    const response = await fetch('http://localhost:5000/api/me', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
    });
    if (!response.ok) {
      throw new Error('Erro ao buscar dados do usuário');
    }
    const data = await response.json();
    username.value = data.username;
    profile.value = data.profile;
    bank.value = data.bank;
  } catch (error) {
    console.error(error);
  }
}

function logout() {
  localStorage.removeItem('access_token');
  router.push('/login');
}
</script>
