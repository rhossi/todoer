import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface User {
  id: number;
  username: string;
  email: string;
  created_at: string;
}

export interface Todo {
  id: number;
  name: string;
  description?: string;
  creation_date: string;
  due_date?: string;
  created_by: number;
  is_completed: boolean;
  completed_at?: string;
}

export interface TodoCreate {
  name: string;
  description?: string;
  due_date?: string;
}

export interface TodoUpdate {
  name?: string;
  description?: string;
  due_date?: string;
}

export const authAPI = {
  register: async (username: string, email: string, password: string) => {
    const response = await api.post('/api/auth/register', {
      username,
      email,
      password,
    });
    return response.data;
  },

  login: async (username: string, password: string) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    const response = await api.post('/api/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/api/auth/me');
    return response.data;
  },
};

export interface TodoListResponse {
  todos: Todo[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export const todosAPI = {
  list: async (params?: {
    search?: string;
    sort_by?: string;
    sort_order?: string;
    completed?: string; // 'all', 'true', 'false'
    page?: number;
    page_size?: number;
  }): Promise<TodoListResponse> => {
    const response = await api.get('/api/todos', { params });
    return response.data;
  },

  get: async (id: number): Promise<Todo> => {
    const response = await api.get(`/api/todos/${id}`);
    return response.data;
  },

  create: async (todo: TodoCreate): Promise<Todo> => {
    const response = await api.post('/api/todos', todo);
    return response.data;
  },

  update: async (id: number, todo: TodoUpdate): Promise<Todo> => {
    const response = await api.put(`/api/todos/${id}`, todo);
    return response.data;
  },

  toggleComplete: async (id: number): Promise<Todo> => {
    const response = await api.patch(`/api/todos/${id}/toggle-complete`);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/todos/${id}`);
  },
};

export const chatAPI = {
  sendMessage: async (message: string, conversationHistory: Array<{ role: string; content: string }> = []) => {
    const response = await api.post('/api/chat', {
      message,
      conversation_history: conversationHistory,
    });
    return response.data;
  },
};

export default api;

