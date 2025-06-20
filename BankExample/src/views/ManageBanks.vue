<template>
    <v-container>
        <v-btn color="secondary" @click="$router.back()" class="mb-4">
            Voltar
        </v-btn>
        <h1>Gerenciar Bancos</h1>
        <v-btn color="primary" @click="showForm = !showForm">
            {{ showForm ? 'Cancelar' : 'Adicionar Banco' }}
        </v-btn>
        <v-form v-if="showForm" @submit.prevent="handleSubmit" class="my-4">
            <v-text-field
            v-model="form.name"
            label="Nome do Banco"
            required
            ></v-text-field>
            <v-btn type="submit" color="success" :loading="loading">
            Salvar
            </v-btn>
        </v-form>
        <v-alert v-if="error" type="error" class="my-2">{{ error }}</v-alert>
        <v-alert v-if="success" type="success" class="my-2">{{ success }}</v-alert>
        <v-table>
            <thead>
                <tr>
                    <th>Nome do Banco</th>
                    <th>Criado em</th>
                    <th>Status</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="bank in banks" :key="bank.id">
                    <td>{{ bank.name }}</td>
                    <td>{{ bank.created_at }}</td>
                    <td>{{ bank.status }}</td>
                    <td>
                        <v-btn color="primary" @click="editBank(bank.id)">Editar</v-btn>
                        <v-btn color="error" @click="deleteBank(bank.id)">Excluir</v-btn>
                    </td>
                </tr>
            </tbody>
        </v-table>
    </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const banks = ref([]);

const form = ref({
    name: '',
});

const showForm = ref(false);
const loading = ref(false);
const error = ref(null);
const success = ref(null);

onMounted(() => {
    fetchBanks();
});

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

    try {
        const response = await fetch('http://localhost:5000/banks/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
            body: JSON.stringify(form.value),
        });

        if (!response.ok) {
            throw new Error('Erro ao cadastrar banco');
        }

        success.value = 'Banco cadastrado com sucesso!';
        form.value.name = '';
    } catch (err) {
        error.value = err.message;
    } finally {
        loading.value = false;
    }
}
</script>
