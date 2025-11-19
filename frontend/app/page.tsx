'use client';

import { useState } from 'react';
import { AuthProvider, useAuth } from '@/contexts/AuthContext';
import LoginForm from '@/components/LoginForm';
import TodoList from '@/components/TodoList';
import ChatWindow from '@/components/ChatWindow';
import { todosAPI } from '@/lib/api';

function TodoApp() {
  const { user, logout, loading } = useAuth();
  const [showLogin, setShowLogin] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [showChat, setShowChat] = useState(false);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [newTodoName, setNewTodoName] = useState('');
  const [newTodoDescription, setNewTodoDescription] = useState('');
  const [newTodoDueDate, setNewTodoDueDate] = useState('');

  const handleCreateTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Convert datetime-local format to ISO string, or undefined if empty
      const dueDate = newTodoDueDate && newTodoDueDate.trim() 
        ? new Date(newTodoDueDate).toISOString() 
        : undefined;
      
      await todosAPI.create({
        name: newTodoName,
        description: newTodoDescription || undefined,
        due_date: dueDate,
      });
      setShowCreateForm(false);
      setNewTodoName('');
      setNewTodoDescription('');
      setNewTodoDueDate('');
      // Trigger refresh of todo list
      setRefreshTrigger(prev => prev + 1);
    } catch (error) {
      console.error('Error creating todo:', error);
    }
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center text-dash-gray">Loading...</div>;
  }

  if (!user) {
    return (
      <>
        {showLogin && <LoginForm onClose={() => setShowLogin(false)} />}
        <div className="min-h-screen flex items-center justify-center px-6 py-12">
          <div className="glass-panel max-w-2xl w-full text-center px-8 py-16 md:px-12 md:py-20 relative overflow-hidden">
            {/* Decorative gradient orbs */}
            <div className="absolute top-0 left-1/4 w-32 h-32 bg-dash-green/10 rounded-full blur-3xl -z-10" />
            <div className="absolute bottom-0 right-1/4 w-40 h-40 bg-dash-orange/10 rounded-full blur-3xl -z-10" />
            
            <div className="relative z-10">
              <p className="uppercase tracking-[0.4em] text-xs text-dash-gray mb-6 font-medium">TwoHundredOk</p>
              <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 font-display leading-tight">
                Welcome to Todoer
              </h1>
              <p className="text-lg text-dash-gray mb-12 max-w-md mx-auto leading-relaxed">
                Log in to track your tasks. Stay organized, stay productive.
              </p>
              <button
                onClick={() => setShowLogin(true)}
                className="inline-flex items-center justify-center gap-2 bg-dash-green text-gray-900 font-bold px-8 py-4 rounded-full hover:bg-dash-green-strong transition-all transform hover:scale-105 shadow-lg shadow-dash-green/20 text-base"
              >
                Login or Register
              </button>
            </div>
          </div>
        </div>
      </>
    );
  }

  return (
    <div className="min-h-screen bg-charcoal-soft">
      <header className="bg-charcoal border-b border-white/5 shadow-card">
        <div className="max-w-7xl mx-auto px-4 py-4 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <h1 className="text-2xl font-semibold text-white font-display tracking-tight">Todoer</h1>
          <div className="flex flex-col gap-3 md:flex-row md:items-center md:gap-4">
            <input
              type="text"
              placeholder="Search todos..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="px-4 py-2 rounded-2xl bg-charcoal-muted border border-white/10 text-white placeholder:text-dash-gray focus:outline-none focus:ring-2 focus:ring-dash-green transition"
            />
            <span className="text-dash-gray text-sm md:text-base">Hello, {user.username}</span>
            <button
              onClick={logout}
              className="bg-dash-orange text-gray-900 px-4 py-2 rounded-2xl font-semibold hover:bg-dash-orange-soft transition"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-10 space-y-8">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.4em] text-dash-gray">Dashboard</p>
            <h2 className="text-3xl font-semibold text-white mt-1">My Todos</h2>
          </div>
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="self-start md:self-auto bg-dash-green text-gray-900 px-6 py-3 rounded-2xl font-semibold hover:bg-dash-green-strong transition"
          >
            {showCreateForm ? 'Cancel' : 'Create Todo'}
          </button>
        </div>

        {showCreateForm && (
          <form onSubmit={handleCreateTodo} className="glass-panel p-6 space-y-4">
            <div>
              <label className="block text-xs uppercase tracking-[0.3em] text-dash-gray mb-2">Name *</label>
              <input
                type="text"
                value={newTodoName}
                onChange={(e) => setNewTodoName(e.target.value)}
                className="w-full rounded-2xl bg-charcoal border border-white/10 px-4 py-3 text-white placeholder:text-dash-gray focus:outline-none focus:ring-2 focus:ring-dash-green"
                required
              />
            </div>
            <div>
              <label className="block text-xs uppercase tracking-[0.3em] text-dash-gray mb-2">Description</label>
              <textarea
                value={newTodoDescription}
                onChange={(e) => setNewTodoDescription(e.target.value)}
                className="w-full rounded-2xl bg-charcoal border border-white/10 px-4 py-3 text-white placeholder:text-dash-gray focus:outline-none focus:ring-2 focus:ring-dash-green"
                rows={3}
              />
            </div>
            <div>
              <label className="block text-xs uppercase tracking-[0.3em] text-dash-gray mb-2">
                Due Date <span className="text-[10px] text-dash-gray">(optional)</span>
              </label>
              <div className="flex flex-col gap-3 sm:flex-row">
                <input
                  type="date"
                  value={newTodoDueDate.split('T')[0] || ''}
                  onChange={(e) => {
                    const date = e.target.value;
                    const time = newTodoDueDate.includes('T') ? newTodoDueDate.split('T')[1] : '00:00';
                    setNewTodoDueDate(date ? `${date}T${time}` : '');
                  }}
                  className="flex-1 rounded-2xl bg-charcoal border border-white/10 px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-dash-green"
                />
                <input
                  type="time"
                  value={newTodoDueDate.includes('T') ? newTodoDueDate.split('T')[1] : ''}
                  onChange={(e) => {
                    const time = e.target.value;
                    const date = newTodoDueDate.split('T')[0] || '';
                    setNewTodoDueDate(date ? `${date}T${time}` : '');
                  }}
                  className="flex-1 rounded-2xl bg-charcoal border border-white/10 px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-dash-green disabled:opacity-40"
                  disabled={!newTodoDueDate.split('T')[0]}
                />
                {newTodoDueDate && (
                  <button
                    type="button"
                    onClick={() => setNewTodoDueDate('')}
                    className="rounded-2xl border border-white/10 px-4 py-3 text-sm text-dash-gray hover:text-white"
                  >
                    Clear
                  </button>
                )}
              </div>
            </div>
            <button
              type="submit"
              className="bg-dash-green text-gray-900 px-6 py-3 rounded-2xl font-semibold hover:bg-dash-green-strong transition"
            >
              Create
            </button>
          </form>
        )}

        <TodoList searchQuery={searchQuery} refreshTrigger={refreshTrigger} />
      </main>

      <button
        onClick={() => setShowChat(!showChat)}
        className="fixed bottom-6 right-6 bg-dash-green text-gray-900 w-14 h-14 rounded-3xl shadow-card hover:bg-dash-green-strong flex items-center justify-center text-2xl z-40"
      >
        💬
      </button>

      <ChatWindow isOpen={showChat} onClose={() => setShowChat(false)} />
    </div>
  );
}

export default function Home() {
  return (
    <AuthProvider>
      <TodoApp />
    </AuthProvider>
  );
}

