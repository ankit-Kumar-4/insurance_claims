# Insurance Claims Frontend Web Application - Design Document

## Overview

This document outlines the design and architecture for a modern, high-performance insurance claims frontend web application built with Next.js 14, React 18, TypeScript, and Tailwind CSS.

**Project Location:** `insurance_claims_web/`

## Monorepo Structure

This frontend application is part of the insurance claims monorepo:

```
/Users/ankitkumar/Coding/insurance_claims/     # Root directory
├── .gitignore                                 # Root-level ignore patterns
├── .vscode/                                   # Shared IDE configuration
├── insurance_claims_service/                  # Backend API (Python/FastAPI) ✅
├── insurance_claims_web/                      # Frontend Web App (Next.js/React) 📱
│   ├── .gitignore                            # Node.js-specific patterns
│   ├── src/                                  # Application source code
│   ├── public/                               # Static assets
│   ├── tests/                                # Test suite
│   ├── package.json                          # Dependencies
│   ├── tsconfig.json                         # TypeScript configuration
│   ├── next.config.js                        # Next.js configuration
│   ├── tailwind.config.ts                    # Tailwind CSS configuration
│   ├── .env.local                            # Local environment variables
│   └── README.md                             # Frontend documentation
└── knowledge/                                 # Project documentation
    ├── design/
    │   ├── entities_details.md
    │   ├── backend_service_design.md         # Backend design ✅
    │   └── frontend_web_design.md            # Frontend design (this file)
    └── tasks/
        └── tasks.md
```

## Technology Stack

### Core Framework
- **Next.js 14** (App Router): Modern React framework
  - Server-side rendering (SSR)
  - Static site generation (SSG)
  - File-based routing
  - API routes
  - Image optimization
  - Built-in TypeScript support

### UI Framework & Libraries
- **React 18**: Component-based UI library
  - Concurrent rendering
  - Automatic batching
  - Transitions API
  - Suspense improvements

- **TypeScript 5.3+**: Type-safe development
  - Strong typing
  - IntelliSense support
  - Compile-time error detection
  - Better refactoring support

### Styling & UI Components
- **Tailwind CSS 3.4+**: Utility-first CSS framework
  - Responsive design
  - Dark mode support
  - Custom design system
  - JIT (Just-In-Time) compiler

- **shadcn/ui**: Beautiful, accessible component library
  - Built on Radix UI primitives
  - Fully customizable
  - Copy-paste components
  - Accessibility by default

- **Radix UI**: Unstyled, accessible components
  - Dialog, Dropdown, Select, etc.
  - ARIA-compliant
  - Full keyboard navigation

- **Lucide Icons**: Modern icon library
  - Consistent design
  - Tree-shakeable
  - SVG-based

### State Management
- **Zustand**: Lightweight state management
  - Simple API
  - No boilerplate
  - TypeScript support
  - Middleware support

- **TanStack Query (React Query)**: Server state management
  - Automatic caching
  - Background refetching
  - Optimistic updates
  - Pagination support

### Form Handling & Validation
- **React Hook Form**: Performant form library
  - Minimal re-renders
  - Easy validation
  - Built-in error handling

- **Zod**: TypeScript-first schema validation
  - Runtime validation
  - Type inference
  - Composable validators

### Data Fetching & API
- **Axios**: HTTP client
  - Request/response interceptors
  - Automatic retries
  - TypeScript support

- **TanStack Query**: Data fetching & caching
  - Automatic revalidation
  - Infinite queries
  - Mutations with rollback

### Charts & Visualizations
- **Recharts**: React chart library
  - Responsive charts
  - Composable API
  - Customizable

- **ApexCharts**: Modern charting library
  - Interactive charts
  - Real-time updates
  - Multiple chart types

### Date & Time
- **date-fns**: Modern date utility library
  - Tree-shakeable
  - Immutable
  - TypeScript support

### File Handling
- **react-dropzone**: File upload with drag & drop
  - Multiple file support
  - File type validation
  - Preview generation

### PDF Generation
- **jsPDF**: PDF generation
  - Client-side rendering
  - Custom layouts

- **react-pdf**: PDF viewer
  - Page navigation
  - Zoom controls

### Tables & Data Display
- **TanStack Table**: Headless table library
  - Sorting
  - Filtering
  - Pagination
  - Virtual scrolling

### Authentication
- **NextAuth.js**: Authentication for Next.js
  - JWT support
  - OAuth providers
  - Credentials provider
  - Session management

### Testing
- **Vitest**: Fast unit test framework
  - Vite-powered
  - Jest compatibility
  - TypeScript support

- **React Testing Library**: Component testing
  - User-centric testing
  - Accessibility testing

- **Playwright**: E2E testing
  - Cross-browser testing
  - Auto-wait
  - Network mocking

