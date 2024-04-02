provider "azurerm" {
  features{}
}

terraform {
  required_providers {
    azurem = {
        source  = "hashicorp/azurerm"
        version = "3.62.1"
    }
  }
}
