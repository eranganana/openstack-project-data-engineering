# OpenStack Multi-Server Deployment for Data Engineering

## Project Overview
Automated deployment of a complete data engineering infrastructure on OpenStack cloud, including production server, development server, and a 3-node Ray cluster for distributed computing.

## 🏗️ Architecture
```
┌─────────────────┐
│ Jump Node │
│ (Floating IP) │
└────────┬────────┘
│
┌──────────────┼──────────────┐
│ │ │
┌────▼────┐ ┌─────▼─────┐ ┌────▼────┐
│Production│ │Development│ │ Ray │
│ Server │ │ Server │ │ Cluster │
└─────────┘ └───────────┘ └────┬────┘
│
┌─────────┼─────────┐
│ │ │
┌──▼──┐ ┌──▼──┐ ┌──▼──┐
│Node1│ │Node2│ │Node3│
└─────┘ └─────┘ └─────┘
```
text

## 🛠️ Technologies Used
- **OpenStack** (Nova, Neutron, Keystone)
- **Python** (Novaclient, OpenStack SDK)
- **Ansible** (Configuration Management)
- **Bash** (Automation Scripts)
- **Git** (Version Control)
- **Ray** (Distributed Computing)

## 👥 My Role & Contributions
- **Infrastructure as Code**: Wrote Python scripts to automate OpenStack instance creation
- **Configuration Management**: Created Ansible playbooks for server setup
- **Cloud Automation**: Implemented cloud-init for automated server configuration
- **Security**: Managed SSH keys, security groups, and credential protection
- **CI/CD**: Configured Git hooks for model deployment pipeline

## 📋 Key Achievements
- ✅ Deployed 5 interconnected servers on OpenStack infrastructure
- ✅ Achieved 100% automated deployment (0 to running in <10 minutes)
- ✅ Implemented secure SSH tunneling for Flask app access
- ✅ Created CI/CD pipeline for ML model updates

## 🚀 Quick Start

### Prerequisites
```bash
# Source your OpenStack credentials
source openrc_albin.sh
```
## Deploy Servers
```bash
./start_servers.sh
```
## Delete Servers
```bash
./delete_servers.sh
```
## 📁 Project Structure
```
├── start_instances.py      # Main OpenStack deployment script
├── start_servers.sh        # Server launch script
├── delete_servers.sh       # Server cleanup script
├── ansible/                # Configuration management
├── cloud-config/           # Cloud-init configurations
├── development_server/     # Dev environment
└── production_server/      # Prod environment
```
## 🔧 Technical Challenges Solved
Secret Management: Implemented .gitignore strategy to prevent credential leakage

Cross-Platform Automation: Adapted scripts for both Linux and Windows

Network Configuration: Automated floating IP assignment and SSH proxy jumping

## 📫 Connect With Me
GitHub: eranganana

LinkedIn: https://www.linkedin.com/in/achini-eranga-nanayakkara/

Email: erangananayakkara@yahoo.com

## 📚 Course Context
This was a group project for Data Engineering course at Uppsala University.

For detailed setup instructions, see course documentation.
