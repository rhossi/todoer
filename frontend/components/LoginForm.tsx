'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';

interface LoginFormProps {
  onClose?: () => void;
}

export default function LoginForm({ onClose }: LoginFormProps) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login, register, user } = useAuth();
  
  useEffect(() => {
    if (user && onClose) {
      onClose();
    }
  }, [user, onClose]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      if (isLogin) {
        await login(username, password);
      } else {
        await register(username, email, password);
      }
      // Close form on success
      setUsername('');
      setEmail('');
      setPassword('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred');
    }
  };

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 px-4">
      <div className="glass-panel w-full max-w-md p-8 rounded-3xl">
        <h2 className="text-3xl font-semibold mb-6">{isLogin ? 'Login' : 'Register'}</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm text-dash-gray uppercase tracking-[0.25em] mb-2">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-3 rounded-2xl bg-charcoal border border-white/10 text-white placeholder:text-dash-gray focus:outline-none focus:ring-2 focus:ring-dash-green"
              required
            />
          </div>
          {!isLogin && (
            <div className="mb-4">
              <label className="block text-sm text-dash-gray uppercase tracking-[0.25em] mb-2">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 rounded-2xl bg-charcoal border border-white/10 text-white placeholder:text-dash-gray focus:outline-none focus:ring-2 focus:ring-dash-green"
                required
              />
            </div>
          )}
          <div className="mb-4">
            <label className="block text-sm text-dash-gray uppercase tracking-[0.25em] mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 rounded-2xl bg-charcoal border border-white/10 text-white placeholder:text-dash-gray focus:outline-none focus:ring-2 focus:ring-dash-green"
              required
            />
          </div>
          {error && <div className="text-dash-orange mb-4">{error}</div>}
          <button
            type="submit"
            className="w-full bg-dash-green text-gray-900 py-3 rounded-2xl font-semibold hover:bg-dash-green-strong transition"
          >
            {isLogin ? 'Login' : 'Register'}
          </button>
        </form>
        <button
          onClick={() => setIsLogin(!isLogin)}
          className="mt-4 text-dash-green hover:text-white underline text-sm"
        >
          {isLogin ? 'Need an account? Register' : 'Already have an account? Login'}
        </button>
      </div>
    </div>
  );
}

