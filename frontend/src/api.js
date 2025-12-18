// src/api.js
// Centralized API utility for frontend-backend communication

const API_BASE = import.meta.env.VITE_API_BASE || 
  (import.meta.env.PROD ? '' : 'http://localhost:5000');

// File upload example
export async function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${API_BASE}/api/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) throw new Error('Upload failed');
  return res.json();
}

// Chat endpoint (updated to match backend)
export async function sendChatMessage(message) {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error('Chat failed');
  return res.json();
}

// Profile update (placeholder)
export async function updateProfile(profileData) {
  const res = await fetch(`${API_BASE}/api/profile`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(profileData),
  });
  if (!res.ok) throw new Error('Profile update failed');
  return res.json();
}

// Create chart from uploaded data
export async function createChart(chartData) {
  const res = await fetch(`${API_BASE}/api/charts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(chartData),
  });
  if (!res.ok) throw new Error('Chart creation failed');
  return res.json();
}

// Health check
export async function healthCheck() {
  const res = await fetch(`${API_BASE}/api/health`);
  if (!res.ok) throw new Error('Health check failed');
  return res.json();
}
