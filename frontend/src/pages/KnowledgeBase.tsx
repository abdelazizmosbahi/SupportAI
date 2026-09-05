import { Card, CardContent, Typography } from '@mui/material'

export default function KnowledgeBasePage() {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="h1" sx={{ fontWeight: 'bold' }}>
          Knowledge Base
        </Typography>
        <Typography color="text.secondary">Documents, uploads, and status tracking</Typography>
      </CardContent>
    </Card>
  )
}