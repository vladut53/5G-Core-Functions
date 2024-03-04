locals {
  name   = "Mini-5G-cluster"
  region = "eu-west-1"

  vpc_cidr = "10.123.0.0/16"
  azs      = ["eu-west-1a", "eu-west-1b"]

  public_subnets  = ["10.123.1.0/24", "10.123.2.0/24"]
  private_subnets = ["10.123.3.0/24", "10.123.4.0/24"]
  intra_subnets   = ["10.123.5.0/24", "10.123.6.0/24"]

  tags = {
    Example = local.name
  }
}