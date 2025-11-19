# Frontend - Next.js Todoer Application

The frontend is a Next.js 14 application with a modern neon-dark design system for managing todos.

## Overview

The frontend provides:
- User authentication (login/register)
- Todo management interface (CRUD operations)
- Search and filtering capabilities
- Sorting options
- Chat interface for AI-powered todo management
- Responsive design with neon-dark theme

## Architecture

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context API
- **HTTP Client**: Axios
- **Date Formatting**: date-fns
- **Markdown Rendering**: react-markdown

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx      # Root layout with metadata
│   ├── page.tsx        # Main page component
│   └── globals.css     # Global styles and design system
├── components/
│   ├── ChatWindow.tsx   # Chat interface component
│   ├── LoginForm.tsx   # Authentication form
│   └── TodoList.tsx    # Todo list with filters and pagination
├── contexts/
│   └── AuthContext.tsx # Authentication context provider
├── lib/
│   └── api.ts          # API client functions
├── package.json        # Dependencies and scripts
├── tailwind.config.js  # Tailwind configuration
└── tsconfig.json       # TypeScript configuration
```

## Setup

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

### Starting the Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Design System

The application uses a custom neon-dark design system with:

### Colors

- **Charcoal**: Dark backgrounds (`#0E1118`, `#1F242F`)
- **Dash Green**: Primary accent (`#A9FF5B`)
- **Dash Orange**: Secondary accent (`#FF8B2C`)
- **Dash Gray**: Muted text (`#A0A3AD`)
- **Dash Cream**: Light text (`#F9F7F1`)

### Typography

- **Display Font**: Space Grotesk (headings)
- **Body Font**: Inter (body text)

### Components

- Glass panels with subtle borders and shadows
- Rounded corners (24px-32px border radius)
- Neon accent colors for interactive elements
- Smooth transitions and hover effects

## Features

### Authentication

- User registration and login
- JWT token management
- Protected routes
- Automatic token refresh

### Todo Management

- Create todos with name, description, and due date
- View todos in a paginated list
- Edit todos (double-click to edit)
- Delete todos
- Toggle completion status
- Search todos by name/description
- Filter by completion status
- Sort by name, creation date, or due date
- Pagination controls

### Chat Interface

- Floating chat button
- Natural language todo management
- Markdown rendering for responses
- Conversation history

## API Integration

The frontend communicates with the backend API via the `lib/api.ts` module, which provides:

- `authAPI`: Authentication endpoints
- `todosAPI`: Todo CRUD operations
- `chatAPI`: Chat endpoint

All API calls include JWT tokens from the authentication context.

## Environment Variables

The frontend expects the backend API to be available at `http://localhost:8000` by default. To change this, update the API base URL in `lib/api.ts`.

## Building for Production

```bash
npm run build
npm run start
```

The production build will be optimized and minified.

## Browser Support

The application supports modern browsers:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development Notes

- The app uses Next.js App Router (not Pages Router)
- All components are client components (`'use client'`)
- Authentication state is managed via React Context
- API calls are made using Axios with interceptors for token handling

