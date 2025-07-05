import React from 'react'
import './App.css'
import Login from './components/Login'
import AdminPortal from './components/AdminPortal'
import { useAuth } from './hooks/useAuth'

// Debug component to monitor authentication state
const AuthDebug: React.FC = () => {
  const token = localStorage.getItem('authToken');
  const timestamp = localStorage.getItem('authTimestamp');
  
  if (!token) return null;
  
  const tokenAge = timestamp ? Math.round((Date.now() - parseInt(timestamp)) / 1000 / 60) : 0;
  const isExpired = timestamp ? (Date.now() - parseInt(timestamp)) > (24 * 60 * 60 * 1000) : false;
  
  return (
    <div style={{
      position: 'fixed',
      top: '10px',
      right: '10px',
      background: isExpired ? '#ffebee' : '#e8f5e8',
      border: `2px solid ${isExpired ? '#f44336' : '#4caf50'}`,
      borderRadius: '8px',
      padding: '10px',
      fontSize: '12px',
      fontFamily: 'monospace',
      zIndex: 1000,
      maxWidth: '300px'
    }}>
      <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>
        🔐 Auth Debug
      </div>
      <div>Token: {token ? '✅ Found' : '❌ Missing'}</div>
      <div>Age: {tokenAge} min</div>
      <div>Status: {isExpired ? '⚠️ Expired' : '✅ Valid'}</div>
      <button 
        onClick={() => {
          localStorage.removeItem('authToken');
          localStorage.removeItem('authTimestamp');
          window.location.reload();
        }}
        style={{
          marginTop: '5px',
          padding: '2px 6px',
          fontSize: '10px',
          background: '#ff5722',
          color: 'white',
          border: 'none',
          borderRadius: '3px',
          cursor: 'pointer'
        }}
      >
        Clear Token
      </button>
    </div>
  );
};

const App: React.FC = () => {
  const { isAuthenticated, login, logout, isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <AuthDebug />
      {!isAuthenticated ? (
        <Login onLogin={login} />
      ) : (
        <AdminPortal onLogout={logout} />
      )}
    </>
  );
}

export default App 