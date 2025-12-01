#include <stdio.h> //biblioteca para funções de entrada e saída

// Constantes simbólicas de login
#define MAX_EMAIL 100
#define MAX_SENHA 30
#define MAX_TIPO 20

// Estrutura para armazenar os dados de login do usuário
typedef struct {
    char email[MAX_EMAIL];
    char senha[MAX_SENHA];
    char tipo[MAX_TIPO];
} Usuario;

// Função para salvar os usuários no arquivo CSV
void salvar_usuario_csv(FILE *arquivo, Usuario *usuario) {
     fprintf(arquivo,
     "\"%s\",\"%s\",\"%s\"\n",
     usuario->email, usuario->senha, usuario->tipo);
}

// Início do escopo
int main() {
    // Gera o arquivo que armazena os dados dos usuários
    FILE *arquivo = fopen("usuario_dados.csv", "w");

    // Tratamento caso a criação do arquivo não funcione
    if (arquivo == NULL) {
        printf("Erro ao criar o arquivo!\n");
        return 1;
    }

    // Cadastro de dados do usuário Administrador
    Usuario usuario_cadastrado[] = {
          {"administrador@escola.com", "123", "Administrador"}
    };

    // Calcula a quantidade de usuários cadastrados em 'usuarios'
    int num_usuario = sizeof(usuario_cadastrado) / sizeof(Usuario);

    // Percorre cada usuário cadastrado lido acima
    for (int i = 0; i < num_usuario; i++) {

        // Chama a função que grava os dados do usuário atual no arquivo CSV
        salvar_usuario_csv(arquivo, &usuario_cadastrado[i]);
    }

    // Fecha o arquivo e mostra a mensagem de sucesso
    fclose(arquivo);
    printf("Arquivo 'usuario_dados.csv' gerado com sucesso.\n");


    //Gera o arquivo que armazena os dados acadêmicos dos usuários
    FILE *arquivo_dados = fopen("dados_academicos.csv", "w");

    //Tratamento caso a criação do arquivo não funcione
    if (arquivo_dados == NULL) {
        printf("Erro ao criar o arquivo de dados acadêmicos!\n");
        return 1;
    }

    //Fecha o arquivo e mostra a mensagem de sucesso
    fclose(arquivo_dados);
    printf("Arquivo 'dados_academicos.csv' vazio gerado com sucesso.\n");

    return 0;
}
