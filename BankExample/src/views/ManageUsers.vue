<template>
    
    <v-container>
        <v-btn color="secondary" @click="$router.back()" class="mb-4">
            Voltar
        </v-btn>
        <h1>Gerenciar Bancos</h1>
        <v-btn color="primary" @click="showForm = !showForm">
            {{ showForm ? 'Cancelar' : 'Adicionar Usuário' }}
        </v-btn>
        <v-form v-if="showForm" @submit.prevent="handleSubmit" class="my-4">
            <v-text-field
            v-model="form.username"
            label="Nome do Usuário"
            required
            ></v-text-field>
            <v-text-field
            v-model="form.password"
            label="Senha do Usuário"
            required
            ></v-text-field>
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
            ></v-select>
            <v-btn type="submit" color="success" :loading="loading">
            Salvar
            </v-btn>
        </v-form>
        <v-alert v-if="error" type="error" class="my-2">{{ error }}</v-alert>
        <v-alert v-if="success" type="success" class="my-2">{{ success }}</v-alert>
        <v-table>
            <thead>
                <tr>
                    <th>Nome de Usuário</th>
                    <th>Perfil</th>
                    <th>Banco</th>
                    <th>Criado em</th>
                    <th>Status</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody :loading="loading">
                <tr v-for="user in users" :key="user.id">
                    <td>{{ user.username }}</td>
                    <td>{{ user.profile.title }}</td>
                    <td>{{ user.bank.name }}</td>
                    <td>{{ user.created_at }}</td>
                    <td>{{ user.status }}</td>
                    <td>
                        <v-btn color="primary" @click="editUser(user.id)">Editar</v-btn>
                        <v-btn color="error" @click="deleteUser(user.id)">Excluir</v-btn>
                    </td>
                </tr>
            </tbody>
        </v-table>
    </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const banks = ref([]);
const profiles = ref([]);
const users = ref([]);

const form = ref({
  username: '',
  password: '',
  bank_id: null,
  profile_id: null,
});

const showForm = ref(false);
const loading = ref(false);
const error = ref(null);
const success = ref(null);

onMounted(() => {
    fetchBanks();
    fetchProfiles();
    fetchUsers();
});

async function fetchUsers() {
    try {
        const response = await fetch('http://localhost:5000/bank_users/all', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
        });
        if (!response.ok) {
            throw new Error('Erro ao buscar usuários');
        }
        const data = await response.json();
        console.log(data);
        users.value = data;
    } catch (err) {
        error.value = err.message;
    }
}

async function fetchProfiles() {
    try {
        const response = await fetch('http://localhost:5000/user_profiles/all', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
        });
        if (!response.ok) {
            throw new Error('Erro ao buscar perfis');
        }
        const data = await response.json();
        profiles.value = data;
    } catch (err) {
        error.value = err.message;
    }
}

async function fetchBanks() {
    try {
        const response = await fetch('http://localhost:5000/banks/all', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
        });
        if (!response.ok) {
            throw new Error('Erro ao buscar bancos');
        }
        const data = await response.json();
        banks.value = data;
    } catch (err) {
        error.value = err.message;
    }
}

async function handleSubmit() {
    loading.value = true;
    error.value = null;
    success.value = null;

    console.log('Enviando:', form.value);

    try {
        const response = await fetch('http://localhost:5000/bank_users/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
            body: JSON.stringify(form.value),
        });


        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData?.error || 'Erro ao cadastrar usuário');
        }

        success.value = 'Usuário cadastrado com sucesso!';
        form.value.name = '';
        await fetchUsers();
    } catch (err) {
        error.value = err.message;
    } finally {
        loading.value = false;
    }
}
</script>
