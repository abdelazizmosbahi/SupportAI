import { Card, CardContent, Typography } from '@mui/material'

export default function EvaluationsPage() {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="h1" sx={{ fontWeight: 'bold' }}>
          Evaluations
        </Typography>
        <Typography color="text.secondary">AI response quality metrics</Typography>
      </CardContent>
    </Card>
  )
}