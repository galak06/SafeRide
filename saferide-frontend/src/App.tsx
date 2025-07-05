import React from 'react'
import './App.css'
import Login from './components/Login'
import AdminPortal from './components/AdminPortal'
import { useAuth } from './hooks/useAuth'

const App: React.FC = () => {
  const { isAuthenticated, login, logout, isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    // Pass login function to Login component
    return <Login onLogin={login} />;
  }

  // Pass logout function to AdminPortal
  return <AdminPortal onLogout={logout} />;
}

export default App 