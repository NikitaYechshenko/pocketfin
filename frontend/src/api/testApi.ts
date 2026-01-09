const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

function authHeaders() {
  const token = localStorage.getItem("gat_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

// ============ AUTH ============

export async function login(email: string, password: string) {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  const res = await fetch(`${BASE}/auth/jwt/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Login failed: ${res.status}`);
  }

  const data = await res.json();
  localStorage.setItem("gat_token", data.access_token);
  return data;
}

export async function register(email: string, password: string) {
  const res = await fetch(`${BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Registration failed: ${res.status}`);
  }

  return res.json();
}

export async function getCurrentUser() {
  const res = await fetch(`${BASE}/users/me`, { headers: { ...authHeaders() } });
  if (!res.ok) return null;
  return res.json();
}

export function logout() {
  localStorage.removeItem("gat_token");
}

export function isLoggedIn() {
  return !!localStorage.getItem("gat_token");
}

// ============ PORTFOLIOS ============

export async function getPortfolios() {
  const res = await fetch(`${BASE}/portfolios`, { headers: { ...authHeaders() } });
  if (res.status === 401) throw new Error('Unauthorized')
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  return res.json();
}

export async function createPortfolio(name: string) {
  const res = await fetch(`${BASE}/portfolios`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ name }),
  });
  if (res.status === 401) throw new Error('Unauthorized')
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  return res.json();
}

export async function getPortfolioWithAssets(id: number) {
  const res = await fetch(`${BASE}/portfolios/${id}/with-assets`, { headers: { ...authHeaders() } });
  if (res.status === 401) throw new Error('Unauthorized')
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  return res.json();
}

export async function createAsset(payload: any) {
  const res = await fetch(`${BASE}/assets`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(payload),
  });
  if (res.status === 401) throw new Error('Unauthorized')
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  return res.json();
}

export async function deleteAsset(id: number) {
  const res = await fetch(`${BASE}/assets/${id}`, { method: "DELETE", headers: { ...authHeaders() } });
  if (res.status === 401) throw new Error('Unauthorized')
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  return res;
}
