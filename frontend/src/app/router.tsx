import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { AskPage } from '@/pages/AskPage/AskPage'
import { AppLayout } from '@/shared/components/layout/AppLayout'

const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      {
        index: true,
        element: <AskPage />,
      },
    ],
  },
])

export function AppRouter() {
  return <RouterProvider router={router} />
}
