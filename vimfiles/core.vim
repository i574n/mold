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
noremap <leader>ee 7<C-e>

noremap <C-y> 7<C-y>

noremap <leader>ff <C-f>
noremap <leader>bb <C-b>

if !exists('g:vscode')
    noremap <leader>sa :action $SelectAll<CR>
else
    noremap <leader>sa <Cmd>lua require('vscode-neovim').action('editor.action.selectAll')<CR>
endif

if !exists('g:vscode')
    noremap <leader>go :action GotoLine<CR>
else
    noremap <leader>go <Cmd>lua require('vscode-neovim').action('workbench.action.gotoLine')<CR>
endif

noremap <leader>m M
noremap <leader><leader>4 $

if !exists('g:vscode')
    noremap <leader>tt :action ParameterInfo<CR>
else
    noremap <leader>tt <Cmd>lua require('vscode-neovim').action('editor.action.showHover')<CR>
endif

if !exists('g:vscode')
else
    noremap <leader>fi <Cmd>lua require('vscode-neovim').action('actions.find')<CR>
    noremap <leader>fa <Cmd>lua require('vscode-neovim').action('workbench.action.findInFiles')<CR>
    noremap <leader>rd <Cmd>lua require('vscode-neovim').action('redo')<CR>
    noremap <leader>re <Cmd>lua require('vscode-neovim').action('editor.action.startFindReplaceAction')<CR>
    noremap <leader>ra <Cmd>lua require('vscode-neovim').action('workbench.action.replaceInFiles')<CR>
    noremap <leader>fn <Cmd>lua require('vscode-neovim').action('editor.action.nextMatchFindAction')<CR>
    noremap <leader>fsn <Cmd>lua require('vscode-neovim').action('editor.action.nextSelectionMatchFindAction')<CR>
    noremap <leader>su <Cmd>lua require('vscode-neovim').action('editor.action.inlineSuggest.trigger')<CR>
    noremap <leader>co <Cmd>lua require('vscode-neovim').action('editor.action.blockComment')<CR>
    noremap <leader>ins <Cmd>lua require('vscode-neovim').action('editor.action.inspectTMScopes')<CR>
    noremap <leader>cc <Cmd>lua require('vscode-neovim').action('editor.action.clipboardCopyAction')<CR>
    noremap <leader>vv <Cmd>lua require('vscode-neovim').action('editor.action.clipboardPasteAction')<CR>
    noremap <leader>th <Cmd>lua require('vscode-neovim').action('workbench.action.previousEditor')<CR>
    noremap <leader>tl <Cmd>lua require('vscode-neovim').action('workbench.action.nextEditor')<CR>
    noremap <leader>gh <Cmd>lua require('vscode-neovim').action('workbench.action.previousEditorInGroup')<CR>
    noremap <leader>gl <Cmd>lua require('vscode-neovim').action('workbench.action.nextEditorInGroup')<CR>
    noremap <leader>bf <Cmd>lua require('vscode-neovim').action('buildFile')<CR>
    noremap <leader>te <Cmd>lua require('vscode-neovim').action('workbench.action.terminal.toggleTerminal')<CR>
    noremap <leader>fsb <Cmd>lua require('vscode-neovim').action('workbench.action.focusSideBar')<CR>
    noremap <leader>ind <Cmd>lua require('vscode-neovim').action('editor.action.indentLines')<CR>
    noremap <leader>out <Cmd>lua require('vscode-neovim').action('editor.action.outdentLines')<CR>
    noremap <leader>qf <Cmd>lua require('vscode-neovim').action('editor.action.quickFix')<CR>
    noremap <leader>fd <Cmd>lua require('vscode-neovim').action('editor.action.formatDocument')<CR>
    noremap <leader>nb <Cmd>lua require('vscode-neovim').action('workbench.action.navigateBack')<CR>
    noremap <leader>nf <Cmd>lua require('vscode-neovim').action('workbench.action.navigateForward')<CR>
    noremap <leader>ma <Cmd>lua require('vscode-neovim').action('notebook.cell.insertMarkdownCellAbove')<CR>
    noremap <leader>mb <Cmd>lua require('vscode-neovim').action('notebook.cell.insertMarkdownCellAbove')<CR>
    noremap <leader>Th <Cmd>lua require('vscode-neovim').action('workbench.action.moveEditorLeftInGroup')<CR>
    noremap <leader>Tl <Cmd>lua require('vscode-neovim').action('workbench.action.moveEditorRightInGroup')<CR>
    noremap <leader>TH :lua for i=1,100 do require('vscode-neovim').action('workbench.action.moveEditorLeftInGroup') end<CR>
    noremap <leader>TL :lua for i=1,100 do require('vscode-neovim').action('workbench.action.moveEditorRightInGroup') end<CR>



    noremap <leader>rc :let @+ = @a<CR>
    "" nmap <leader>sn Q\C[A-Z]<CR>vu:normal i_<CR>

    "" nmap <leader>sn Q\C[A-Z]<CR>vuvyphr_:noh<CR>

    "" nmap <leader>sn f\C[A-Z]<CR>vuvyphr_:noh<CR>
    "" nmap <leader>sn Q\C[A-Z]<CR>vuvyphr_:noh<CR>
    "" nmap <leader>sn :find \C[A-Z]<CR>vuvyphr_<CR>

    "" nmap <leader>sn :s/\C[A-Z]/_\L\0\E/<CR>

    "" nmap <leader>sn Q\C[A-Z]<CR>vuvyphr_<Cmd>lua require('vscode-neovim').call('_ping')<CR>

    "" nmap <leader>sn :s/\C[A-Z]/_\L\0\E/<CR><Cmd>lua require('vscode-neovim').call('_ping')<CR>

    nmap <leader>sn :s/\(\C[A-Z]\)/_\L\1\E/g<CR>

    "" nmap <leader>sn :call search('\C[A-Z]')<CR>vuvyphr_

    "" nmap <leader>sn :let @n=":s/\\C[A-Z]/_\\L\\0\\E/<C-v><CR>"<CR>@n

    "" nmap <leader>sn :let @n="Q\C[A-Z]<C-v><CR>"<CR>@nvuvyphr_


