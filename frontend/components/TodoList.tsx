'use client';

import { useState, useEffect } from 'react';
import { todosAPI, Todo } from '@/lib/api';
import { format } from 'date-fns';

interface TodoListProps {
  searchQuery: string;
  refreshTrigger?: number;
}

export default function TodoList({ searchQuery, refreshTrigger }: TodoListProps) {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState<'name' | 'creation_date' | 'due_date'>('creation_date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [completedFilter, setCompletedFilter] = useState<'all' | 'true' | 'false'>('false');
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [editingTodoId, setEditingTodoId] = useState<number | null>(null);
  const [editName, setEditName] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [editDueDate, setEditDueDate] = useState('');

  useEffect(() => {
    loadTodos();
  }, [searchQuery, sortBy, sortOrder, completedFilter, page, pageSize, refreshTrigger]);

  const loadTodos = async () => {
    setLoading(true);
    try {
      const data = await todosAPI.list({
        search: searchQuery || undefined,
        sort_by: sortBy,
        sort_order: sortOrder,
        completed: completedFilter,
        page,
        page_size: pageSize,
      });
      setTodos(data.todos);
      setTotal(data.total);
      setTotalPages(data.total_pages);
      if (page > data.total_pages && data.total_pages > 0) {
        setPage(1);
      }
    } catch (error) {
      console.error('Error loading todos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleComplete = async (id: number) => {
    try {
      await todosAPI.toggleComplete(id);
      loadTodos();
    } catch (error) {
      console.error('Error toggling todo completion:', error);
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm('Are you sure you want to delete this todo?')) {
      try {
        await todosAPI.delete(id);
        loadTodos();
      } catch (error) {
        console.error('Error deleting todo:', error);
      }
    }
  };

  const handleDoubleClick = (todo: Todo) => {
    setEditingTodoId(todo.id);
    setEditName(todo.name);
    setEditDescription(todo.description || '');
    if (todo.due_date) {
      const date = new Date(todo.due_date);
      const dateStr = date.toISOString().split('T')[0];
      const timeStr = date.toTimeString().split(' ')[0].substring(0, 5);
      setEditDueDate(`${dateStr}T${timeStr}`);
    } else {
      setEditDueDate('');
    }
  };

  const handleSaveEdit = async (id: number) => {
    try {
      const dueDate = editDueDate && editDueDate.trim() ? new Date(editDueDate).toISOString() : undefined;

      await todosAPI.update(id, {
        name: editName,
        description: editDescription || undefined,
        due_date: dueDate,
      });
      setEditingTodoId(null);
      loadTodos();
    } catch (error) {
      console.error('Error updating todo:', error);
    }
  };

  const handleCancelEdit = () => {
    setEditingTodoId(null);
    setEditName('');
    setEditDescription('');
    setEditDueDate('');
  };

  if (loading) {
    return (
      <div className="text-center py-12 text-dash-gray">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-white/10 bg-charcoal-muted">
          <span className="w-2 h-2 rounded-full bg-dash-green animate-pulse" />
          Loading todos...
        </div>
      </div>
    );
  }

  const handlePageSizeChange = (newPageSize: number) => {
    setPageSize(newPageSize);
    setPage(1);
  };

  return (
    <div className="space-y-4">
      <div className="flex gap-4 items-center flex-wrap">
        <select
          value={completedFilter}
          onChange={(e) => {
            setCompletedFilter(e.target.value as 'all' | 'true' | 'false');
            setPage(1);
          }}
          className="px-4 py-2 text-sm font-medium text-white bg-charcoal-muted border border-white/10 rounded-full hover:border-dash-green focus:outline-none focus:ring-2 focus:ring-dash-green cursor-pointer"
        >
          <option value="false">Uncompleted</option>
          <option value="true">Completed</option>
          <option value="all">All</option>
        </select>
        <select
          value={sortBy}
          onChange={(e) => {
            setSortBy(e.target.value as any);
            setPage(1);
          }}
          className="px-4 py-2 text-sm font-medium text-white bg-charcoal-muted border border-white/10 rounded-full hover:border-dash-green focus:outline-none focus:ring-2 focus:ring-dash-green cursor-pointer"
        >
          <option value="name">Sort by Name</option>
          <option value="creation_date">Sort by Creation Date</option>
          <option value="due_date">Sort by Due Date</option>
        </select>
        <select
          value={sortOrder}
          onChange={(e) => {
            setSortOrder(e.target.value as any);
            setPage(1);
          }}
          className="px-4 py-2 text-sm font-medium text-white bg-charcoal-muted border border-white/10 rounded-full hover:border-dash-green focus:outline-none focus:ring-2 focus:ring-dash-green cursor-pointer"
        >
          <option value="asc">Ascending</option>
          <option value="desc">Descending</option>
        </select>
        <select
          value={pageSize}
          onChange={(e) => handlePageSizeChange(Number(e.target.value))}
          className="px-4 py-2 text-sm font-medium text-white bg-charcoal-muted border border-white/10 rounded-full hover:border-dash-green focus:outline-none focus:ring-2 focus:ring-dash-green cursor-pointer"
        >
          <option value="5">5 per page</option>
          <option value="10">10 per page</option>
          <option value="15">15 per page</option>
          <option value="30">30 per page</option>
        </select>
      </div>
      {todos.length === 0 ? (
        <div className="text-center py-8 text-dash-gray">No todos found</div>
      ) : (
        <div className="space-y-3">
          {todos.map((todo) => (
            <div
              key={todo.id}
              className={`rounded-3xl border border-white/5 bg-charcoal-muted p-6 transition hover:border-dash-green/60 ${
                todo.is_completed ? 'opacity-70' : ''
              }`}
            >
              {editingTodoId === todo.id ? (
                <div className="space-y-4">
                  <div>
                    <label className="block text-xs uppercase tracking-[0.3em] text-dash-gray mb-2">Name *</label>
                    <input
                      type="text"
                      value={editName}
                      onChange={(e) => setEditName(e.target.value)}
                      className="w-full px-4 py-3 rounded-2xl bg-charcoal border border-white/10 text-white focus:outline-none focus:ring-2 focus:ring-dash-green"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-xs uppercase tracking-[0.3em] text-dash-gray mb-2">Description</label>
                    <textarea
                      value={editDescription}
                      onChange={(e) => setEditDescription(e.target.value)}
                      className="w-full px-4 py-3 rounded-2xl bg-charcoal border border-white/10 text-white focus:outline-none focus:ring-2 focus:ring-dash-green"
                      rows={3}
                    />
                  </div>
                  <div>
                    <label className="block text-xs uppercase tracking-[0.3em] text-dash-gray mb-2">
                      Due Date <span className="text-dash-gray text-[10px]">(optional)</span>
                    </label>
                    <div className="flex gap-2 flex-col sm:flex-row">
                      <input
                        type="date"
                        value={editDueDate.split('T')[0] || ''}
                        onChange={(e) => {
                          const date = e.target.value;
                          const time = editDueDate.includes('T') ? editDueDate.split('T')[1] : '00:00';
                          setEditDueDate(date ? `${date}T${time}` : '');
                        }}
                        className="flex-1 px-4 py-3 rounded-2xl bg-charcoal border border-white/10 text-white focus:outline-none focus:ring-2 focus:ring-dash-green"
                      />
                      <input
                        type="time"
                        value={editDueDate.includes('T') ? editDueDate.split('T')[1] : ''}
                        onChange={(e) => {
                          const time = e.target.value;
                          const date = editDueDate.split('T')[0] || '';
                          setEditDueDate(date ? `${date}T${time}` : '');
                        }}
                        className="flex-1 px-4 py-3 rounded-2xl bg-charcoal border border-white/10 text-white focus:outline-none focus:ring-2 focus:ring-dash-green"
                        disabled={!editDueDate.split('T')[0]}
                      />
                      {editDueDate && (
                        <button
                          type="button"
                          onClick={() => setEditDueDate('')}
                          className="px-4 py-3 rounded-2xl border border-white/10 text-sm text-dash-gray hover:text-white"
                        >
                          Clear
                        </button>
                      )}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleSaveEdit(todo.id)}
                      className="flex-1 bg-dash-green text-gray-900 px-4 py-3 rounded-2xl font-semibold hover:bg-dash-green-strong"
                    >
                      Save
                    </button>
                    <button
                      onClick={handleCancelEdit}
                      className="flex-1 bg-charcoal border border-white/10 text-white px-4 py-3 rounded-2xl hover:border-white/30"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <div className="flex items-start gap-4">
                  <input
                    type="checkbox"
                    checked={todo.is_completed}
                    onChange={() => handleToggleComplete(todo.id)}
                    className="w-5 h-5 mt-1 cursor-pointer accent-dash-green"
                  />
                  <div
                    className="flex-1 cursor-pointer"
                    onDoubleClick={() => handleDoubleClick(todo)}
                    title="Double-click to edit"
                  >
                    <h3
                      className={`font-semibold text-lg ${
                        todo.is_completed ? 'line-through text-dash-gray' : 'text-white'
                      }`}
                    >
                      {todo.name}
                    </h3>
                    {todo.description && (
                      <p className={`text-dash-gray mt-1 ${todo.is_completed ? 'line-through' : ''}`}>
                        {todo.description}
                      </p>
                    )}
                    <div className="mt-3 flex flex-wrap gap-4 text-xs text-dash-gray uppercase tracking-[0.3em]">
                      <div>Created · {format(new Date(todo.creation_date), 'MMM dd, yyyy')}</div>
                      {todo.due_date && (
                        <div className={new Date(todo.due_date) < new Date() ? 'text-dash-orange' : ''}>
                          Due · {format(new Date(todo.due_date), 'MMM dd, yyyy')}
                        </div>
                      )}
                    </div>
                  </div>
                  <button
                    onClick={() => handleDelete(todo.id)}
                    className="ml-4 text-dash-orange hover:text-white px-3 py-1 rounded"
                  >
                    Delete
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {totalPages > 1 && (
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between mt-6 pt-4 border-t border-white/5">
          <div className="text-sm text-dash-gray">
            Showing {(page - 1) * pageSize + 1} to {Math.min(page * pageSize, total)} of {total} todos
          </div>
          <div className="flex gap-2 items-center">
            <button
              onClick={() => setPage(page - 1)}
              disabled={page === 1}
              className="px-4 py-2 border border-white/10 rounded-full disabled:opacity-50 disabled:cursor-not-allowed hover:border-white/40"
            >
              Previous
            </button>
            <div className="flex gap-1">
              {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                let pageNum;
                if (totalPages <= 5) {
                  pageNum = i + 1;
                } else if (page <= 3) {
                  pageNum = i + 1;
                } else if (page >= totalPages - 2) {
                  pageNum = totalPages - 4 + i;
                } else {
                  pageNum = page - 2 + i;
                }
                return (
                  <button
                    key={pageNum}
                    onClick={() => setPage(pageNum)}
                    className={`px-3 py-2 border rounded-md ${
                      page === pageNum
                        ? 'bg-dash-green text-gray-900 border-dash-green'
                        : 'border-white/10 hover:border-white/40'
                    }`}
                  >
                    {pageNum}
                  </button>
                );
              })}
            </div>
            <button
              onClick={() => setPage(page + 1)}
              disabled={page === totalPages}
              className="px-4 py-2 border border-white/10 rounded-full disabled:opacity-50 disabled:cursor-not-allowed hover:border-white/40"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
