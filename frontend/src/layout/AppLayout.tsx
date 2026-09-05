import { Outlet } from 'react-router-dom'
import { Box } from '@mui/material'

import { Sidebar } from './Sidebar'
import { Header } from './Header'

export function AppLayout() {
  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      <Sidebar />
      <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        <Header />
        <Box sx={{ flex: 1, overflowY: 'auto', bgcolor: '#f5f5f5', p: 3 }}>
          <Outlet />
        </Box>
      </Box>
    </Box>
  )
}