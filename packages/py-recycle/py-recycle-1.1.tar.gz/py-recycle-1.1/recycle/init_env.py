import os
from recycle.lib import my_print, HOME

shell_config = {
    "zsh": """compdef '_files -W ~/.Trash`pwd`' undel""",
    "bash": """_undel() {
    local trash_home="$HOME/.Trash"
    local current_path=`pwd`
    local current_arg="${COMP_WORDS[COMP_CWORD]}"
    local trash_dir=$trash_home$current_path/${COMP_LINE:6:999}
    local IFS=$'\t\n'

    if [[ $current_arg =~ ^/ ]] ; then
      # /a/b/c
      return 0
    elif [[ $current_path =~ $trash_home ]] ; then
      # in /root/.Trash/
      return 0
    elif [[ ! -d $trash_dir ]] ; then
      # /root/.Trash/`pwd` don't exists
      return 0
    elif [[ -d $trash_dir ]] ; then
      COMPREPLY=( $(compgen -W "`ls -a $trash_dir|grep -Pv '^\.{1,2}$'`" -- ${current_arg}) )
      return 0
    fi
}

complete -o filenames -o dirnames -o default -F _undel undel""",
}


def install(shell):
    if os.path.exists("/bin/" + shell):
        shellrc_path = "{}/.{}rc".format(HOME, shell)
        if os.path.exists(shellrc_path) and "undel" in open(shellrc_path, "r").read():
            my_print("undel already in ~/.{}rc".format(shell))
            return
        else:
            open(shellrc_path, "a+").write(shell_config[shell])
        os.system("/bin/{} -c 'source {}/.{}rc'".format(shell, HOME, shell))
        my_print("Installed in {}, enjoy it :)".format(shellrc_path))
    else:
        my_print("your don't have {}, skip it".format(shell))


def main():
    install("zsh")
    install("bash")
