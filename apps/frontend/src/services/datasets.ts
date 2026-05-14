"""Dataset API service - Handle all dataset API calls."""
interface Dataset {
  id: string
  name: string
  source: string
  description: string
  status: 'active' | 'archived' | 'processing'
}

interface DatasetCreate {
  name: string
  source: string
  description?: string
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const API_ENDPOINT = `${API_BASE_URL}/api/datasets`

export async function fetchDatasets(): Promise<Dataset[]> {
  const response = await fetch(API_ENDPOINT)
  if (!response.ok) throw new Error('Failed to fetch datasets')
  return response.json()
}

export async function fetchDataset(id: string): Promise<Dataset> {
  const response = await fetch(`${API_ENDPOINT}/${id}`)
  if (!response.ok) throw new Error('Dataset not found')
  return response.json()
}

export async function createDataset(data: DatasetCreate): Promise<Dataset> {
  const response = await fetch(API_ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  if (!response.ok) throw new Error('Failed to create dataset')
  return response.json()
}

export async function updateDataset(id: string, data: DatasetCreate): Promise<Dataset> {
  const response = await fetch(`${API_ENDPOINT}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  if (!response.ok) throw new Error('Failed to update dataset')
  return response.json()
}

export async function deleteDataset(id: string): Promise<void> {
  const response = await fetch(`${API_ENDPOINT}/${id}`, {
    method: 'DELETE'
  })
  if (!response.ok) throw new Error('Failed to delete dataset')
}

export type { Dataset, DatasetCreate }
