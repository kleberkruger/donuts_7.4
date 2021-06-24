#
# Script para excluir os experimentos versão 1 de PiCL (com on-chip undo buffer infinito)
# e mover os da versão 2 para o caminho correto.
#

for app in *
do
    if [ -d "$app" ]; then
        base_path=$app/base
        pikl_path=$app/pikl

        find $base_path -mindepth 1 -name v2 -prune -o -exec rm -rf {} \;
        find $pikl_path -mindepth 1 -name v2 -prune -o -exec rm -rf {} \;

        mv $base_path/v2/* $base_path
        mv $pikl_path/v2/* $pikl_path

        rm -rf $base_path/v2
        rm -rf $pikl_path/v2

        mv $pikl_path $app/picl
    fi
done
