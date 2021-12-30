variable "sender_email" {
  description = "Sender's email"
  type        = string
}

variable "receiver_email" {
  description = "Receiver's email"
  type        = string
}

variable "schedule" {
  description = "Cron expression for scheduling the emails"
  type        = string
  default     = "cron(10 7 * * ? *)" # everyday at 3.10pm SGT
}

variable "config_filepath" {
  description = "Config filepath relative to infra folder"
  type        = string
  default     = "config/local.json"
}