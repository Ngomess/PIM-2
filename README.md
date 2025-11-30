# Sistema de Gerenciamento Acadêmico
O Sistema de Gerenciamento Acadêmico é um projeto desenvolvido pelo nosso grupo, unindo a linguagem C para criação e manipulação de arquivos com o auxílio da interface gráfica feita em Python.
A proposta é criar uma aplicação simples, funcional e intuitiva para auxiliar no cadastro e gerenciamento de dados acadêmicos.

## Sobre o projeto
O sistema é dividido em duas partes principais:

**Estrutura em C:** Responsável por gerar e estruturar os arquivos-base do sistema.
  O programa cria dois arquivos CSV essenciais:

- usuario_dados.csv — contém usuários pré-cadastrados (administrador).

- dados_academicos.csv — criado vazio, para ser preenchido posteriormente.

Essa parte garante padronização, organização e segurança na formatação dos dados.


**Interface em Python:** Após gerar os arquivos iniciais, o Python é usado para criar a interface visual do sistema, permitindo que diferentes usuários interajam de forma intuitiva.
O usuário pode:
- Navegar entre menus específicos para Administrador, Professor ou Aluno;
- Cadastrar novos usuários;
- Registrar ou consultar informações acadêmicas;
- Visualizar e atualizar os arquivos CSV em tempo real.

## Funcionalidades
- Tela de login;
- Diferentes menus de acesso (Administrador / Professor / Aluno);
- Cadastro de usuários;
- Registro de notas;
- Consulta e edição de dados acadêmicos;
- Integração total com arquivos CSV;
- Estrutura inicial dos arquivos criada em C.

## Tecnologias utilizadas
**Utilizando C:**
- Manipulação de arquivos (CSV)
- Estruturas (struct)
- Escrita formatada (fprintf)
- Lógica inicial do sistema


**Utilizando Python:**
- Tkinter ou PySimpleGUI (interface gráfica)
- Módulo CSV
- Organização de telas e menus
- Leitura e escrita dos arquivos gerados pelo C

## O que aprendemos
Este projeto nos permitiu:
- Integrar duas linguagens diferentes dentro de um mesmo sistema;
- Trabalhar com estruturas e arquivos em C;
- Criar interfaces gráficas funcionais em Python;
- Aplicar boas práticas de organização e modularização;
- Desenvolver versionamento e colaboração usando Git e GitHub.
