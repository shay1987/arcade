# Arcade

![Arcade Logo](logo.png)

Arcade is a repository that contains a collection of classic TUI arcade games implemented using bash script and ttyd.
These games are recreated to provide a nostalgic gaming experience for users, whether you're a seasoned gamer or just looking for some fun, `Arcade` has something for everyone.

## Project Overview

Arcade is not only a collection of classic arcade games but also serves as a Continuous Integration and Continuous Deployment (CI/CD) project.  
It incorporates various technologies and tools to demonstrate a complete CI/CD pipeline.  
The project utilizes the following components:

### Docker

Docker is a key component in this project, providing containerization for the game.  
The game is encapsulated within a Docker container, ensuring portability, consistency, and easy deployment across different environments.

### Docker Compose
Docker Compose is utilized to define and run multi-container Docker applications.  
It allows for the configuration of all application's services (like the MySQL database, Login App, Arcade App, and Nginx proxy) in a single `docker-compose.yaml` file, simplifying their orchestration and local development setup.

### Minikube

Minikube, a tool for running Kubernetes locally, is employed in this project to orchestrate the deployment and management of the game's infrastructure. It allows for the creation of a local Kubernetes cluster, providing a platform to host and scale the game containers.

### Python Login App with MySQL

Arcade repository includes a Python login app that connects to a MySQL database. This showcases the integration between Python and a database system, allowing users to register and log in to the games app.

## Games Included

The following arcade games are included in this repository:

1. Bastet
2. Ninvaders
3. Snake
4. Greed
5. Pacman

More games will be available in future releases.

## How to Run locally

Follow these steps to run **only the Arcade game** locally using a direct Docker command:

1.  Open a terminal or command prompt and run the following command:
    ```bash
    docker run -p 7681:7681 shay1987/arcade
    ```
2.  Open your browser and enter 'localhost:7681'
3.  Enjoy playing the games!

## How to Run Locally with Docker Compose

Follow these steps to run the **complete application stack** (MySQL, Login App, Arcade App, Nginx Proxy) locally using Docker Compose:

1.  **Ensure Docker and Docker Compose are Installed:**
    Make sure you have Docker and Docker Compose installed on your system. If not, you can use the `install_applications.sh` script provided in the root of this repository.

2.  **Navigate to the Docker Compose Directory:**
    Open your terminal or command prompt and change your current directory to the `docker-compose` folder, as your `docker-compose.yaml` is located there:
    ```bash
    cd docker-compose
    ```

