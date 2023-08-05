#!/usr/bin/env bash

# GPL v3 License
#
# Copyright (c) 2018 Blake Huber
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


function _complete_5_horsemen_commands(){
    local cmds="$1"
    local split='5'       # times to split screen width
    local ct="0"
    local IFS=$' \t\n'
    local formatted_cmds=( $(compgen -W "${cmds}" -- "${cur}") )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_region_subcommands -->
}


function _complete_5_horsemen_subcommands(){
    local cmds="$1"
    local split='4'       # times to split screen width
    local ct="0"
    local IFS=$' \t\n'
    local formatted_cmds=( $(compgen -W "${cmds}" -- "${cur}") )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_region_subcommands -->
}


function _complete_keyup_commands(){
    local cmds="$1"
    local split='6'       # times to split screen width
    local ct="0"
    local IFS=$' \t\n'
    local formatted_cmds=( $(compgen -W "${cmds}" -- "${COMP_WORDS[1]}") )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_keyup_commands -->
}


function _complete_profile_subcommands(){
    local cmds="$1"
    local split='7'       # times to split screen width
    local ct="0"
    local IFS=$' \t\n'
    local formatted_cmds=( $(compgen -W "${cmds}" -- "${cur}") )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_profile_subcommands -->
}


function _complete_username_subcommands(){
    local cmds="$1"
    local split='7'       # times to split screen width
    local ct="0"
    local IFS=$' \t\n'
    local formatted_cmds=( $(compgen -W "${cmds}" -- "${cur}") )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_username_subcommands -->
}


function _list_iam_users(){
    ##
    ##  Returns array of iam users
    ##
    local profile_name="$1"
    declare -a profiles

    if [ ! $profile_name ]; then
        profile_name="default"
    fi
    for user in $(aws iam list-users  --profile $profile_name --output json | jq .Users[].UserName); do
        profiles=(  "${profiles[@]}" "$user"  )
    done
    echo "${profiles[@]}"
    return 0
}


function _numargs(){
    ##
    ## Returns count of number of parameter args passed
    ##
    local parameters="$1"
    local numargs=0

    if [[ ! "$parameters" ]]; then
        printf -- '%s\n' "0"
    else
        for i in $(echo $parameters); do
            numargs=$(( $numargs + 1 ))
        done
        printf -- '%s\n' "$numargs"
    fi
    return 0
    #
    # <-- end function _numargs -->
}


function _parse_compwords(){
    ##
    ##  Interogate compwords to discover which of the  5 horsemen are missing
    ##
    compwords=("${!1}")
    four=("${!2}")

    declare -a missing_words

    for key in "${four[@]}"; do
        if [[ ! "$(echo "${compwords[@]}" | grep ${key##*-})" ]]; then
            missing_words=( "${missing_words[@]}" "$key" )
        fi
    done
    printf -- '%s\n' "${missing_words[@]}"
    #
    # <-- end function _parse_compwords -->
}


function _return_profiles(){
    ##
    ##  Returns a list of all awscli profiles
    ##
    if [ -f "$HOME/.aws/credentials" ]; then
        echo "$(grep '\[*\]' ~/.aws/credentials | cut -c 2-80 | rev | cut -c 2-80 | rev)"

    elif [ -f "$HOME/.aws/config" ]; then
        echo "$(grep 'profile' ~/.aws/config | awk '{print $2}' | rev | cut -c 2-80 | rev)"

    fi
    return 0
}

