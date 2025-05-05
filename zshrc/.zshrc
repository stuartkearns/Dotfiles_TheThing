# Lines configured by zsh-newuser-install
# Updated 2024-10-17
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
bindkey -e
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '/home/stuartkearns/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall
alias config='/usr/bin/git --git-dir=/home/stuartkearns/dotfiles/ --work-tree=/home/stuartkearns'
