# eBPF Monitoring with Prometheus and Grafana

## Overview
This project leverages eBPF and Python to gather enhanced system metrics and provides a Terraform script to deploy a monitoring infrastructure with Prometheus and Grafana. It also includes Ansible scripts to automate the monitoring setup across multiple machines, enabling efficient observability with a descriptive Grafana dashboard.

## Features
- **eBPF Metrics Collection:** Using eBPF to gather detailed and accurate system-level metrics.
- **Python Integration:** Enhanced metrics collection with Python scripts.
- **Terraform Deployment:** Provision infrastructure for Prometheus and Grafana using Terraform.
- **Ansible Automation:** Automate deployment and monitoring setup across multiple machines.
- **Grafana Dashboards:** Pre-configured dashboards for real-time log and metric visualization.

## Architecture
1. **eBPF Metrics Collector:**
   - Python scripts leveraging eBPF for in-depth monitoring.
   - Metrics include CPU usage, memory usage, network I/O, and custom system events.

2. **Prometheus:**
   - Metrics storage and querying.
   - Integrated with the eBPF collector for seamless data ingestion.

3. **Grafana:**
   - Pre-built dashboards for log visualization and system health monitoring.
   - Easy-to-understand metrics with descriptive visuals.

4. **Ansible Automation:**
   - Automates the deployment of monitoring agents and configurations across multiple nodes.

5. **Terraform:**
   - Provisions the infrastructure for Prometheus and Grafana servers.

## Setup Instructions

### Prerequisites
- Terraform installed on your local system.
- Ansible installed on the control machine.
- Python (>=3.8) and pip for running eBPF scripts.
- Sufficient permissions to deploy infrastructure and run scripts.

### Step 1: Deploy Infrastructure with Terraform
1. Clone the repository:
   ```bash
   git clone https://github.com/patel-aum/ebpf-monitoring.git
   cd ebpf-monitoring
   ```
2. Initialize Terraform:
   ```bash
   terraform init && terraform plan 
   ```
3. Apply the Terraform configuration:
   ```bash
   terraform apply
   ```
   - Confirm the deployment when prompted.

### Step 2: Deploy Monitoring Agents with Ansible
1. Navigate to the Ansible directory:
   ```
   cd ansible
   ```
2. Update the inventory file with your target machines and ssh access.
3. Run the ping test and findout
``bash
ansible all -i inventory/hosts -m ping
``

![image](https://github.com/user-attachments/assets/8a0e9800-dacc-4269-83f4-0af3c4c2f788)

3. Run the Ansible playbook:
   ```
    ansible-playbook -i inventory/hosts tasks/main.yaml
   ```
![Grafana Dashboard 1](https://github.com/user-attachments/assets/b922ecd9-1bb2-4083-aacb-f6af6a4480bf)
4. Change the ip in promethes yaml and restart promethers by docker-compose restart promethers
 
### Step 3: Visualize Metrics in Grafana
1. Access the Grafana dashboard using the IP address provided by Terraform.
2. Import the pre-configured dashboard JSON from the `grafana` directory.
3. Start monitoring your logs and metrics in real-time!

## Grafana Dashboard Highlights
- **Log Monitoring:** Visualize system logs with enhanced filters.
- **Resource Utilization:**
  - CPU usage.
  - Memory consumption.
  - Network I/O.
- **Custom Metrics:**
  - Application-specific metrics derived from eBPF.

![Grafana Dashboard 2](https://github.com/user-attachments/assets/efeac36e-714d-42ba-b861-96e002694b7c)

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request.