### Code Quality
- **ESLint**: JavaScript/TypeScript linter
  - Next.js rules
  - React rules
  - Custom rules

- **Prettier**: Code formatter
  - Consistent style
  - Auto-formatting

- **Husky**: Git hooks
  - Pre-commit checks
  - Pre-push validation

### Additional Libraries
- **clsx / cn**: Conditional class names utility
- **react-hot-toast**: Notifications
- **framer-motion**: Animations
- **react-error-boundary**: Error handling
- **lodash/debounce**: Utility functions (tree-shakeable imports)

## Project Structure

```
insurance_claims_web/
├── public/                        # Static assets
│   ├── images/
│   │   ├── logo.svg
│   │   ├── hero-bg.jpg
│   │   └── insurance-icons/
│   ├── fonts/
│   └── favicon.ico
│
├── src/                           # Source code
│   ├── app/                       # Next.js App Router
│   │   ├── (auth)/               # Auth route group
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   ├── register/
│   │   │   │   └── page.tsx
│   │   │   ├── forgot-password/
│   │   │   │   └── page.tsx
│   │   │   └── layout.tsx
│   │   │
│   │   ├── (dashboard)/          # Protected dashboard routes
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx      # Main dashboard
│   │   │   │
│   │   │   ├── policies/
│   │   │   │   ├── page.tsx      # List policies
│   │   │   │   ├── [id]/         # Policy details
│   │   │   │   │   ├── page.tsx
│   │   │   │   │   └── edit/page.tsx
│   │   │   │   └── new/page.tsx  # Create policy
│   │   │   │
│   │   │   ├── claims/
│   │   │   │   ├── page.tsx      # List claims
│   │   │   │   ├── [id]/         # Claim details
│   │   │   │   │   ├── page.tsx
│   │   │   │   │   └── edit/page.tsx
│   │   │   │   └── new/page.tsx  # File claim
│   │   │   │
│   │   │   ├── customers/
│   │   │   │   ├── page.tsx
│   │   │   │   ├── [id]/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── new/page.tsx
│   │   │   │
│   │   │   ├── agents/
│   │   │   │   ├── page.tsx
│   │   │   │   ├── [id]/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── new/page.tsx
│   │   │   │
│   │   │   ├── quotes/
│   │   │   │   ├── page.tsx
│   │   │   │   ├── [id]/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── new/page.tsx
│   │   │   │
│   │   │   ├── premiums/
│   │   │   │   ├── page.tsx
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx
│   │   │   │
│   │   │   ├── documents/
│   │   │   │   ├── page.tsx
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx
│   │   │   │
│   │   │   ├── reports/
│   │   │   │   ├── page.tsx
│   │   │   │   ├── policies/page.tsx
│   │   │   │   ├── claims/page.tsx
│   │   │   │   └── revenue/page.tsx
│   │   │   │
│   │   │   ├── settings/
│   │   │   │   ├── page.tsx
│   │   │   │   ├── profile/page.tsx
│   │   │   │   └── security/page.tsx
│   │   │   │
│   │   │   └── layout.tsx        # Dashboard layout with sidebar
│   │   │
│   │   ├── api/                   # API routes (if needed)
│   │   │   └── auth/
│   │   │       └── [...nextauth]/
│   │   │           └── route.ts
│   │   │
│   │   ├── layout.tsx             # Root layout
│   │   ├── page.tsx               # Landing page
│   │   ├── error.tsx              # Error boundary
│   │   ├── loading.tsx            # Loading state
│   │   └── not-found.tsx          # 404 page
│   │
│   ├── components/                # React components
│   │   ├── ui/                    # Base UI components (shadcn/ui)
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── dropdown-menu.tsx
│   │   │   ├── form.tsx
│   │   │   ├── input.tsx
│   │   │   ├── label.tsx
│   │   │   ├── select.tsx
│   │   │   ├── table.tsx
│   │   │   ├── tabs.tsx
│   │   │   ├── toast.tsx
│   │   │   └── ...
│   │   │
│   │   ├── forms/                 # Form components
│   │   │   ├── PolicyForm.tsx
│   │   │   ├── ClaimForm.tsx
│   │   │   ├── CustomerForm.tsx
│   │   │   ├── QuoteCalculator.tsx
│   │   │   └── FileUploader.tsx
│   │   │
│   │   ├── tables/                # Data table components
│   │   │   ├── PoliciesTable.tsx
│   │   │   ├── ClaimsTable.tsx
│   │   │   ├── CustomersTable.tsx
│   │   │   ├── DataTable.tsx      # Reusable data table
│   │   │   └── DataTablePagination.tsx
│   │   │
│   │   ├── cards/                 # Card components
│   │   │   ├── PolicyCard.tsx
│   │   │   ├── ClaimCard.tsx
│   │   │   ├── StatCard.tsx
│   │   │   └── DashboardCard.tsx
│   │   │
│   │   ├── charts/                # Chart components
│   │   │   ├── RevenueChart.tsx
│   │   │   ├── ClaimsChart.tsx
│   │   │   ├── PremiumChart.tsx
│   │   │   └── PerformanceChart.tsx
│   │   │
│   │   ├── layout/                # Layout components
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── Navbar.tsx
│   │   │   └── DashboardShell.tsx
│   │   │
│   │   ├── shared/                # Shared components
│   │   │   ├── LoadingSpinner.tsx
│   │   │   ├── ErrorMessage.tsx
│   │   │   ├── EmptyState.tsx
│   │   │   ├── SearchBar.tsx
│   │   │   ├── Pagination.tsx
│   │   │   ├── Badge.tsx
│   │   │   ├── StatusBadge.tsx
│   │   │   └── ConfirmDialog.tsx
│   │   │
│   │   └── features/              # Feature-specific components
│   │       ├── auth/
│   │       │   ├── LoginForm.tsx
│   │       │   ├── RegisterForm.tsx
│   │       │   └── ProtectedRoute.tsx
│   │       ├── policies/
│   │       │   ├── PolicyDetails.tsx
│   │       │   ├── PolicyList.tsx
│   │       │   └── PolicyActions.tsx
│   │       ├── claims/
│   │       │   ├── ClaimTimeline.tsx
│   │       │   ├── ClaimDocuments.tsx
│   │       │   └── ClaimStatus.tsx
│   │       └── dashboard/
│   │           ├── DashboardStats.tsx
│   │           ├── RecentActivity.tsx
│   │           └── QuickActions.tsx
│   │
│   ├── lib/                       # Utility functions
│   │   ├── api/                   # API client
│   │   │   ├── axios.ts          # Axios instance
│   │   │   ├── endpoints.ts      # API endpoints
│   │   │   └── client.ts         # API client
│   │   │
│   │   ├── hooks/                 # Custom React hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── usePolicies.ts
│   │   │   ├── useClaims.ts
│   │   │   ├── useCustomers.ts
│   │   │   ├── useDebounce.ts
│   │   │   ├── useLocalStorage.ts
│   │   │   └── useMediaQuery.ts
│   │   │
│   │   ├── utils/                 # Utility functions
│   │   │   ├── cn.ts             # className utility
│   │   │   ├── formatters.ts     # Date, currency formatters
│   │   │   ├── validators.ts     # Validation functions
│   │   │   ├── constants.ts      # App constants
│   │   │   └── helpers.ts        # Helper functions
│   │   │
│   │   ├── stores/                # Zustand stores
│   │   │   ├── authStore.ts
│   │   │   ├── uiStore.ts
│   │   │   └── notificationStore.ts
│   │   │
│   │   └── queries/               # React Query hooks
│   │       ├── policies.ts
│   │       ├── claims.ts
│   │       ├── customers.ts
│   │       ├── quotes.ts
│   │       └── payments.ts
│   │
│   ├── types/                     # TypeScript type definitions
│   │   ├── index.ts              # Re-exports
│   │   ├── api.ts                # API types
│   │   ├── policy.ts
│   │   ├── claim.ts
│   │   ├── customer.ts
│   │   ├── agent.ts
│   │   ├── quote.ts
│   │   ├── payment.ts
│   │   └── common.ts
│   │
│   ├── styles/                    # Global styles
│   │   └── globals.css           # Global CSS + Tailwind imports
│   │
│   ├── config/                    # Configuration
│   │   ├── site.ts               # Site metadata
│   │   ├── navigation.ts         # Navigation config
│   │   └── theme.ts              # Theme config
│   │
│   └── middleware.ts              # Next.js middleware (auth, etc.)
│
├── tests/                         # Tests
│   ├── unit/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── utils/
│   ├── integration/
│   │   └── api/
│   └── e2e/
│       ├── auth.spec.ts
│       ├── policies.spec.ts
│       └── claims.spec.ts
│
├── .env.example                   # Environment variables template
├── .env.local                     # Local environment variables (gitignored)
├── .eslintrc.json                 # ESLint configuration
├── .gitignore
├── .prettierrc                    # Prettier configuration
├── components.json                # shadcn/ui config
├── next.config.js                 # Next.js configuration
├── package.json                   # Dependencies
├── pnpm-lock.yaml                # Lock file (if using pnpm)
├── postcss.config.js              # PostCSS configuration
├── tailwind.config.ts             # Tailwind configuration
├── tsconfig.json                  # TypeScript configuration
├── vitest.config.ts               # Vitest configuration
└── README.md                      # Project documentation
```

