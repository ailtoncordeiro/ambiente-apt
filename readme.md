# Provisionamento de Ambiente Experimental na Google Cloud com Terraform

Este projeto utiliza Terraform para provisionar um ambiente experimental na Google Cloud, composto por:

- **Rede Virtual (VPC) e Sub-rede:** Isolamento do ambiente.
- **Instâncias Windows:** Endpoints e Controlador de Domínio.
- **Instância de Ataque:** Máquina atacante (ex.: Kali Linux ou similar) com acesso SSH.
- **Regras de Firewall:** Para acesso via RDP (porta 3389) às instâncias Windows e SSH (porta 22) para a máquina atacante.

> **Observação:**  
> Este ambiente é destinado para fins de testes e simulação de cenários de APT (Ataques Persistentes Avançados). Utilize com cautela e garanta que esteja devidamente isolado.

## 1. Pré-requisitos

Antes de provisionar os recursos, verifique se os seguintes itens estão instalados e configurados:

- **Terraform:**  
  Baixe e instale o Terraform em: [Terraform Downloads](https://www.terraform.io/downloads)

- **Google Cloud SDK:**  
  Instale o SDK do Google Cloud e autentique-se:
  ```bash
  gcloud auth application-default login
  ```

## 2. Estrutura do projeto

O Projeto contém os seguintes arquivos no diretório Terraform:

- **main.tf:**  
  Define a infraestrutura: VPC, sub-rede, instâncias e regras de firewall.

- **variables.tf:**  
  Declara as variáveis utilizadas, como project_id, region e zone.
    
- **outputs.tf:**  
  Define as saídas, por exemplo, os IPs públicos das instâncias provisionadas.

## 3. Provisionamento da Infraestrutura

> **Observação:**  
> No terminal, navegue até o diretório Terraform, do projeto, e em seguida digite os comandos.

### 3.1 Inicializar o terraform

```bash
  terraform init
```

### 3.2 Visualizar o plano de execução

```bash
  terraform init
```

### 3.3 Provisionar os recursos

```bash
  terraform apply
```

### 3.4 Verificar as saídas

```bash
  terraform output
```

## 4. Comandos Adicionais

Refazer o plano após alterações

```bash
  terraform plan -var="project_id=SEU_PROJECT_ID"
```

Destruir os recursos provisionados

```bash
  terraform destroy
```