import { Card, CardContent, Typography } from '@mui/material'

export default function SettingsPage() {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="h1" sx={{ fontWeight: 'bold' }}>
          Settings
        </Typography>
        <Typography color="text.secondary">Organization, members, and profile</Typography>
      </CardContent>
    </Card>
  )
}