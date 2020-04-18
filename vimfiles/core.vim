function! VisualSearch(direction)
    let l:register=@@
    normal! gvy
    let l:search=escape(@@, '$.*/\[]')
    if a:direction=='/'
        execute 'normal! /'.l:search
    else
        execute 'normal! ?'.l:search
    endif
    let @/=l:search
    normal! gV
    let @@=l:register
endfunction

set lazyredraw
set ignorecase
set visualbell
set noerrorbells

let mapleader=" "
let @a = "text"

noremap <C-e> 7<C-e>
noremap <leader>e 7<C-e>

noremap <C-y> 7<C-y>
noremap <leader>y 7<C-y>

noremap <leader>f <C-f>
noremap <leader>b <C-b>

noremap <leader>sa :action $SelectAll<CR>
noremap <leader>goto :action GotoLine<CR>

noremap <leader>m M
noremap <leader><leader>4 $
noremap <leader>tt :action ParameterInfo<CR>
noremap <leader>te :action ShowErrorDescription<CR>

noremap <leader>js o```js<enter>```<esc>O
noremap <leader>fs o```fs<enter>```<esc>O




noremap <leader>vv V

"" noremap y j
noremap <leader>y y
"" noremap Y j
noremap <leader>Y Y
vnoremap d j
vnoremap <leader>d d

noremap <leader>1 "zy
noremap <leader>2 "zY
noremap <leader>3 "zp
noremap <leader>4 "zd

noremap <leader>nm ggcenamespace<esc>Eviw"mxxo<esc>omodule <esc>"mpa =<esc>o()<esc>>>

noremap <leader><leader>' i````<Esc>hi
inoremap <leader><leader>' ````<Esc>hi

noremap <leader><leader>/ i／
inoremap <leader><leader>/ ／

nnoremap <leader>[ ?let <CR>:noh<CR>
nnoremap <leader>] /let <CR>:noh<CR>

noremap <leader>rr :action Rerun<CR>
noremap <leader>ru :action Run<CR>
noremap <leader>rs :action Stop<CR>
noremap <leader>rc :action RunConfiguration<CR>

noremap <leader>cn :action CloseAllNotifications<CR>
noremap <leader>co :action CloseAllEditorsButActive<CR>



noremap <leader>ne :action GotoNextError<CR>
noremap <leader>pe :action GotoPreviousError<CR>

noremap <leader>no :action NextOccurence<CR>
noremap <leader>po :action PreviousOccurence<CR>

noremap Q /
noremap <space>Q ?
noremap / j
noremap ? j

nmap <leader>nc G Q(FlukeDate.Cr<CR> 2 3O<CR>comment """<esc>j$bcw<esc>O<esc><<<<<<j$i
nmap <leader>nd G QflukeDate <CR> 2$%p<esc>o]<esc>k$bb

if env ==? "sh"

	nnoremap <c-right> gt
	nnoremap <c-left> gT

	nnoremap <silent><esc><esc> :noh<CR>

	nnoremap <leader>w /[A-Z]<CR>h:noh<CR>
	nnoremap <leader>W /[A-Z]<CR>:noh<CR>
	vnoremap <leader>w /[A-Z]<CR>h
    vnoremap <leader>W /[A-Z]<CR>

	vnoremap <silent>* <ESC>:call VisualSearch('/')<CR>/<CR>
	vnoremap <silent># <ESC>:call VisualSearch('?')<CR>?<CR>

elseif env ==? "idea"

    noremap <leader>w ]w
    noremap <leader>W [w

endif













nnoremap <c-[> j
nnoremap <c-]> j
nnoremap <c-\> j
nnoremap <c-s-[> k
nnoremap <c-s-]> k
nnoremap <c-s-\> k

nnoremap ; j
nnoremap <c-;> j
nnoremap <c-s-;> j

nnoremap <leader>< k
nnoremap <leader>> j
nnoremap <leader>- k
nnoremap <leader>= j




nnoremap ! j
nnoremap <t	ab> j
nnoremap <s-tab> j
nnoremap <s-f1> j
nnoremap <s-f5> j
nnoremap <c-k> j
nnoremap ,d j
nnoremap <leader><leader> j
nnoremap <leader>4 j
nnoremap <leader>j j
nnoremap <leader>J k