## Architecture Patterns

### 1. Feature-Based Architecture

```
Features are organized by domain:
- Each feature has its own components, hooks, and types
- Promotes code colocation and maintainability
- Easy to understand and scale
```

### 2. Component Composition

```tsx
// Compound component pattern
<Dialog>
  <DialogTrigger>Open</DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Title</DialogTitle>
    </DialogHeader>
    <DialogBody>Content</DialogBody>
    <DialogFooter>
      <Button>Close</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### 3. Custom Hooks Pattern

```tsx
// Encapsulate logic in reusable hooks
const usePolicies = () => {
  return useQuery({
    queryKey: ['policies'],
    queryFn: fetchPolicies,
  })
}
```

### 4. Container/Presentational Pattern

```tsx
// Container: Handles logic
const PolicyListContainer = () => {
  const { data, isLoading } = usePolicies()
  return <PolicyList policies={data} loading={isLoading} />
}

// Presentational: Pure UI
const PolicyList = ({ policies, loading }) => {
  // Render UI
}
```

## Implementation Status

### Status: PLANNING (0%)

**Current Phase:** Design & Architecture  
**Backend Dependency:** Phase 3 (Schemas) must be complete before frontend API integration

**Planned Phases:**
1. ⏳ Project Setup & Configuration
2. ⏳ UI Component Library (shadcn/ui)
3. ⏳ Authentication & Authorization
4. ⏳ Dashboard & Navigation
5. ⏳ Policy Management UI
6. ⏳ Claims Management UI
7. ⏳ Customer Management UI
8. ⏳ Agent & Underwriter Portals
9. ⏳ Reports & Analytics
10. ⏳ File Upload & Document Management
11. ⏳ Testing & Optimization
12. ⏳ Deployment

## User Roles & Access

### Role-Based Interface

**1. Customer Portal**
- View own policies
- File claims
- Upload documents
- Make payments
- View claim status
- Request quotes

**2. Agent Dashboard**
- Manage customers
- Create policies
- Generate quotes
- View commissions
- Track performance
- Access reports

**3. Claims Adjuster Interface**
- Review claims
- Request additional documents
- Approve/reject claims
- Process settlements
- Track claim timeline

**4. Underwriter Dashboard**
- Review risk assessments
- Approve policies
- Set premiums
- Review applications

**5. Admin Panel**
- Manage all entities
- View system analytics
- Configure settings
- User management
- Audit logs

## Key Features & Pages

### 1. Landing Page
```
Features:
- Hero section with CTA
- Product overview
- Customer testimonials
- Quick quote calculator
- Contact information
- SEO optimized
```

### 2. Authentication Pages
```
- Login (email/password, OAuth)
- Register (multi-step form)
- Forgot Password
- Reset Password
- Email Verification
- Two-Factor Authentication
```

### 3. Dashboard (Role-based)
```
Components:
- Summary statistics
- Recent activity
- Quick actions
- Notifications
- Pending tasks
- Charts & graphs
```

### 4. Policy Management
```
Pages:
- Policy list (filterable, sortable)
- Policy details
- Create/Edit policy
- Policy documents
- Premium schedule
- Renewal management
- Endorsements

