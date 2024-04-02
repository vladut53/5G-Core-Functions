provider "azurem" {
  features{}
}

terraform {
  required_providers {
    azurem = {
        source  = "hashicorp/azurem"
        version = "3.62.1"
    }
  }
}