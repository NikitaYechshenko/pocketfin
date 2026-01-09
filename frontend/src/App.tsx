import { useState, useEffect } from 'react'
import './App.css'
import TestHarness from './pages/TestHarness'
import AuthPage from './pages/AuthPage'
import { isLoggedIn, logout, getCurrentUser } from './api/testApi'

function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  async function checkAuth() {
    if (isLoggedIn()) {
      try {
        const user = await getCurrentUser();
        if (user) {
          setAuthenticated(true);
          setUserEmail(user.email);
        } else {
          logout();
        }
      } catch {
        logout();
      }
    }
    setChecking(false);
  }

  function handleAuth() {
    checkAuth();
  }

  function handleLogout() {
    logout();
    setAuthenticated(false);
    setUserEmail(null);
  }

  if (checking) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
        <p style={{ color: 'var(--text-muted)' }}>Loading...</p>
      </div>
    );
  }

  if (!authenticated) {
    return <AuthPage onAuth={handleAuth} />;
  }

  return (
    <>
      <header className="app-header">
        <div className="app-logo" />
        <h1 className="app-title">Asset Tracker</h1>
        <div className="app-user">
          <span className="app-email">{userEmail}</span>
          <button className="small" onClick={handleLogout}>Sign Out</button>
        </div>
      </header>
      <TestHarness />
    </>
  )
}

export default App