function _keyup_completions(){
    ##
    ##  Completion structures for keyup exectuable
    ##
    local numargs numoptions cur prev initcmd
    local completion_dir

    completion_dir="$HOME/.bash_completion.d"
    config_dir="$HOME/.config/keyup"
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    initcmd="${COMP_WORDS[COMP_CWORD-2]}"
    #echo "cur: $cur, prev: $prev"

    # initialize vars
    COMPREPLY=()
    numargs=0
    numoptions=0

    # option strings
    commands='--quiet --configure --debug --help --key-report --operation --profile --user-name --version'
    conjunct_commands='--profile  --operation  --user-name  --quiet  --debug'
    operations='list up'


    case "${initcmd}" in

        '--profile' | '--user-name' | '--operation')
            ##
            ##  Return compreply with any of the 5 comp_words that
            ##  not already present on the command line
            ##
            declare -a horsemen
            horsemen=(  '--profile'  '--operation'  '--user-name' '--quiet' '--debug' )
            subcommands=$(_parse_compwords COMP_WORDS[@] horsemen[@])
            numargs=$(_numargs "$subcommands")

            if [ "$cur" = "" ] || [ "$cur" = "-" ] || [ "$cur" = "--" ] && (( "$numargs" > 2 )); then
                _complete_5_horsemen_subcommands "${subcommands}"
            else
                COMPREPLY=( $(compgen -W "${subcommands}" -- ${cur}) )
            fi
            return 0
            ;;
    esac

    case "${cur}" in

        '--h'*)
            COMPREPLY=( $(compgen -W '--help' -- ${cur}) )
            return 0
            ;;

        '--c'*)
            COMPREPLY=( $(compgen -W '--configure' -- ${cur}) )
            return 0
            ;;

        '--d'*)
            COMPREPLY=( $(compgen -W '--debug' -- ${cur}) )
            return 0
            ;;

        '--k'*)
            COMPREPLY=( $(compgen -W '--key-report' -- ${cur}) )
            return 0
            ;;

        '--o'*)
            COMPREPLY=( $(compgen -W '--operation' -- ${cur}) )
            return 0
            ;;

        '--p'*)
            COMPREPLY=( $(compgen -W '--profile' -- ${cur}) )
            return 0
            ;;

        '--q'*)
            COMPREPLY=( $(compgen -W '--quiet' -- ${cur}) )
            return 0
            ;;

        '--u'*)
            COMPREPLY=( $(compgen -W '--user-name' -- ${cur}) )
            return 0
            ;;

        '--v'*)
            COMPREPLY=( $(compgen -W '--version' -- ${cur}) )
            return 0
            ;;

        'keyup' | 'keyu')
            #COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )
            _complete_keyup_commands "${commands}"
            return 0
            ;;

    esac

    case "${prev}" in

        '--profile')
            python3=$(which python3)
            iam_users=$($python3 "$config_dir/iam_users.py")

            if [ "$cur" = "" ] || [ "$cur" = "-" ] || [ "$cur" = "--" ]; then

                # display full completion subcommands
                _complete_profile_subcommands "${iam_users}"

            else
                COMPREPLY=( $(compgen -W "${iam_users}" -- ${cur}) )
            fi
            return 0
            ;;

        '--quiet' | '--debug')
            ##
            ##  Return compreply with any of the 5 comp_words that
            ##  not already present on the command line
            ##
            declare -a horsemen
            horsemen=(  '--profile'  '--operation'  '--user-name'  )
            subcommands=$(_parse_compwords COMP_WORDS[@] horsemen[@])
            numargs=$(_numargs "$subcommands")

            if [ "$cur" = "" ] || [ "$cur" = "-" ] || [ "$cur" = "--" ] && (( "$numargs" > 2 )); then
                _complete_5_horsemen_subcommands "${subcommands}"
            else
                COMPREPLY=( $(compgen -W "${subcommands}" -- ${cur}) )
            fi
            return 0
            ;;

        '--configure' | '--version' | '--help' | '--key-report')
            return 0
            ;;

        '--operation')
            COMPREPLY=( $(compgen -W  'list up' -- ${cur}) )
            return 0
            ;;

        '--user-name')
            ##  NOTE: Need to filter users by account number assoc with --profile
            ## use python3 config parser
            python3=$(which python3)
            iam_users=$($python3 "$config_dir/iam_users.py" default)

            if [ "$cur" = "" ] || [ "$cur" = "-" ] || [ "$cur" = "--" ]; then

                _complete_username_subcommands "${iam_users}"

            else
                COMPREPLY=( $(compgen -W "${iam_users}" -- ${cur}) )
            fi
            return 0
            ;;

        'keyup')
            if [ "$cur" = "" ] || [ "$cur" = "-" ] || [ "$cur" = "--" ]; then

                _complete_keyup_commands "${commands}"
                return 0
            fi
            ;;
    esac

    COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )

} && complete -F _keyup_completions keyup
