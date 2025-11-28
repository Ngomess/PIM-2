#include <stdio.h>

#define MAX_EMAIL 100
#define MAX_SENHA 30
#define MAX_TIPO 20

typedef struct {
    char email[MAX_EMAIL];
    char senha[MAX_SENHA];
    char tipo[MAX_TIPO];
} Usuario;

void salvar_usuario_csv(FILE *arquivo, Usuario *usuario) {
     fprintf(arquivo,
     "\"%s\",\"%s\",\"%s\"\n",
     usuario->email, usuario->senha, usuario->tipo);
}

int main() {
    FILE *arquivo = fopen("usuario_dados.csv", "w");
    if (arquivo == NULL) {
        printf("Erro ao criar o arquivo!\n");
        return 1;
    }

    Usuario usuario_cadastrado[] = {
          {"administrador@escola.com", "123", "Administrador"}
    };

    int num_usuario = sizeof(usuario_cadastrado) / sizeof(Usuario);
    for (int i = 0; i < num_usuario; i++) {
        salvar_usuario_csv(arquivo, &usuario_cadastrado[i]);
    }

    fclose(arquivo);
    printf("Arquivo 'usuario_dados.csv' gerado com sucesso.\n");


    FILE *arquivo_dados = fopen("dados_academicos.csv", "w");
    if (arquivo_dados ==NULL) {
        printf("Erro ao criar o arquivo de dados acad�micos!\n");
        return 1;
    }

    fclose(arquivo_dados);
    printf("Arquivo 'dados_academicos.csv' vazio gerado com sucesso.\n");

    return 0;
}
