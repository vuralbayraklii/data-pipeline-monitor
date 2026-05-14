"""Datasets page component - Full CRUD operations."""
<template>
  <div class="datasets-page">
    <div class="page-header">
      <h2>Dataset Registry</h2>
      <button @click="refreshDatasets" class="btn btn-secondary" :disabled="isLoading">
        🔄 Refresh
      </button>
    </div>

    <div class="actions">
      <button @click="isCreating = !isCreating" class="btn btn-primary" :disabled="isLoading">
        {{ isCreating ? 'Cancel' : '+ New Dataset' }}
      </button>
    </div>

    <div v-if="isCreating" class="create-form">
      <h3>Create New Dataset</h3>
      <form @submit.prevent="createDataset">
        <div class="form-group">
          <label for="name">Name:</label>
          <input
            id="name"
            v-model="formData.name"
            type="text"
            placeholder="Dataset name"
            required
          />
        </div>

        <div class="form-group">
          <label for="source">Source:</label>
          <input
            id="source"
            v-model="formData.source"
            type="text"
            placeholder="s3://bucket/path"
            required
          />
        </div>

        <div class="form-group">
          <label for="description">Description:</label>
          <textarea
            id="description"
            v-model="formData.description"
            placeholder="Optional description"
            rows="3"
          ></textarea>
        </div>

        <button type="submit" class="btn btn-success" :disabled="isLoading">
          {{ isLoading ? 'Creating...' : 'Create Dataset' }}
        </button>
      </form>
    </div>

    <div v-if="error" class="alert alert-error">
      {{ error }}
    </div>

    <div v-if="isLoading" class="loading">
      Loading datasets...
    </div>

    <div v-else-if="datasets.length > 0" class="table-wrapper">
      <table class="datasets-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Source</th>
            <th>Description</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="dataset in datasets" :key="dataset.id">
            <td>{{ dataset.id }}</td>
            <td>{{ dataset.name }}</td>
            <td><code>{{ dataset.source }}</code></td>
            <td>{{ dataset.description || '-' }}</td>
            <td>
              <span :class="`badge badge-${dataset.status}`">
                {{ dataset.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="empty-state">
      <p>No datasets yet. Create your first dataset!</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Dataset {
  id: string
  name: string
  source: string
  description: string
  status: string
}

const datasets = ref<Dataset[]>([])
const isLoading = ref(false)
const isCreating = ref(false)
const error = ref<string | null>(null)

const formData = ref({
  name: '',
  source: '',
  description: ''
})

onMounted(async () => {
  await loadDatasets()
})

async function loadDatasets(): Promise<void> {
  isLoading.value = true
  error.value = null

  try {
    const response = await fetch('http://localhost:8000/api/datasets')
    if (!response.ok) throw new Error('Failed to load datasets')
    datasets.value = await response.json()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Unknown error'
  } finally {
    isLoading.value = false
  }
}

async function createDataset(): Promise<void> {
  isLoading.value = true
  error.value = null

  try {
    const response = await fetch('http://localhost:8000/api/datasets', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData.value)
    })

    if (!response.ok) throw new Error('Failed to create dataset')

    const newDataset = await response.json()
    datasets.value.push(newDataset)

    // Reset form
    formData.value = { name: '', source: '', description: '' }
    isCreating.value = false
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Unknown error'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.datasets-page {
  padding: 2rem 0;
}

h2 {
  color: #2c3e50;
  margin-bottom: 2rem;
}

.actions {
  margin-bottom: 2rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s;
}

.btn-primary {
  background: #0066cc;
  color: white;
}

.btn-primary:hover {
  background: #0052a3;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-success:hover:not(:disabled) {
  background: #218838;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.create-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2c3e50;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #0066cc;
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.alert {
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 2rem;
}

.alert-error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.table-wrapper {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: auto;
}

.datasets-table {
  width: 100%;
  border-collapse: collapse;
}

.datasets-table th {
  background: #f8f9fa;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #dee2e6;
}

.datasets-table td {
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
}

.datasets-table tbody tr:hover {
  background: #f8f9fa;
}

code {
  background: #f5f5f5;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-size: 0.9rem;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.badge-active {
  background: #d4edda;
  color: #155724;
}

.badge-archived {
  background: #e2e3e5;
  color: #383d41;
}

.badge-processing {
  background: #cfe2ff;
  color: #084298;
}

.empty-state {
  background: white;
  padding: 3rem 2rem;
  border-radius: 8px;
  text-align: center;
  color: #666;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