endif


"" noremap <leader>te :action ShowErrorDescription<CR>

noremap <leader>bl o```<enter>```<esc>O


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

noremap <leader>gl Olet getLocals () = $"0={0} {getLocals ()}"<Esc>0jw
noremap <leader>nm ggcenamespace<esc>Eviw"mxxo<esc>omodule <esc>"mpa =<esc>o()<esc>>>

noremap <leader><leader>' i````<Esc>hi
inoremap <leader><leader>' ````<Esc>hi



"" noremap <leader><leader>/ i／
"" inoremap <leader><leader>/ ／

nnoremap <leader>[ ?let <CR>:noh<CR>
nnoremap <leader>] /let <CR>:noh<CR>

noremap <leader>rr :action Rerun<CR>
noremap <leader>ru :action Run<CR>
noremap <leader>rs :action Stop<CR>
noremap <leader>rc :action RunConfiguration<CR>

noremap <leader>cn :action CloseAllNotifications<CR>
noremap <leader>co :action CloseAllEditorsButActive<CR>



if !exists('g:vscode')
    noremap <leader>ne :action GotoNextError<CR>
else
    noremap <leader>ne <Cmd>lua require('vscode-neovim').action('editor.action.marker.next')<CR>
    noremap <leader>nE <Cmd>lua require('vscode-neovim').action('editor.action.marker.nextInFiles')<CR>
endif

if !exists('g:vscode')
    noremap <leader>pe :action GotoPreviousError<CR>
else
    noremap <leader>pe <Cmd>lua require('vscode-neovim').action('editor.action.marker.prev')<CR>
    noremap <leader>pE <Cmd>lua require('vscode-neovim').action('editor.action.marker.prevInFiles')<CR>
endif


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

	nnoremap <leader>w /\C[A-Z_]<CR>h:noh<CR>
	nnoremap <leader>W /\C[A-Z_]<CR>:noh<CR>
	vnoremap <leader>w /\C[A-Z_]<CR>h
    vnoremap <leader>W /\C[A-Z_]<CR>

	vnoremap <silent>* <ESC>:call VisualSearch('/')<CR>/<CR>
	vnoremap <silent># <ESC>:call VisualSearch('?')<CR>?<CR>

elseif env ==? "idea"

    noremap <leader>w ]w
    noremap <leader>W [w

endif













nnoremap <c-[> <nop>
nnoremap <c-]> <nop>
nnoremap <c-\> <nop>
nnoremap <c-s-[> <nop>
nnoremap <c-s-]> <nop>
nnoremap <c-s-\> <nop>

nnoremap ; <nop>
nnoremap <c-;> <nop>
nnoremap <c-s-;> <nop>

nnoremap <leader>< <nop>
nnoremap <leader>> <nop>
nnoremap <leader>- <nop>
nnoremap <leader>= <nop>




nnoremap ! <nop>
"" nnoremap <tab> <nop>
nnoremap <s-tab> <nop>
nnoremap <s-f1> <nop>
nnoremap <s-f5> <nop>
nnoremap <c-k> <nop>
nnoremap ,d <nop>
nnoremap <leader><leader> <nop>
nnoremap <leader>j <nop>
nnoremap <leader>J <nop>
