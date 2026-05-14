<template>
  <div class="dataset-table">
    <table v-if="datasets.length > 0" class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Source</th>
          <th>Description</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="dataset in datasets" :key="dataset.id" class="table-row">
          <td class="cell-id">
            <code>{{ dataset.id }}</code>
          </td>
          <td class="cell-name">{{ dataset.name }}</td>
          <td class="cell-source">
            <code>{{ dataset.source }}</code>
          </td>
          <td class="cell-description">
            {{ dataset.description || '-' }}
          </td>
          <td class="cell-status">
            <span :class="`badge badge-${dataset.status}`">
              {{ dataset.status }}
            </span>
          </td>
          <td class="cell-actions">
            <button
              class="btn btn-sm btn-edit"
              @click="$emit('edit', dataset)"
              title="Edit dataset"
            >
              ✎ Edit
            </button>
            <button
              class="btn btn-sm btn-delete"
              @click="confirmDelete(dataset)"
              title="Delete dataset"
            >
              🗑 Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-else class="empty-state">
      <p>{{ emptyMessage }}</p>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="deleteConfirm.show" class="modal-overlay" @click="cancelDelete">
      <div class="modal" @click.stop>
        <h3>Confirm Delete</h3>
        <p>
          Are you sure you want to delete "{{ deleteConfirm.dataset?.name }}"?
        </p>
        <div class="modal-actions">
          <button class="btn btn-secondary" @click="cancelDelete">Cancel</button>
          <button class="btn btn-danger" @click="performDelete">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Dataset {
  id: string
  name: string
  source: string
  description: string
  status: 'active' | 'archived' | 'processing'
}

interface Props {
  datasets: Dataset[]
  emptyMessage?: string
}

interface Emits {
  (e: 'delete', datasetId: string): void
  (e: 'edit', dataset: Dataset): void
}

defineProps<Props>()
const emit = defineEmits<Emits>()

const deleteConfirm = ref({
  show: false,
  dataset: null as Dataset | null
})

function confirmDelete(dataset: Dataset) {
  deleteConfirm.value = {
    show: true,
    dataset
  }
}

function cancelDelete() {
  deleteConfirm.value = {
    show: false,
    dataset: null
  }
}

function performDelete() {
  if (deleteConfirm.value.dataset) {
    emit('delete', deleteConfirm.value.dataset.id)
  }
  cancelDelete()
}
</script>

<style scoped>
.dataset-table {
  width: 100%;
}

.table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.table thead {
  background: #f8f9fa;
  border-bottom: 2px solid #dee2e6;
}

.table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
}

.table-row {
  border-bottom: 1px solid #dee2e6;
  transition: background 0.2s;
}

.table-row:hover {
  background: #f8f9fa;
}

.table td {
  padding: 1rem;
  color: #555;
}

.cell-id,
.cell-source {
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
}

code {
  background: #f5f5f5;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
  white-space: nowrap;
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

.cell-actions {
  white-space: nowrap;
}

.btn {
  padding: 0.4rem 0.8rem;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
  border-radius: 4px;
  font-size: 0.85rem;
  transition: all 0.2s;
}

.btn-sm {
  margin-right: 0.5rem;
}

.btn-edit {
  border-color: #0066cc;
  color: #0066cc;
}

.btn-edit:hover {
  background: #e6f0ff;
}

.btn-delete {
  border-color: #dc3545;
  color: #dc3545;
}

.btn-delete:hover {
  background: #ffe6e6;
}

.empty-state {
  background: white;
  padding: 3rem 2rem;
  border-radius: 8px;
  text-align: center;
  color: #666;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 90%;
}

.modal h3 {
  margin-top: 0;
  color: #2c3e50;
}

.modal p {
  color: #666;
  line-height: 1.6;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.btn-secondary {
  background: #f5f5f5;
  border-color: #ddd;
  color: #333;
}

.btn-secondary:hover {
  background: #e9e9e9;
}

.btn-danger {
  background: #dc3545;
  border-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background: #c82333;
}
</style>