Features:
- Advanced search
- Bulk operations
- Export to PDF/Excel
- Timeline view
```

### 5. Claims Management
```
Pages:
- Claims list
- Claim details
- File new claim
- Claim timeline
- Document upload
- Status tracking

Features:
- Real-time status updates
- Document management
- Communication thread
- Settlement calculator
```

### 6. Customer Management
```
Pages:
- Customer list
- Customer profile
- Customer policies
- Customer claims
- Payment history
- Communication log

Features:
- 360° customer view
- Quick actions
- Notes & tags
- Contact management
```

### 7. Quote Calculator
```
Features:
- Multi-step wizard
- Real-time premium calculation
- Coverage comparison
- PDF quote generation
- Email quote
- Convert to policy
```

### 8. Reports & Analytics
```
Reports:
- Revenue dashboard
- Claims statistics
- Agent performance
- Policy analytics
- Customer retention
- Financial reports

Features:
- Interactive charts
- Date range filters
- Export functionality
- Scheduled reports
```

### 9. Document Management
```
Features:
- Drag & drop upload
- File preview
- Version control
- Search & filter
- Bulk download
- Share documents
```

### 10. Settings
```
Pages:
- Profile settings
- Security settings
- Notification preferences
- Theme customization
- Language selection
```

## UI/UX Design System

### Color Palette

```typescript
// Primary colors
const colors = {
  primary: {
    50: '#eff6ff',
    100: '#dbeafe',
    500: '#3b82f6', // Brand blue
    600: '#2563eb',
    900: '#1e3a8a',
  },
  success: '#10b981', // Green
  warning: '#f59e0b', // Amber
  error: '#ef4444',   // Red
  neutral: {
    50: '#f9fafb',
    100: '#f3f4f6',
    500: '#6b7280',
    900: '#111827',
  },
}
```

### Typography

```typescript
const typography = {
  fonts: {
    sans: 'Inter, system-ui, sans-serif',
    mono: 'JetBrains Mono, monospace',
  },
  sizes: {
    xs: '0.75rem',   // 12px
    sm: '0.875rem',  // 14px
    base: '1rem',    // 16px
    lg: '1.125rem',  // 18px
    xl: '1.25rem',   // 20px
    '2xl': '1.5rem', // 24px
    '3xl': '1.875rem', // 30px
    '4xl': '2.25rem',  // 36px
  },
}
```

### Spacing System

```typescript
// Tailwind default spacing scale (4px base)
const spacing = {
  0: '0',
  1: '0.25rem',  // 4px
  2: '0.5rem',   // 8px
  3: '0.75rem',  // 12px
  4: '1rem',     // 16px
  5: '1.25rem',  // 20px
  6: '1.5rem',   // 24px
  8: '2rem',     // 32px
  12: '3rem',    // 48px
  16: '4rem',    // 64px
}
```

### Component Variants

```typescript
// Button variants
const buttonVariants = {
  default: 'bg-primary-500 text-white hover:bg-primary-600',
  outline: 'border border-primary-500 text-primary-500 hover:bg-primary-50',
  ghost: 'text-primary-500 hover:bg-primary-50',
  destructive: 'bg-error text-white hover:bg-error/90',
}

