_hlfilter_completion() {
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _HLFILTER_COMPLETE=complete $1 ) )
    return 0
}

complete -F _hlfilter_completion -o default hlfilter;
