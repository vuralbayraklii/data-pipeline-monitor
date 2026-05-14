<template>
  <div class="datasets-page">
    <div class="page-header">
      <div>
        <h1>Dataset Registry</h1>
        <p class="subtitle">Manage and monitor your datasets</p>
      </div>
      <button @click="refreshDatasets" class="btn btn-primary" :disabled="isLoading">
        <span v-if="!isLoading">🔄 Refresh</span>
        <span v-else>Loading...</span>
      </button>
    </div>

    <!-- Alert Messages -->
    <div v-if="successMessage" class="alert alert-success">
      ✅ {{ successMessage }}
      <button @click="successMessage = ''" class="close-btn">×</button>
    </div>

    <div v-if="error" class="alert alert-error">
      ❌ {{ error }}
      <button @click="error = ''" class="close-btn">×</button>
    </div>

    <!-- Create/Edit Form -->
    <div class="form-section">
      <h2>{{ editingId ? 'Edit Dataset' : 'Create New Dataset' }}</h2>
      
      <form @submit.prevent="handleSubmit" class="dataset-form">
        <div class="form-group">
          <label for="name">Dataset Name *</label>
          <input
            id="name"
            v-model="formData.name"
            type="text"
            placeholder="e.g., sales_data"
            required
            maxlength="255"
          />
        </div>

        <div class="form-group">
          <label for="source">Data Source *</label>
          <input
            id="source"
            v-model="formData.source"
            type="text"
            placeholder="e.g., s3://bucket/path"
            required
          />
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea
            id="description"
            v-model="formData.description"
            placeholder="Optional description"
            maxlength="1000"
            rows="3"
          ></textarea>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn btn-success" :disabled="isCreating">
            {{ editingId ? 'Update Dataset' : 'Create Dataset' }}
          </button>
          
          <button 
            v-if="editingId" 
            type="button" 
            @click="cancelEdit" 
            class="btn btn-secondary"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>

    <!-- Datasets Table -->
    <div class="table-section">
      <h2>Datasets ({{ datasets.length }})</h2>
      
      <div v-if="datasets.length === 0" class="empty-state">
        <p>No datasets found. Create one to get started!</p>
      </div>

      <DatasetTable
        v-else
        :datasets="datasets"
        @edit="handleEdit"
        @delete="handleDelete"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import DatasetTable from '../components/DatasetTable.vue'
import { 
  fetchDatasets, 
  createDataset, 
  updateDataset, 
  deleteDataset,
  type Dataset,
  type DatasetCreate 
} from '../services/datasets'

// State
const datasets = ref<Dataset[]>([])
const isLoading = ref(false)
const isCreating = ref(false)
const error = ref('')
const successMessage = ref('')
const editingId = ref<string | null>(null)

// Form data
const formData = ref<DatasetCreate>({
  name: '',
  source: '',
  description: ''
})

// Load datasets on mount
onMounted(async () => {
  await loadDatasets()
})

// Load datasets from API
async function loadDatasets() {
  isLoading.value = true
  error.value = ''
  try {
    datasets.value = await fetchDatasets()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load datasets'
  } finally {
    isLoading.value = false
  }
}

// Refresh datasets
async function refreshDatasets() {
  await loadDatasets()
}

// Handle form submission (create or update)
async function handleSubmit() {
  isCreating.value = true
  error.value = ''
  try {
    if (editingId.value) {
      // Update existing dataset
      await updateDataset(editingId.value, formData.value)
      successMessage.value = 'Dataset updated successfully!'
      editingId.value = null
    } else {
      // Create new dataset
      await createDataset(formData.value)
      successMessage.value = 'Dataset created successfully!'
    }
    
    // Reset form
    resetForm()
    
    // Reload datasets
    await loadDatasets()
    
    // Clear success message after 3 seconds
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to save dataset'
  } finally {
    isCreating.value = false
  }
}

// Handle edit action from table
async function handleEdit(dataset: Dataset) {
  editingId.value = dataset.id
  formData.value = {
    name: dataset.name,
    source: dataset.source,
    description: dataset.description
  }
  
  // Scroll to form
  const formSection = document.querySelector('.form-section')
  formSection?.scrollIntoView({ behavior: 'smooth' })
}

// Handle delete action from table
async function handleDelete(id: string) {
  if (!confirm('Are you sure you want to delete this dataset?')) {
    return
  }

  error.value = ''
  try {
    await deleteDataset(id)
    successMessage.value = 'Dataset deleted successfully!'
    await loadDatasets()
    
    // Clear success message after 3 seconds
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to delete dataset'
  }
}

// Cancel edit
function cancelEdit() {
  editingId.value = null
  resetForm()
}

// Reset form to initial state
function resetForm() {
  formData.value = {
    name: '',
    source: '',
    description: ''
  }
}
</script>

<style scoped>
.datasets-page {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.page-header h1 {
  margin: 0;
  color: #1a1a1a;
  font-size: 2rem;
}

.subtitle {
  margin: 0.5rem 0 0 0;
  color: #666;
  font-size: 0.95rem;
}

/* Alerts */
.alert {
  padding: 1rem;
  margin-bottom: 1.5rem;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  animation: slideIn 0.3s ease-in-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.alert-error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.close-btn:hover {
  opacity: 1;
}

/* Form Section */
.form-section {
  background: #f9f9f9;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  border: 1px solid #e0e0e0;
}

.form-section h2 {
  margin-top: 0;
  color: #1a1a1a;
}

.dataset-form {
  display: grid;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input,
.form-group textarea {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: inherit;
  font-size: 0.95rem;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #0066cc;
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

/* Buttons */
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #0066cc;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #0052a3;
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-success:hover:not(:disabled) {
  background-color: #218838;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #5a6268;
}

/* Table Section */
.table-section {
  background: #f9f9f9;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.table-section h2 {
  margin-top: 0;
  color: #1a1a1a;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
}

/* Responsive */
@media (max-width: 768px) {
  .datasets-page {
    padding: 1rem;
  }

  .page-header {
    flex-direction: column;
    gap: 1rem;
  }

  .page-header h1 {
    font-size: 1.5rem;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}
</style>