// Card shadows
const shadows = {
  sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
  md: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
  lg: '0 10px 15px -3px rgb(0 0 0 / 0.1)',
  xl: '0 20px 25px -5px rgb(0 0 0 / 0.1)',
}
```

## State Management Strategy

### 1. Server State (TanStack Query)

```typescript
// lib/queries/policies.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api/client'
import type { Policy, PolicyCreate } from '@/types'

export const usePolicies = (filters?: PolicyFilters) => {
  return useQuery({
    queryKey: ['policies', filters],
    queryFn: () => api.policies.list(filters),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export const usePolicy = (id: string) => {
  return useQuery({
    queryKey: ['policy', id],
    queryFn: () => api.policies.get(id),
    enabled: !!id,
  })
}

export const useCreatePolicy = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (data: PolicyCreate) => api.policies.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['policies'] })
      toast.success('Policy created successfully')
    },
    onError: (error) => {
      toast.error('Failed to create policy')
    },
  })
}

export const useUpdatePolicy = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: PolicyUpdate }) => 
      api.policies.update(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['policy', id] })
      queryClient.invalidateQueries({ queryKey: ['policies'] })
      toast.success('Policy updated successfully')
    },
  })
}
```

### 2. Client State (Zustand)

```typescript
// lib/stores/authStore.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  updateUser: (user: User) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      
      login: async (email, password) => {
        const { user, token } = await api.auth.login(email, password)
        set({ user, token, isAuthenticated: true })
      },
      
      logout: () => {
        set({ user: null, token: null, isAuthenticated: false })
      },
      
      updateUser: (user) => {
        set({ user })
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ token: state.token }),
    }
  )
)
```

### 3. UI State (Zustand)

```typescript
// lib/stores/uiStore.ts
import { create } from 'zustand'

interface UIState {
  sidebarOpen: boolean
  theme: 'light' | 'dark'
  toggleSidebar: () => void
  setTheme: (theme: 'light' | 'dark') => void
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  theme: 'light',
  
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setTheme: (theme) => set({ theme }),
}))
```

## API Integration

### Axios Client Setup

```typescript
// lib/api/axios.ts
import axios from 'axios'
import { useAuthStore } from '@/lib/stores/authStore'

const axiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor (add auth token)
axiosInstance.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor (handle errors)
axiosInstance.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default axiosInstance
```

### API Client

```typescript
// lib/api/client.ts
import axios from './axios'
import type { 
  Policy, PolicyCreate, PolicyUpdate, 
  Claim, ClaimCreate, ClaimUpdate,
  Customer, CustomerCreate, CustomerUpdate 
} from '@/types'

