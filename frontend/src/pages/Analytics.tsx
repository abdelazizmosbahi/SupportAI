import { Card, CardContent, Typography } from '@mui/material'

export default function AnalyticsPage() {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="h1" sx={{ fontWeight: 'bold' }}>
          Analytics
        </Typography>
        <Typography color="text.secondary">Metrics and charts</Typography>
      </CardContent>
    </Card>
  )
}