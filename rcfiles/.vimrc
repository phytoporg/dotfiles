set ai
syntax on
set nu!
set rnu!
set ts=4
set sw=4
set et
%retab!

set hlsearch

set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

" Airline
Plugin 'vim-airline/vim-airline'
Plugin 'vim-airline/vim-airline-themes'
Plugin 'dylanaraps/wal.vim'
"Plugin 'Valloric/YouCompleteMe'
Plugin 'bogado/file-line'
Plugin 'scrooloose/nerdtree'
Plugin 'joe-skb7/cscope-maps'
Plugin 'junegunn/fzf'
Plugin 'liuchengxu/vim-clap'
Plugin 'honza/vim-snippets'

if !has('nvim')
    Plugin 'tpope/vim-fugitive'
    Plugin 'SirVer/ultisnips'
endif

if has('nvim')
    Plugin 'neovim/nvim-lspconfig'
    Plugin 'neoclide/coc.nvim'
endif

" Syntax highlighting
Plugin 'petrbroz/vim-glsl'

" SNIPPETS
" Trigger configuration. Do not use <tab> if you use
" https://github.com/Valloric/YouCompleteMe.
let g:UltiSnipsExpandTrigger="<tab>"
let g:UltiSnipsJumpForwardTrigger="<c-b>"
let g:UltiSnipsJumpBackwardTrigger="<c-z>"

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line

color wal
let g:airline_powerline_fonts = 1
let g:airline_theme='powerlineish'

set colorcolumn=100

" For vim-go
let g:go_bin_path = $GOBIN
