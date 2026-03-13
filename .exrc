" SpeciesExplorer project configuration for Neovim
" See .nvim.lua for full configuration with WhichKey shortcuts

" Python settings
set tabstop=4
set shiftwidth=4
set expandtab
set colorcolumn=120

" File associations
autocmd BufRead,BufNewFile *.qml set filetype=xml
autocmd BufRead,BufNewFile *.ui set filetype=xml
autocmd BufRead,BufNewFile metadata.txt set filetype=dosini

" Project-local settings
set path+=species_explorer/**
set path+=test/**
