import { Card, CardContent, Typography } from '@mui/material'

export default function TicketsPage() {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="h1" sx={{ fontWeight: 'bold' }}>
          Tickets
        </Typography>
        <Typography color="text.secondary">Support tickets and handling</Typography>
      </CardContent>
    </Card>
  )
}