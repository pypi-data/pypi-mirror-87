# py-dirk

dirk is a tool for Kubernetes administrators who manage a large number of clusters. 
dirk makes sure that you always communicate with the right kubernetes cluster, even though you switch between many project folders.

py-dirk is the Python implementation of dirk.

# Install py-dirk

Install py-dirk like this:

```bash
pip install py-dirk
```

# Use dirk

Init dirk for a certain project folder like this:

```bash
dirk init <directory>
```

This command creates a kubeconfig file which will be used by kubectl as long your current working directory is in the project folder.
Leaving the project folder will lead to the kubeconfig file to be unloaded.

# Example of use

1. Install dirk and minikube.
2. Run `example/build_example.sh`.
3. Change to `example/foo`, run 
   ```bash
   minikube start -p foo 
   ```
   and get the node of the minikube cluster
   ```bash
   kubectl get nodes 
   ```   
4. Change to `example/bar`, run 
   ```bash
   minikube start -p bar
   ```
   and get the node of the minikube cluster
   ```bash
   kubectl get nodes 
   ```   
5. Change to `example/foo` again and get the node
   ```bash
   minikube start -p foo
   ```
   As you can see, changing the directory changes the kubeconfig file which is used by kubectl.
 