export const api = {
  // Policies
  policies: {
    list: (params?: any) => axios.get<Policy[]>('/policies', { params }),
    get: (id: string) => axios.get<Policy>(`/policies/${id}`),
    create: (data: PolicyCreate) => axios.post<Policy>('/policies', data),
    update: (id: string, data: PolicyUpdate) => 
      axios.patch<Policy>(`/policies/${id}`, data),
    delete: (id: string) => axios.delete(`/policies/${id}`),
    export: (params?: any) => 
      axios.get('/policies/export', { params, responseType: 'blob' }),
  },
  
  // Claims
  claims: {
    list: (params?: any) => axios.get<Claim[]>('/claims', { params }),
    get: (id: string) => axios.get<Claim>(`/claims/${id}`),
    create: (data: ClaimCreate) => axios.post<Claim>('/claims', data),
    update: (id: string, data: ClaimUpdate) => 
      axios.patch<Claim>(`/claims/${id}`, data),
    approve: (id: string) => axios.post(`/claims/${id}/approve`),
    reject: (id: string, reason: string) => 
      axios.post(`/claims/${id}/reject`, { reason }),
  },
  
  // Customers
  customers: {
    list: (params?: any) => axios.get<Customer[]>('/customers', { params }),
    get: (id: string) => axios.get<Customer>(`/customers/${id}`),
    create: (data: CustomerCreate) => axios.post<Customer>('/customers', data),
    update: (id: string, data: CustomerUpdate) => 
      axios.patch<Customer>(`/customers/${id}`, data),
    delete: (id: string) => axios.delete(`/customers/${id}`),
  },
  
  // Quotes
  quotes: {
    calculate: (data: QuoteRequest) => axios.post('/quotes/calculate', data),
    create: (data: QuoteCreate) => axios.post('/quotes', data),
    convert: (id: string) => axios.post(`/quotes/${id}/convert`),
  },
  
  // Documents
  documents: {
    upload: (file: File, entityType: string, entityId: string) => {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('entity_type', entityType)
      formData.append('entity_id', entityId)
      return axios.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
    },
    download: (id: string) => 
      axios.get(`/documents/${id}/download`, { responseType: 'blob' }),
  },
  
  // Auth
  auth: {
    login: (email: string, password: string) => 
      axios.post('/auth/login', { email, password }),
    register: (data: RegisterData) => axios.post('/auth/register', data),
    logout: () => axios.post('/auth/logout'),
    refreshToken: () => axios.post('/auth/refresh'),
  },
}
```

## Form Handling

### React Hook Form + Zod

```typescript
// components/forms/PolicyForm.tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'

const policySchema = z.object({
  policy_number: z.string().min(1, 'Policy number is required'),
  policy_type: z.enum(['auto', 'health', 'life', 'property']),
  policy_holder_id: z.number().positive(),
  start_date: z.date(),
  end_date: z.date(),
  premium_amount: z.number().positive('Premium must be positive'),
  coverage_amount: z.number().positive('Coverage must be positive'),
})

type PolicyFormValues = z.infer<typeof policySchema>

export function PolicyForm({ policy, onSubmit }: PolicyFormProps) {
  const form = useForm<PolicyFormValues>({
    resolver: zodResolver(policySchema),
    defaultValues: policy || {
      policy_type: 'auto',
      premium_amount: 0,
      coverage_amount: 0,
    },
  })
  
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="policy_number"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Policy Number</FormLabel>
              <FormControl>
                <Input placeholder="POL-2024-001" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        
        <FormField
          control={form.control}
          name="policy_type"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Policy Type</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select type" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem value="auto">Auto</SelectItem>
                  <SelectItem value="health">Health</SelectItem>
                  <SelectItem value="life">Life</SelectItem>
                  <SelectItem value="property">Property</SelectItem>
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />
        
        <Button type="submit" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? 'Saving...' : 'Save Policy'}
        </Button>
      </form>
    </Form>
  )
}
```

## Data Tables

### TanStack Table Implementation

```typescript
// components/tables/PoliciesTable.tsx
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  type ColumnDef,
} from '@tanstack/react-table'
import { Policy } from '@/types'

const columns: ColumnDef<Policy>[] = [
  {
    accessorKey: 'policy_number',
    header: 'Policy Number',
    cell: ({ row }) => (
      <Link href={`/dashboard/policies/${row.original.id}`}>
        {row.getValue('policy_number')}
      </Link>
    ),
  },
  {
    accessorKey: 'policy_type',
    header: 'Type',
    cell: ({ row }) => {
      const type = row.getValue('policy_type') as string
      return <Badge variant="secondary">{type}</Badge>
    },
  },
  {
    accessorKey: 'status',
    header: 'Status',
    cell: ({ row }) => {
      const status = row.getValue('status') as string
      return <StatusBadge status={status} />
    },
  },
  {
    accessorKey: 'premium_amount',
    header: 'Premium',
    cell: ({ row }) => {
      const amount = parseFloat(row.getValue('premium_amount'))
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      }).format(amount)
    },
  },
  {
    id: 'actions',
    cell: ({ row }) => <PolicyActions policy={row.original} />,
  },
]

