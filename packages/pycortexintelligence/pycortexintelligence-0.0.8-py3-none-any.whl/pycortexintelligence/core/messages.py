VARIABLES_CREATED = 'VÁRIAVÉIS DE AMBIENTE RECUPERADAS COM SUCESSO!'
OS_PARAMS_CORRECT = 'TUDO INDICA QUE O OS_PARAMS ESTÁ CORRETO PARA O PROJETO!'
TEMP_DIRS = 'DIRETÓRIOS TEMPORÁRIOS CONFIGURADOS COM SUCESSO!'
TEMP_DIRS_EMPTY = 'DIRETÓRIOS TEMPORÁRIOS RESETADOS COM SUCESSO!'
EMAIL_PROJECT_ERROR_SUBJECT = 'Projeto: {} | Erro Encontrado'


def mail_variable_error(key):
    return "Tivemos um erro ao verificar as varíaveis de ambiente. \n A variável {} não foi encontrada.".format(key)
