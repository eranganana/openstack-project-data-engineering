\# OpenStack Multi-Server Deployment for Data Engineering



\## Project Overview

Automated deployment of a complete data engineering infrastructure on OpenStack cloud, including production server, development server, and a 3-node Ray cluster for distributed computing.



\## My Role \& Contributions

\- \*\*Infrastructure as Code\*\*: Wrote Python scripts using Novaclient to automate OpenStack instance creation

\- \*\*Configuration Management\*\*: Created Ansible playbooks for server configuration

\- \*\*Cloud Automation\*\*: Implemented cloud-init user data for automated server setup

\- \*\*Security\*\*: Managed SSH keys, security groups, and sensitive data protection

\- \*\*CI/CD Setup\*\*: Configured Git hooks for model deployment pipeline



\## Technologies Used

\- \*\*OpenStack\*\* (Nova, Neutron, Keystone)

\- \*\*Python\*\* (Novaclient, OpenStack SDK)

\- \*\*Ansible\*\* (Configuration management)

\- \*\*Bash\*\* (Automation scripts)

\- \*\*Git\*\* (Version control)

\- \*\*Ray\*\* (Distributed computing cluster)



\## Architecture



\[User] → \[Jump Node] → \[Production Server]

→ \[Development Server]

→ \[Ray Cluster: Node1, Node2, Node3]





\## Key Achievements

\- Deployed 5 interconnected servers on OpenStack infrastructure

\- Achieved 100% automated deployment (from 0 to running in <10 minutes)

\- Implemented secure SSH tunneling for Flask app access

\- Created CI/CD pipeline for ML model updates



\## Technical Challenges Solved

1\. \*\*Secret Management\*\*: Implemented .gitignore strategy to prevent credential leakage

2\. \*\*Cross-Platform Automation\*\*: Adapted scripts for both Linux and Windows environments

3\. \*\*Network Configuration\*\*: Automated floating IP assignment and SSH proxy jumping



\## Live Demo

\[Add screenshot of working Flask app here]



\## Connect With Me

\- GitHub: \[eranganana]

\- LinkedIn: \[Your LinkedIn URL]

\- Email: \[Your email]



\## Course Context

\*This was a group project for \[Course Name] at \[University]. Full technical documentation below.\*

