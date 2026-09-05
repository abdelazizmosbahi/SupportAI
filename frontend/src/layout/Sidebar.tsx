import { NavLink } from 'react-router-dom'
import { Box, List, ListItemButton, ListItemIcon, ListItemText, Typography } from '@mui/material'
import DashboardIcon from '@mui/icons-material/Dashboard'
import ChatIcon from '@mui/icons-material/Chat'
import LibraryBooksIcon from '@mui/icons-material/LibraryBooks'
import ConfirmationNumberIcon from '@mui/icons-material/ConfirmationNumber'
import AssessmentIcon from '@mui/icons-material/Assessment'
import AnalyticsIcon from '@mui/icons-material/Analytics'
import SettingsIcon from '@mui/icons-material/Settings'
import SupportAgentIcon from '@mui/icons-material/SupportAgent'

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: <DashboardIcon /> },
  { to: '/conversations', label: 'Conversations', icon: <ChatIcon /> },
  { to: '/knowledge-base', label: 'Knowledge Base', icon: <LibraryBooksIcon /> },
  { to: '/tickets', label: 'Tickets', icon: <ConfirmationNumberIcon /> },
  { to: '/evaluations', label: 'Evaluations', icon: <AssessmentIcon /> },
  { to: '/analytics', label: 'Analytics', icon: <AnalyticsIcon /> },
  { to: '/settings', label: 'Settings', icon: <SettingsIcon /> },
]

export function Sidebar() {
  return (
    <Box
      sx={{
        width: 250,
        height: '100%',
        bgcolor: '#1a1a2e',
        color: 'white',
        display: 'flex',
        flexDirection: 'column',
        flexShrink: 0,
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, p: 2, fontSize: 18, fontWeight: 500, borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
        <SupportAgentIcon />
        <span>SupportAI</span>
      </Box>
      <List sx={{ flex: 1, p: 1 }}>
        {navItems.map((item) => (
          <ListItemButton
            key={item.to}
            component={NavLink}
            to={item.to}
            sx={{
              color: 'rgba(255,255,255,0.7)',
              mb: 0.5,
              borderRadius: 2,
              '&.active': {
                bgcolor: 'rgba(103, 58, 183, 0.3)',
                color: 'white',
              },
              '&:hover': {
                bgcolor: 'rgba(255,255,255,0.1)',
                color: 'white',
              },
            }}
          >
            <ListItemIcon sx={{ color: 'inherit', minWidth: 36 }}>{item.icon}</ListItemIcon>
            <ListItemText primary={<Typography variant="body2">{item.label}</Typography>} />
          </ListItemButton>
        ))}
      </List>
    </Box>
  )
}