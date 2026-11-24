variable "aws_region" {
  description = "AWS region for the EKS cluster."
  type        = string
  default     = "ap-south-1"
}

variable "cluster_name" {
  description = "Unique EKS cluster name."
  type        = string
  default     = "devops-portfolio-eks"
}

variable "kubernetes_version" {
  description = "Kubernetes version supported by the selected EKS module and AWS region."
  type        = string
  default     = "1.30"
}
