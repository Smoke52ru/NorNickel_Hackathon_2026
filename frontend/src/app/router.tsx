import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { HomePage } from '@/pages/HomePage/HomePage'
import { AppLayout } from '@/shared/components/layout/AppLayout'

const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
    ],
  },
])

export function AppRouter() {
  return <RouterProvider router={router} />
}
