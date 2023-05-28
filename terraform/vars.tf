variable "account-id" {

  default     = "269012942764"
  description = "aws account id"

}

variable "project-name" {

  default     = "spotify-data-platform"
  description = "name of this project"

}

variable "bucket-names" {

  type    = list(string)
  default = ["landing", "curated"]

}