3.  **Start the Services:**
    Run the following command to build the necessary images (if they don't exist or have been updated) and start all services in detached mode (`-d`):
    ```bash
    docker-compose up --build -d
    ```
    * **Troubleshooting Tip:** If you encounter any issues with existing containers (e.g., "Conflict. The container name is already in use"), you can clean up thoroughly by running:
        ```bash
        docker-compose down --remove-orphans
        docker-compose up --build -d
        ```

4.  **Access the Applications:**
    Once all services are up and running (this might take a minute, especially for MySQL to become healthy):
    * **Login Application:** Open your web browser and go to `http://localhost/`
    * **Arcade Games:** After (or without, depending on your `login-app`'s configuration for direct access) logging in via the Login App, you can access the arcade games by navigating to `http://localhost/arcade/` (or `http://localhost/arcade`).

5.  **Stop the Services:**
    When you're done, you can stop and remove all services defined in `docker-compose.yaml` by running the following command from within the `docker-compose` directory:
    ```bash
    docker-compose down
    ```

## How to Deploy to Kubernetes Cluster (using `kubectl apply`)

To deploy this application suite (MySQL, Login App, Arcade Game) to a Kubernetes cluster using individual YAML files, follow these steps.
Ensure you have `kubectl` configured to interact with your cluster.

1.  **Enable Ingress Controller (if using Minikube or a similar local setup):**
    If you're deploying on Minikube, ensure the Ingress addon is enabled:
    ```bash
    minikube addons enable ingress
    ```

2.  **Deploy MySQL Database:**
    This file defines the MySQL Secret, Persistent Volume Claim, ConfigMap, Deployment, and Service.
    ```bash
    kubectl apply -f mysql.yaml
    ```
    *It's good practice to wait for the MySQL pod to be `Running` and `Ready` before proceeding:*
    ```bash
    kubectl get pods -l app=mysql
    ```

3.  **Deploy Login Application:**
    This deploys the Flask Login application's Deployment and Service.
    ```bash
    kubectl apply -f login.yaml
    ```
    *Wait for the Login pod to be `Running` and `Ready`.*
    ```bash
    kubectl get pods -l app=login
    ```

4.  **Deploy Login Static Files Ingress:**
    This Ingress routes requests for static assets (`/static/`) to your login application.
    ```bash
    kubectl apply -f login-static-ingress.yaml
    ```

5.  **Deploy Arcade Game:**
    This deploys the Arcade game application's Deployment and Service.
    ```bash
    kubectl apply -f arcade_game/deployment.yaml
    ```
    *Wait for the Arcade pod to be `Running` and `Ready`.*
    ```bash
    kubectl get pods -l app=arcade
    ```

6.  **Deploy Arcade Game Ingress:**
    This Ingress exposes the Arcade game externally, including WebSocket support.
    ```bash
    kubectl apply -f arcade-ingress.yaml
    ```

7.  **Access the Applications:**
    After all resources are deployed and running, you can access your applications via the Ingress controller's external IP or hostname.

    * **Find Ingress IP/Hostname:**
        If on Minikube, get the Ingress IP:
        ```bash
        minikube ip
        ```
        If on a cloud provider, check your Ingress controller's external IP or hostname (e.g., using `kubectl get ingress -A -o wide`).

    * **Access Login:** Open your browser to `http://<YOUR_INGRESS_IP_OR_HOSTNAME>/` (or `http://yourdomain.com/` if you configured a hostname in Ingress).
    * **Access Arcade:** After a successful login through the Login app, you will be redirected to the Arcade game, which will be accessible at `http://<YOUR_INGRESS_IP_OR_HOSTNAME>/arcade` (or `http://yourdomain.com/arcade`).

## How to Deploy to Kubernetes Cluster with Helm

To deploy the complete application suite (MySQL, Login App, Arcade Game) to a Kubernetes cluster using the provided Helm chart, follow these steps.

**Prerequisites:**
* A running Kubernetes cluster (e.g., Minikube).
* `kubectl` configured to interact with your cluster.
* Helm v3+ installed.
* If using Minikube, ensure the Ingress addon is enabled:
    ```bash
    minikube addons enable ingress
    ```

**Deployment Steps:**

1.  **Navigate to the Helm Chart Directory:**
    Open your terminal or command prompt and change your current directory to the `helm-chart/arcade` folder where your `Chart.yaml` is located.
    ```bash
    cd helm-chart/arcade
    ```

2.  **Lint the Chart (Optional, but Recommended):**
    Before deploying, it's good practice to lint your Helm chart to check for syntax errors and best practices:
    ```bash
    helm lint .
    ```

3.  **Install the Chart:**
    This command will deploy all components (MySQL, Login App, Arcade App, Ingresses) defined in your Helm chart.
    ```bash
    helm install my-arcade-release . --wait
    ```
    * Replace `my-arcade-release` with a name for your deployment.
    * The `--wait` flag ensures Helm waits until all resources are in a ready state.

4.  **Upgrade the Chart (for subsequent deployments/changes):**
    If you make changes to your chart (templates or `values.yaml`), use `helm upgrade` to apply them.
    ```bash
    helm upgrade my-arcade-release . --wait
    ```

5.  **Verify Deployment:**
    You can check the status of all deployed resources:
    ```bash
    kubectl get all -l app.kubernetes.io/instance=my-arcade-release
    kubectl get ingress -l app.kubernetes.io/instance=my-arcade-release
    ```

6.  **Access the Applications:**
    Once all resources are deployed and running, you can access your applications via the Ingress controller's external IP or hostname.

    * **Find Ingress IP/Hostname:**
        If on Minikube, get the Ingress IP:
        ```bash
        minikube ip
        ```
        If on a cloud provider, check your Ingress controller's external IP or hostname (e.g., using `kubectl get ingress -A -o wide`).

    * **Access Login:** Open your browser to `http://<YOUR_INGRESS_IP_OR_HOSTNAME>/` (or `http://yourdomain.com/` if you configured a hostname in Ingress).
    * **Access Arcade:** After a successful login through the Login app, you will be redirected to the Arcade game, which will be accessible at `http://<YOUR_INGRESS_IP_OR_HOSTNAME>/arcade` (or `http://yourdomain.com/arcade`).

## Contributing

Contributions to this repository are welcome! If you'd like to add more games or improve existing ones, feel free to create a pull request with your changes. Make sure to follow the existing code style and include any necessary documentation or assets.

## License

The code in this repository is licensed under the MIT License. You can find more information in the [LICENSE](LICENSE) file.

## Acknowledgements

This repository is based on the work by [shay1987](https://github.com/shay1987). Thank you for creating and sharing these classic arcade game implementations.

If you have any questions or encounter any issues, please don't hesitate to [open an issue](https://github.com/shay1987/Arcade/issues). We hope you enjoy playing these arcade games!