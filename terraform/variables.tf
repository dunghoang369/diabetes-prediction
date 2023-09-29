// Variables to use accross the project
// which can be accessed by var.project_id
variable "project_id" {
  description = "The project ID to host the cluster in"
  default     = "asr-callcenter"
}

variable "region" {
  description = "The region the cluster in"
  default     = "us-central1"
}
