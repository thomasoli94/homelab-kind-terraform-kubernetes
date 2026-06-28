# homelab k8s

Homelab local para estudar Kubernetes usando kind, Ansible e manifests Kubernetes.

O projeto provisiona a toolchain base, cria um cluster kind multi-node e inclui uma aplicacao Flask de demonstracao com ConfigMap, Secret, Deployment, probes e Service.

## Estrutura

```text
.
+-- ansible/
|   +-- site.yml
|   +-- 01-tooling.yml
|   +-- 02-cluster.yml
|   +-- group_vars/all.yml
|   +-- templates/kind-config.yaml.j2
+-- apps/
|   +-- app-demo/
|       +-- app.py
|       +-- Dockerfile
|       +-- requirements.txt
+-- kubernetes/
    +-- app-demo/
        +-- 00-namespace.yaml
        +-- 01-configmap.yaml
        +-- 02-secret.yaml
        +-- 03-deployment.yaml
        +-- 04-service.yaml
```

## O que este repo cria

- Tooling local: `kubectl`, `kind`, `helm`, `terraform`, `jq` e utilitarios base.
- Cluster kind chamado `homelab`.
- Topologia padrao: 1 control-plane e 2 workers.
- Aplicacao demo em Flask exposta internamente por um Service `ClusterIP`.

## Pre-requisitos

- Linux ou WSL2.
- Docker instalado e rodando.
- Ansible instalado.
- Usuario com permissao para executar tarefas com `sudo`.

## Provisionar o homelab

Execute a partir da pasta `ansible`:

```bash
cd ansible
ansible-playbook site.yml
```

O playbook `site.yml` executa, em ordem:

1. `01-tooling.yml`: instala as ferramentas locais.
2. `02-cluster.yml`: cria o cluster kind usando o template `kind-config.yaml.j2`.

As variaveis principais ficam em `ansible/group_vars/all.yml`:

```yaml
cluster_name: homelab
worker_count: 2
bin_dir: /usr/local/bin
```

## Aplicacao demo

A aplicacao fica em `apps/app-demo` e escuta na porta `8080`.

Endpoints:

- `/`: retorna informacoes do pod, ambiente e versao.
- `/health`: endpoint de liveness.
- `/ready`: endpoint de readiness.
- `/break`: simula falha no liveness probe.

Para construir a imagem local:

```bash
docker build -t app-demo:1.0.0 apps/app-demo
```

Para carregar a imagem no cluster kind:

```bash
kind load docker-image app-demo:1.0.0 --name homelab
```

Para aplicar os manifests:

```bash
kubectl apply -f kubernetes/app-demo/
```

Para testar via port-forward:

```bash
kubectl -n app-demo port-forward svc/app-demo 8080:80
```

Em outro terminal:

```bash
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/ready
```

## Comandos uteis

```bash
kind get clusters
kubectl get nodes
kubectl -n app-demo get all
kubectl -n app-demo describe deploy app-demo
kubectl -n app-demo logs -l app=app-demo
```

## Observacoes

O arquivo `kubernetes/app-demo/02-secret.yaml` usa um token fake apenas para fins de laboratorio. Nao armazene segredos reais em manifests versionados.
