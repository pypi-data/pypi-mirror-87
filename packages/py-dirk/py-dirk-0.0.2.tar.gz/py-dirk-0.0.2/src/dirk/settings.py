ENVRC_FILENAME = '.envrc'
KUBECONFIG_FILENAME = 'kubeconfig'
EXPORT_KUBECONFIG = 'export KUBECONFIG=\"$(pwd)/{kubeconfig}\"'.format(
    kubeconfig=KUBECONFIG_FILENAME
)