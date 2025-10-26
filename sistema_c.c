#include <stdio.h> //biblioteca para funções de entrada e saída

//Constantes simbólicas de login aluno
#define MAX_TIPO 20
#define MAX_EMAIL 100
#define MAX_SENHA 30

typedef struct {
    char tipo[MAX_TIPO];
    char email[MAX_EMAIL];
    char senha[MAX_SENHA];
} Usuario;

void salvar_usuario_csv(FILE *arquivo, Usuario *usuario) {
     fprintf(arquivo,
     "\"%s\",\"%s\",\"%s\n",
     usuario->tipo, usuario->email, usuario->senha
     );
}

int main() {
    FILE *arquivo = fopen("usuario_dados.csv", "w");
    if (arquivo == NULL) {
        printf("Erro ao criar o arquivo!\n");
        return 1;
    }

    Usuario usuario_cadastrado[] = {
          {
            "Administrador", "administrador@escola.com", "123"
          }
};

    int num_usuario = sizeof(usuario_cadastrado) / sizeof(Usuario);

    for (int i = 0; i < num_usuario; i++) {
        salvar_usuario_csv(arquivo, &usuario_cadastrado[i]);
    }

    fclose(arquivo);
    printf("Arquivo 'usuario.dados.csv' gerado com sucesso.\n");
    return 0;
}