export function PoliciesTable({ data }: { data: Policy[] }) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  })
  
  return (
    <div className="space-y-4">
      <DataTable table={table} />
      <DataTablePagination table={table} />
    </div>
  )
}
```

## Authentication

### NextAuth.js Configuration

```typescript
// app/api/auth/[...nextauth]/route.ts
import NextAuth from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'
import { api } from '@/lib/api/client'

export const authOptions = {
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null
        }
        
        try {
          const { user, token } = await api.auth.login(
            credentials.email,
            credentials.password
          )
          
          return {
            ...user,
            accessToken: token,
          }
        } catch (error) {
          return null
        }
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.accessToken = user.accessToken
        token.user = user
      }
      return token
    },
    async session({ session, token }) {
      session.user = token.user
      session.accessToken = token.accessToken
      return session
    },
  },
  pages: {
    signIn: '/login',
    signOut: '/login',
    error: '/login',
  },
}

const handler = NextAuth(authOptions)
export { handler as GET, handler as POST }
```

### Protected Route

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { getToken } from 'next-auth/jwt'

export async function middleware(request: NextRequest) {
  const token = await getToken({ req: request })
  
  // Check if accessing protected route
  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    if (!token) {
      const loginUrl = new URL('/login', request.url)
      loginUrl.searchParams.set('callbackUrl', request.url)
      return NextResponse.redirect(loginUrl)
    }
  }
  
  // Check role-based access
  if (request.nextUrl.pathname.startsWith('/dashboard/admin')) {
    if (token?.role !== 'admin' && token?.role !== 'super_admin') {
      return NextResponse.redirect(new URL('/dashboard', request.url))
    }
  }
  
  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*'],
}
```

## Performance Optimization

### 1. Code Splitting

```typescript
// Dynamic imports for heavy components
const PolicyChart = dynamic(() => import('@/components/charts/PolicyChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false,
})

const PDFViewer = dynamic(() => import('@/components/PDFViewer'), {
  ssr: false,
})
```

### 2. Image Optimization

```tsx
import Image from 'next/image'

<Image
  src="/images/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority
  placeholder="blur"
  blurDataURL="data:image/..."
/>
```

### 3. React Query Optimization

```typescript
// Prefetch data for better UX
const queryClient = useQueryClient()

const prefetchPolicy = (id: string) => {
  queryClient.prefetchQuery({
    queryKey: ['policy', id],
    queryFn: () => api.policies.get(id),
  })
}

// Optimistic updates
const { mutate } = useMutation({
  mutationFn: updatePolicy,
  onMutate: async (newPolicy) => {
    await queryClient.cancelQueries({ queryKey: ['policy', newPolicy.id] })
    const previousPolicy = queryClient.getQueryData(['policy', newPolicy.id])
    queryClient.setQueryData(['policy', newPolicy.id], newPolicy)
    return { previousPolicy }
  },
  onError: (err, newPolicy, context) => {
    queryClient.setQueryData(['policy', newPolicy.id], context.previousPolicy)
  },
})
```

### 4. Memoization

```typescript
import { useMemo, useCallback } from 'react'

const ExpensiveComponent = ({ data }) => {
  // Memoize expensive calculations
  const processedData = useMemo(() => {
    return data.map(item => complexCalculation(item))
  }, [data])
  
  // Memoize callbacks
  const handleClick = useCallback((id: string) => {
    // Handle click
  }, [])
  
  return <div>{/* Render */}</div>
}
```

## Testing Strategy

### 1. Unit Tests (Vitest + React Testing Library)

```typescript
// tests/unit/components/PolicyCard.test.tsx
import { render, screen } from '@testing-library/react'
import { PolicyCard } from '@/components/cards/PolicyCard'

describe('PolicyCard', () => {
  const mockPolicy = {
    id: 1,
    policy_number: 'POL-001',
    policy_type: 'auto',
    status: 'active',
    premium_amount: 500,
  }
  
  it('renders policy information correctly', () => {
    render(<PolicyCard policy={mockPolicy} />)
    
    expect(screen.getByText('POL-001')).toBeInTheDocument()
    expect(screen.getByText('auto')).toBeInTheDocument()
    expect(screen.getByText('$500.00')).toBeInTheDocument()
  })
  
  it('displays active status badge', () => {
    render(<PolicyCard policy={mockPolicy} />)
    
    const statusBadge = screen.getByText('active')
    expect(statusBadge).toHaveClass('bg-green-100')
  })
})
```

### 2. Integration Tests

```typescript
// tests/integration/api/policies.test.ts
import { api } from '@/lib/api/client'
import { setupServer } from 'msw/node'
import { http, HttpResponse } from 'msw'

const server = setupServer(
  http.get('/api/v1/policies', () => {
    return HttpResponse.json([
      { id: 1, policy_number: 'POL-001' },
    ])
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('Policies API', () => {
  it('fetches policies list', async () => {
    const policies = await api.policies.list()
    expect(policies).toHaveLength(1)
    expect(policies[0].policy_number).toBe('POL-001')
  })
})
```

