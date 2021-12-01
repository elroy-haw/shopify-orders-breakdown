resource "aws_ses_email_identity" "sender" {
  email = "<UPDATE THIS TO YOUR SENDER'S EMAIL>"
}

resource "aws_ses_email_identity" "receiver" {
  email = "<UPDATE THIS TO YOUR RECEIVER'S EMAIL>"
}