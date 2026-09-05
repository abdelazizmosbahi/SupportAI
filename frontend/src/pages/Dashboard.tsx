import { Card, CardContent, Typography } from '@mui/material'

export default function DashboardPage() {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="h1" sx={{ fontWeight: 'bold' }}>
          Dashboard
        </Typography>
        <Typography color="text.secondary">Welcome to SupportAI Dashboard</Typography>
      </CardContent>
    </Card>
  )
}