### 3. E2E Tests (Playwright)

```typescript
// tests/e2e/policies.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Policy Management', () => {
  test('should create a new policy', async ({ page }) => {
    await page.goto('/login')
    await page.fill('[name="email"]', 'admin@example.com')
    await page.fill('[name="password"]', 'password')
    await page.click('button[type="submit"]')
    
    await page.goto('/dashboard/policies/new')
    await page.fill('[name="policy_number"]', 'POL-TEST-001')
    await page.selectOption('[name="policy_type"]', 'auto')
    await page.fill('[name="premium_amount"]', '500')
    await page.fill('[name="coverage_amount"]', '50000')
    
    await page.click('button[type="submit"]')
    await expect(page.locator('text=Policy created successfully')).toBeVisible()
  })
})
```

## Deployment Strategy

### Environment Variables

```env
# .env.example
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key
NEXTAUTH_URL=http://localhost:3000
```

### Build & Deploy

```json
// package.json scripts
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "vitest",
    "test:e2e": "playwright test",
    "type-check": "tsc --noEmit"
  }
}
```

### Docker Configuration

```dockerfile
# Dockerfile
FROM node:20-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV production
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT 3000

CMD ["node", "server.js"]
```

### Vercel Deployment (Recommended)

```json
// vercel.json
{
  "buildCommand": "pnpm run build",
  "devCommand": "pnpm run dev",
  "installCommand": "pnpm install",
  "framework": "nextjs"
}
```

## Accessibility

### WCAG 2.1 Level AA Compliance

```tsx
// Semantic HTML
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/dashboard">Dashboard</a></li>
  </ul>
</nav>

// ARIA labels
<button aria-label="Close dialog" onClick={onClose}>
  <X className="w-4 h-4" />
</button>

// Focus management
<Dialog>
  <DialogContent>
    <button ref={closeButtonRef} onClick={onClose}>Close</button>
  </DialogContent>
</Dialog>

// Keyboard navigation
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick()
    }
  }}
>
  Action
</div>
```

## SEO Optimization

### Next.js Metadata API

```typescript
// app/layout.tsx
export const metadata: Metadata = {
  title: {
    default: 'Insurance Claims Management System',
    template: '%s | Insurance Claims',
  },
  description: 'Comprehensive insurance claims management platform',
  keywords: ['insurance', 'claims', 'policy', 'management'],
  authors: [{ name: 'Your Company' }],
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://insurance.example.com',
    siteName: 'Insurance Claims',
  },
}

// app/dashboard/policies/[id]/page.tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  const policy = await api.policies.get(params.id)
  return {
    title: `Policy ${policy.policy_number}`,
    description: `View and manage policy ${policy.policy_number}`,
  }
}
```

## Progressive Web App (PWA)

```typescript
// next.config.js
const withPWA = require('next-pwa')({
  dest: 'public',
  disable: process.env.NODE_ENV === 'development',
  register: true,
  skipWaiting: true,
})

module.exports = withPWA({
  // Next.js config
})
```

## Conclusion

This comprehensive frontend design provides a production-ready, scalable, and maintainable web application for the insurance claims system. The design includes:

✅ **Modern Tech Stack**: Next.js 14, React 18, TypeScript, Tailwind CSS  
✅ **Complete Feature Set**: 10+ major features with role-based access  
✅ **Performance Optimized**: Code splitting, image optimization, caching  
✅ **Type Safety**: Full TypeScript coverage with Zod validation  
✅ **State Management**: TanStack Query for server state, Zustand for client state  
✅ **Beautiful UI**: shadcn/ui component library with dark mode support  
✅ **Responsive Design**: Mobile-first approach with Tailwind CSS  
✅ **Accessibility**: WCAG 2.1 Level AA compliance  
✅ **Testing**: Unit, integration, and E2E test coverage  
✅ **SEO Optimized**: Next.js metadata API and PWA support  
✅ **Developer Experience**: Hot reload, TypeScript, ESLint, Prettier  

The architecture follows React and Next.js best practices with clear separation of concerns, comprehensive error handling, and extensive documentation.

---

**Next Steps:**
1. Set up Next.js project with TypeScript
2. Install and configure dependencies
3. Set up Tailwind CSS and shadcn/ui
4. Implement authentication with NextAuth.js
5. Create base layouts and navigation
6. Build UI component library
7. Implement API integration layer
8. Create dashboard and main features
9. Add form handling and validation
10. Implement data tables with TanStack Table
11. Add charts and analytics
12. Build role-based access control
13. Write comprehensive tests
14. Optimize performance
15. Deploy to Vercel/production
