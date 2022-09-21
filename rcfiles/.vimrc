set ai
syntax on
set nu
set rnu
set ts=4
set sw=4
set et
set completeopt-=preview
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
Plugin 'bogado/file-line'
Plugin 'tikhomirov/vim-glsl'
Plugin 'junegunn/fzf'
Plugin 'junegunn/fzf.vim'
Plugin 'fidian/hexmode'
Plugin 'vimwiki/vimwiki'
Plugin 'preservim/nerdtree'
Plugin 'kyazdani42/nvim-tree.lua'
Plugin 'williamboman/mason.nvim'
Plugin 'williamboman/mason-lspconfig.nvim'
Plugin 'neovim/nvim-lspconfig'
Plugin 'mfussenegger/nvim-dap'
Plugin 'nvim-treesitter/nvim-treesitter'
Plugin 'Badhi/nvim-treesitter-cpp-tools'
Plugin 'ms-jpq/coq_nvim'

" fugitive.vim - A Git wrapper so awesome, it should be illegal
" Fugitive has its own VCS status indicator, but Airline already
" gives that to you.
Plugin 'tpope/vim-fugitive'
" rhubarb gives Github specific features like
" - <C-x><C-o> completion in fugitive commit messages for issue numbers
" - Provider for fugitive's Gbrowse command
Plugin 'tpope/vim-rhubarb'

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

" Disable by default, but keep this here in case it's occasionally useful
" set colorcolumn=80

let mapleader = ","

" Some general binds
noremap <C-A-h> :vertical resize +5<CR>
noremap <C-A-l> :vertical resize -5<CR>
noremap <C-A-k> :resize -1<CR>
noremap <C-A-j> :resize +1<CR>

" Clangd binds
" switch between header and implementation file
noremap <C-k><C-o> :ClangdSwitchSourceHeader<Enter>

" FZF binds
noremap <S-p> :FZF<Enter>

" Fugitive binds
" Basically chords with <leader> to ohmyzsh git binds

noremap <leader>gpl :Gpull<Enter>
noremap <leader>gph :Gpush<Enter>
noremap <leader>gph :Gpush<Enter>
" Opens Git link for selected line or region in browser
noremap <leader>gb  :Gbrowse<Enter>
" Adding hunks with :Gstatus - https://vi.stackexchange.com/a/21410
"  - Press "=" on an file (shows git diff)
"  - Press "-" on a hunk or visual selection to stage/unstage
"  - "cvc" to commit verbosely
noremap <leader>gs  :Gstatus<Enter>
