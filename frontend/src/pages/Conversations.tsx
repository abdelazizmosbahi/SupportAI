import { Card, CardContent, Typography } from '@mui/material'

export default function ConversationsPage() {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="h1" sx={{ fontWeight: 'bold' }}>
          Conversations
        </Typography>
        <Typography color="text.secondary">Conversation list and chat view</Typography>
      </CardContent>
    </Card>
  )
}