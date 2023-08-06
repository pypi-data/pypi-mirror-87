# ConectividadeApp

## Version 0.0.29

### Know Issues

* **\#01** - Campo "MAC" em OldDevice limitado a 12 caracteres retorna erro se ultrapassar esse limite.

* **\#02** - Se nenhum "device" estiver cadastrado na base, o campo "Input the Device" ficará em branco e ao realizer uma requisição, um erro é retornado.

* **\#03** - Ao adicionar uma atividade de forma bem sucedida, o usuário é redirecionardo para conectividadeapp/addactivity/ com uma página em branco.

* **\#04** - Ao adicionar um ator, a mensagem de erro abaixo listada aparece, porém mesmo assim o item é adicionado ao banco:

    > Reverse for 'list' not found. 'list' is not a valid view function or pattern name..

### Fixed Issues
