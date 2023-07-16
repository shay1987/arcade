# Arcade

![Arcade Logo](logo.png)

Arcade is a repository that contains a collection of classic TUI arcade games implemented using bash script and ttyd. These games are recreated to provide a nostalgic gaming experience for users. Whether you're a seasoned gamer or just looking for some fun, Arcade has something for everyone.

## Project Overview

Arcade is not only a collection of classic arcade games but also serves as a Continuous Integration and Continuous Deployment (CI/CD) project. It incorporates various technologies and tools to demonstrate a complete CI/CD pipeline. The project utilizes the following components:

### Docker

Docker is a key component in this project, providing containerization for the game. The game is encapsulated within a Docker container, ensuring portability, consistency, and easy deployment across different environments.

### Minikube

Minikube, a tool for running Kubernetes locally, is employed in this project to orchestrate the deployment and management of the game's infrastructure. It allows for the creation of a local Kubernetes cluster, providing a platform to host and scale the game containers.

### Python Login App with MySQL

Arcade repository includes a Python login app that connects to a MySQL database. This showcases the integration between Python and a database system, allowing users to register and log in to the games app.

### HAProxy Load Balancer

To demonstrate load balancing capabilities, the project incorporates HAProxy as a load balancer. It distributes incoming requests across multiple game pods, ensuring efficient resource utilization and improved performance.

### Continuous Integration with GitHub Actions

The project embraces Continuous Integration practices by leveraging GitHub Actions. With GitHub Actions, automated workflows are set up to build, and Push the Docker image every time changes are pushed to the repository. This ensures that each commit is verified and helps maintain code quality.

### Continuous Deployment with Argo CD

For Continuous Deployment, the project integrates Argo CD, a GitOps-based continuous delivery tool. Argo CD automates the deployment of the games by syncing the desired state defined in a Git repository with the target Kubernetes cluster, ensuring consistent and reliable deployments.

By incorporating these technologies and tools, the Arcade project showcases a complete CI/CD pipeline, enabling developers to efficiently develop, test, and deploy the games in a controlled and automated manner. It demonstrates best practices for modern software development and deployment workflows.

## Games Included

The following arcade games are included in this repository:

1. Bastet
2. Ninvaders
3. Snake
4. Greed
5. Pacman
6. Backgammon

More games will be available in future releases.

## How to Run locally

Follow these steps to run the app locally:

1. Open a terminal or command prompt and run the following command:
   ```
   docker run -p 7681:7681 shay1987/arcade
   ```
2. Open your browser and enter 'localhost:7681'  
3. Enjoy playing the games!

## Contributing

Contributions to this repository are welcome! If you'd like to add more games or improve existing ones, feel free to create a pull request with your changes. Make sure to follow the existing code style and include any necessary documentation or assets.

## License

The code in this repository is licensed under the MIT License. You can find more information in the [LICENSE](LICENSE) file.

## Acknowledgements

This repository is based on the work by [shay1987](https://github.com/shay1987). Thank you for creating and sharing these classic arcade game implementations.

If you have any questions or encounter any issues, please don't hesitate to [open an issue](https://github.com/shay1987/Arcade/issues). We hope you enjoy playing these arcade games!