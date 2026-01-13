'use client';

import React, { useEffect, useState } from 'react';
import styles from './page.module.css';

interface User {
  id: number;
  username: string;
  email: string;
  full_name: string | null;
}

// BFF API Routes를 통해 호출 (Next.js 내부 API)
const API_BASE_URL = '/api';

export default function Home() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newUser, setNewUser] = useState({
    username: '',
    email: '',
    full_name: ''
  });
  const [showForm, setShowForm] = useState(false);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/users`);
      if (!response.ok) {
        throw new Error('Failed to fetch users');
      }
      const data = await response.json();
      setUsers(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_BASE_URL}/users`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newUser),
      });

      if (!response.ok) {
        throw new Error('Failed to create user');
      }

      setNewUser({ username: '', email: '', full_name: '' });
      setShowForm(false);
      fetchUsers();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create user');
    }
  };

  const handleDeleteUser = async (userId: number) => {
    if (!window.confirm('Are you sure you want to delete this user?')) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Failed to delete user');
      }

      fetchUsers();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to delete user');
    }
  };

  if (loading) {
    return (
      <div className={styles.App}>
        <div className={styles.loading}>Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.App}>
        <div className={styles.error}>Error: {error}</div>
        <button onClick={fetchUsers}>Retry</button>
      </div>
    );
  }

  return (
    <div className={styles.App}>
      <header className={styles['App-header']}>
        <h1>FastExit - User Management</h1>
      </header>

      <main className={styles['App-main']}>
        <div className={styles.controls}>
          <button 
            className={`${styles.btn} ${styles['btn-primary']}`}
            onClick={() => setShowForm(!showForm)}
          >
            {showForm ? 'Cancel' : 'Add New User'}
          </button>
          <button className={`${styles.btn} ${styles['btn-secondary']}`} onClick={fetchUsers}>
            Refresh
          </button>
        </div>

        {showForm && (
          <form className={styles['user-form']} onSubmit={handleCreateUser}>
            <h2>Create New User</h2>
            <div className={styles['form-group']}>
              <label htmlFor="username">Username *</label>
              <input
                id="username"
                type="text"
                required
                value={newUser.username}
                onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
                placeholder="Enter username"
              />
            </div>
            <div className={styles['form-group']}>
              <label htmlFor="email">Email *</label>
              <input
                id="email"
                type="email"
                required
                value={newUser.email}
                onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                placeholder="Enter email"
              />
            </div>
            <div className={styles['form-group']}>
              <label htmlFor="full_name">Full Name</label>
              <input
                id="full_name"
                type="text"
                value={newUser.full_name}
                onChange={(e) => setNewUser({ ...newUser, full_name: e.target.value })}
                placeholder="Enter full name"
              />
            </div>
            <button type="submit" className={`${styles.btn} ${styles['btn-success']}`}>Create User</button>
          </form>
        )}

        <div className={styles['users-container']}>
          <h2>Users ({users.length})</h2>
          {users.length === 0 ? (
            <p className={styles['no-users']}>No users found</p>
          ) : (
            <div className={styles['users-grid']}>
              {users.map((user) => (
                <div key={user.id} className={styles['user-card']}>
                  <div className={styles['user-info']}>
                    <h3>{user.username}</h3>
                    <p className={styles['user-email']}>{user.email}</p>
                    {user.full_name && (
                      <p className={styles['user-full-name']}>{user.full_name}</p>
                    )}
                  </div>
                  <div className={styles['user-actions']}>
                    <button
                      className={`${styles.btn} ${styles['btn-danger']} ${styles['btn-sm']}`}
                      onClick={() => handleDeleteUser(user.id)}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
