#!/bin/sh
# allo_instanceinfos.sh
#
# Portage de allo_instanceinfos_bash.sh@0d931deddb569164ed93ec0eb33a8e30e16a60c7
# en /bin/sh
#
# Script permettant de récupérer différentes informations concernant le système:
# date courante, pointeurs, uptime, distribution, processeur, noyau, mémoire,
# partitions.
#
# Les informations concernant les interfaces réseau sont désactivées, le code
# se trouve dans le fichier allo_instanceinfos_interfaces.sh.
#
# Format de sortie YAML 1.2
#
# Auteur: Christian BUFFIN (christian.buffin@libriciel.fr)
# Copyright: Libriciel SCOP (https://www.libriciel.fr/)
# License: CeCILL v.2.0 (http://www.cecill.info/licences/Licence_CeCILL_V2-fr.html)
# Version: 0.11.0
# Dernière modification: 08/12/2017
#-------------------------------------------------------------------------------
# On ajoute des chemins au PATH au cas où...
PATH="${PATH}:/sbin:/usr/sbin"
#-------------------------------------------------------------------------------
# Constantes
#-------------------------------------------------------------------------------
# Nom du script
scriptName="allo_instanceinfos.sh"
# Version du script
scriptVersion="0.11.1"
#-------------------------------------------------------------------------------
# Valeurs par défaut
#-------------------------------------------------------------------------------
# Script silencieux ?
scriptQuiet=false
# Fichier de résultat du script
scriptOutputFile=""
# URL sur laquelle envoyer le résultat du script
scriptOutputUrl=""
#-------------------------------------------------------------------------------
# Fonctions utilitaires
#-------------------------------------------------------------------------------
cmdmap() {
	local program="$1"
	command -v $program || echo $program
	return $?
}

get_value_from_name_equals_value_pairs() {
	local label="$1"
	local text="$2"
	local cmd_grep="`cmdmap grep`"
	local cmd_printf="`cmdmap printf`"
	local cmd_sed="`cmdmap sed`"

	$cmd_printf "$text" | $cmd_grep -i "$label=" | $cmd_sed "s/^.\+=\(.\+\)$/\1/g" | $cmd_sed "s/^\"\(.\+\)\"$/\1/g"
	return $?
}

get_value_from_name_colon_value_pairs() {
	local label="$1"
	local text="$2"
	local cmd_grep="`cmdmap grep`"
	local cmd_printf="`cmdmap printf`"
	local cmd_sed="`cmdmap sed`"

	$cmd_printf "$text" | $cmd_grep -i "$label:" | $cmd_sed 's/^.\+:[[:blank:]]*\(.*\)$/\1/g' | $cmd_sed "s/^\"\(.\+\)\"$/\1/g"
	return $?
}

format_memory() {
	local total="$1"
	local free="$2"

	local cmd_awk="`cmdmap awk`"
	local cmd_expr="`cmdmap expr`"
	local cmd_printf="`cmdmap printf`"

	local used="`$cmd_expr $total - $free`"
	local percent="`$cmd_expr $used \* 100 / $total`"
	local human="`$cmd_printf "$percent $used $total $free" | $cmd_awk '{ printf("%u%%%%, %.2f Go / %.2f Go, %.2f Go libres\n", $1, $2/(1024*1024), $3/(1024*1024), $4/(1024*1024)) }'`"
	$cmd_printf "  total: \"$total\"\n  free: \"$free\"\n  used: \"$used\"\n  percent: \"$percent\"\n  human: \"$human\"\n"
}

# Fonction utilitaire qui retourne l'UUID d'une partition.
#
# @param $1 La chemin vers le device de la partition (ex. /dev/sda1)
# @returns string ex. 5450-4444
partition_uuid() {
    local device="$1"

	local cmd_ls="`cmdmap ls`"
	local cmd_printf="`cmdmap printf`"
	local cmd_readlink="`cmdmap readlink`"

	for disk_uuid in `$cmd_ls -1A /dev/disk/by-uuid/ 2> /dev/null`;do
		local realpath="`$cmd_readlink -f /dev/disk/by-uuid/$disk_uuid 2> /dev/null`"
		if [ "$realpath" = "$device" ] ; then
			$cmd_printf "$disk_uuid\n"
			return 0
		fi
	done

	return 1
}

# Fonction utilitaire qui retourne le label d'une partition.
#
# @param $1 La chemin vers le device de la partition (ex. /dev/sda1)
# @returns string ex. DellUtility
partition_label() {
    local device="$1"

	local cmd_ls="`cmdmap ls`"
	local cmd_printf="`cmdmap printf`"
	local cmd_readlink="`cmdmap readlink`"

	for disk_label in `$cmd_ls -1A /dev/disk/by-label/ 2> /dev/null`;do
		local realpath="`$cmd_readlink -f /dev/disk/by-label/$disk_label 2> /dev/null`"
		if [ "$realpath" = "$device" ] ; then
			$cmd_printf "$disk_label\n"
			return 0
		fi
	done

	return 1
}

#-------------------------------------------------------------------------------

# Affiche l'aide du shell
allo_instanceinfos_help() {
	local cmd_printf="`cmdmap printf`"

	$cmd_printf "NOM\n"
	$cmd_printf "\t${scriptName} - récupération d'informations concernant le système\n"
	$cmd_printf "\nSYNOPSIS\n"
	$cmd_printf "\t${scriptName} [OPTIONS] [-o FILE]\n"
	$cmd_printf "\nDESCRIPTION\n"
	$cmd_printf "\tLe script facilite la récupération d'informations normalisées concernant une\n"
	$cmd_printf "\tinstance pour des techniciens.\n\n"
	$cmd_printf "\tLes catégories d'informations récupérées sont: date courante, pointeurs,\n"
	$cmd_printf "\tuptime, système,processeur, noyau, mémoire, partitions.\n\n"
	$cmd_printf "\tLes commandes nécessaires à l'exécution du script sont vérifiées au début, la\n"
	$cmd_printf "\tsortie se fait par défaut dans la console.\n"
	$cmd_printf "\nOPTIONS\n"
	$cmd_printf "\t-h, --help\tafficher l'aide et quitter\n"
	$cmd_printf "\t-o, --output\tfichier dans lequel stocker le résultat\n"
	$cmd_printf "\t-q, --quiet\tne pas afficher le résultat sur la sortie standard\n"
	$cmd_printf "\t-u, --url\tURL vers laquelle envoyer le fichier de résultat avec cURL\n"
	$cmd_printf "\t-v, --version\tafficher la version du script et quitter\n"
	$cmd_printf "\nEXEMPLES\n"
	$cmd_printf "\t${scriptName}\n"
	$cmd_printf "\t${scriptName} -q -o /tmp/instanceinfos.txt\n"
	$cmd_printf "\t${scriptName} -q -u https://curl.libriciel.fr\n"
}

# Affiche la version du script
allo_instanceinfos_version() {
	local cmd_printf="`cmdmap printf`"
	$cmd_printf "${scriptName} ${scriptVersion}\n"
}

# Retourne la date courante du système au format YAML.
#
# La chaîne retournée est composée d'une clé "date" et des sous-clés "seconds",
# "utc" et "human".
allo_read_current_date() {
	local cmd_printf="`cmdmap printf`"
	local cmd_date="`cmdmap date`"
	local date="`$cmd_date +'%d/%m/%Y %H:%M:%S (UTC%z)'`"
	local seconds="`$cmd_date +'%s'`"
	local utc="`$cmd_date +'%z'`"
	$cmd_printf "date:\n  seconds: \"$seconds\"\n  utc: \"$utc\"\n  human: \"$date\"\n\n"
}

# Retourne le nom d'hôte de la machine et son FQDN au format YAML.
#
# La chaîne retournée est composée d'une clé "pointers" et des sous-clés
# "hostname" et "fqdn".
allo_read_host_domain_names() {
	local cmd_hostname="`cmdmap hostname`"
	local cmd_printf="`cmdmap printf`"
	local cmd_uname="`cmdmap uname`"
	local hostname="`$cmd_uname -n 2> /dev/null`"
	local fqdn="`$cmd_hostname -f 2> /dev/null`"

	$cmd_printf "pointers:\n  hostname: \"$hostname\"\n  fqdn: \"$fqdn\"\n\n"
}

# Retourne l'uptime (la durée de fonctionnement) de la machine au format YAML.
#
# La chaîne retournée est composée d'une clé "uptime" et des sous-clés "seconds"
# et "human".
allo_read_uptime() {
	local cmd_printf="`cmdmap printf`"
	local cmd_sed="`cmdmap sed`"
	local seconds="`$cmd_sed 's/^\([0-9]\+\).*$/\1/g' /proc/uptime`"
	local human="`printf '%d jours %d heures %d minutes %d secondes' $(($seconds/86400)) $(($seconds/3600)) $(($seconds%3600/60)) $(($seconds%60))`"
	$cmd_printf "uptime:\n  seconds: \"$seconds\"\n  human: \"$human\"\n\n"
}

# Retourne le nom et la version du système utilisé sur la machine au format YAML.
#
# La chaîne retournée est composée d'une clé "system" et des sous-clés "id",
# "release", "codename" et "description".
allo_read_system() {
	local cmd_cat="`cmdmap cat`"
	local cmd_grep="`cmdmap grep`"
	local cmd_ls="`cmdmap ls`"
	local cmd_lsb_release="`cmdmap lsb_release`"
	local cmd_printf="`cmdmap printf`"
	local cmd_sed="`cmdmap sed`"
	local cmd_uniq="`cmdmap uniq`"
	local infos="`$cmd_lsb_release -a 2> /dev/null`"
	local id release codename description

 	# lsb_release
 	if [ ! -z "$infos" ] ; then
 		id=`get_value_from_name_colon_value_pairs "^Distributor ID" "$infos"`
 		release=`get_value_from_name_colon_value_pairs "^Release" "$infos"`
 		codename=`get_value_from_name_colon_value_pairs "^Codename" "$infos"`
 		description=`get_value_from_name_colon_value_pairs "^Description" "$infos"`
 	# /etc/os-release
 	elif [ -f /etc/os-release ] ; then
 		infos=`cat /etc/os-release`
 		id=`get_value_from_name_equals_value_pairs "^NAME" "$infos"`
 		release=`get_value_from_name_equals_value_pairs "^VERSION_ID" "$infos"`
 		codename=`get_value_from_name_equals_value_pairs "^VERSION_CODENAME" "$infos"`
 		description=`get_value_from_name_equals_value_pairs "^PRETTY_NAME" "$infos"`
     #@todo: vérifier
 	elif [ `$cmd_ls /etc/*release > /dev/null 2>&1 ; echo $?` -eq 0 ] ; then
 		infos=`$cmd_grep "\(DISTRIB_DESCRIPTION\|PRETTY_NAME\)" /etc/*release 2> /dev/null | $cmd_sed "s/^.\+=\"\(.\+\)\"$/\1/g" | $cmd_uniq`
 		id=`$cmd_printf "$infos" | $cmd_sed "s/^\(.*\)[[:blank:]]\+\([0-9\.]\+\)[[:blank:]]*.*$/\1/g"`
 		release=`$cmd_printf "$infos" | $cmd_sed "s/^\(.*\)[[:blank:]]\+\([0-9\.]\+\)[[:blank:]]*.*$/\2/g"`
 		codename=""
 		description="$infos"
    elif [ `$cmd_ls /etc/*-version > /dev/null 2>&1 ; echo $?` -eq 0 ] ; then
        infos="`$cmd_cat /etc/*-version 2> /dev/null`"
 		id=`$cmd_printf "$infos" | $cmd_sed "s/^\(.*\)[[:blank:]]\+\([0-9\.]\+\)[[:blank:]]*.*$/\1/g"`
 		release=`$cmd_printf "$infos" | $cmd_sed "s/^\(.*\)[[:blank:]]\+\([0-9\.]\+\)[[:blank:]]*.*$/\2/g"`
 		codename=""
 		description="$infos"
	fi

	$cmd_printf "system:\n  id: \"$id\"\n  release: \"$release\"\n  codename: \"$codename\"\n  description: \"$description\"\n\n"
}

# Retourne plusieurs lignes d'informations concernant le(s) processeur(s) de la
# machine au format YAML.
#
# La chaîne retournée est composée d'une clé "processor" et des sous-clés "model",
# "architecture", "processors", "cores", "hyperthreading" et "speeds".
allo_read_cpu() {
	local cmd_cut="`cmdmap cut`"
	local cmd_expr="`cmdmap expr`"
	local cmd_grep="`cmdmap grep`"
	local cmd_printf="`cmdmap printf`"
	local cmd_sed="`cmdmap sed`"
	local cmd_sort="`cmdmap sort`"
	local cmd_uname="`cmdmap uname`"
	local cmd_uniq="`cmdmap uniq`"
	local cmd_tr="`cmdmap tr`"
	local cmd_wc="`cmdmap wc`"

	local model="`$cmd_grep -i "^model name[[:blank:]]\+:" /proc/cpuinfo 2> /dev/null | $cmd_uniq | $cmd_sed "s/^[^:]\+: *//g" | $cmd_sed "s/[[:blank:]]\+/ /g"`"
	local all="`$cmd_grep -i "^bogomips[[:blank:]]\+:" /proc/cpuinfo 2> /dev/null | $cmd_wc -l`"
	local processors="`$cmd_grep -i "^physical id[[:blank:]]\+:" /proc/cpuinfo 2> /dev/null | $cmd_sort | $cmd_uniq | $cmd_wc -l`"
	processors="`$cmd_printf $processors | $cmd_sed "s/^0$/1/g"`"
	local cpu_cores="`$cmd_grep -i "^cpu cores[[:blank:]]\+:" /proc/cpuinfo 2> /dev/null | $cmd_sort | $cmd_uniq | $cmd_cut -d':' -f2 | $cmd_sed 's/\(^[[:blank:]]\+\|[[:blank:]]\+$\)//g'`"
	if [ -z "$cpu_cores" ] ; then
		cpu_cores="`$cmd_grep -i "^processor[[:blank:]]\+:" /proc/cpuinfo 2> /dev/null | $cmd_wc -l`"
	fi
	local physical_cores="`$cmd_expr $processors \\* $cpu_cores`"
	local mhz="`$cmd_grep -i "^cpu MHz[[:blank:]]\+:" /proc/cpuinfo 2> /dev/null | $cmd_sed "s/^[^:]\+: *//g" | $cmd_tr '\n' ' ' | $cmd_sed "s/ \+$//g" | $cmd_sed "s/ \+/, /g"`"
	local arch="`$cmd_uname -m 2> /dev/null`"

	local cpu="\n  model: \"$model\"\n  architecture: \"$arch\"\n  processors: \"$processors\"\n  physical_cores: \"$cpu_cores\"\n  virtual_cores: \"$all\"\n  speeds: [$mhz]"
	$cmd_printf "processor: $cpu\n\n"
}

# Retourne la version du noyau et du système au format YAML.
#
# La chaîne retournée est composée d'une clé "kernel" et des sous-clés "hardware",
# "name", "machine", "processor", "release", "os", "version"
allo_read_kernel() {
	local cmd_printf="`cmdmap printf`"
	local cmd_uname="`cmdmap uname`"
	local hardware="`$cmd_uname -i 2> /dev/null`"
	local machine="`$cmd_uname -m 2> /dev/null`"
	local processor="`$cmd_uname -p 2> /dev/null`"
	local name="`$cmd_uname -s 2> /dev/null`"
	local os="`$cmd_uname -o 2> /dev/null`"
	local release="`$cmd_uname -r 2> /dev/null`"
	local version="`$cmd_uname -v 2> /dev/null`"
	$cmd_printf "kernel:\n  name: \"$name\"\n  hardware: \"$hardware\"\n  machine: \"$machine\"\n  processor: \"$processor\"\n  release: \"$release\"\n  os: \"$os\"\n  version: \"$version\"\n\n"
}

# Retourne l'utilisation mémoire (RAM et SWAP) de la machine au format YAML.
#
# La chaîne retournée est composée d'une clé "memory", des sous-clés "ram" et
# "swap", elles-mêmes composées des sous-clés "total", "free", "used", "percent"
# et "human".
allo_read_memory() {
	local cmd_awk="`cmdmap awk`"
	local cmd_printf="`cmdmap printf`"

	local ram_total="`$cmd_awk '/^MemTotal:/ {printf $2}' /proc/meminfo`"
	local ram_free="`$cmd_awk '/^(MemFree|Buffers|Cached):/ {unused+=$2} END {printf("%d", unused)}' /proc/meminfo`"
	local ram="`format_memory $ram_total $ram_free | sed 's/%/%%/g' | sed 's/^/  /g'`"

	local swap_total="`$cmd_awk '/^SwapTotal:/ {printf $2}' /proc/meminfo`"
	local swap_free="`$cmd_awk '/^SwapFree:/ {printf $2}' /proc/meminfo`"
	local swap="`format_memory $swap_total $swap_free | sed 's/%/%%/g' | sed 's/^/  /g'`"

	$cmd_printf "memory:\n  ram:\n$ram\n  swap:\n$swap\n\n"
}

# Retourne des informations concernant les partitions montées sur le système au
# format YAML.
#
# La chaîne retournée est composée d'une clé "partitions", de sous-clés pour
# chacune des partitions, elles-mêmes composées des sous-clés "mountpoint",
# "label", "type", "uuid" et "usage", cette dernière étant composée des sous-clés
# "total", "free", "used", "percent" et "human".
allo_read_partitions() {
	local cmd_awk="`cmdmap awk`"
	local cmd_cut="`cmdmap cut`"
	local cmd_df="`cmdmap df`"
	local cmd_printf="`cmdmap printf`"
	local cmd_sed="`cmdmap sed`"
	local cmd_tr="`cmdmap tr`"

	$cmd_printf "partitions:\n"

    $cmd_df -T -P 2> /dev/null | $cmd_sed -n '1!p' | $cmd_sed 's/%//g' | while read -r entry ; do
        local entry="`$cmd_printf "$entry" | $cmd_sed 's/%//g' | $cmd_tr -s ' '`"
        local filesystem=`$cmd_printf "$entry" | $cmd_cut -d ' ' -f 1`
		local type=`$cmd_printf "$entry" | $cmd_cut -d ' ' -f 2`
		if [ "$type" != "tmpfs" -a "$type" != "devtmpfs" ] ; then
			local total=`$cmd_printf "$entry" | $cmd_cut -d ' ' -f 3`
			local free=`$cmd_printf "$entry" | $cmd_cut -d ' ' -f 5`
			local mounted=`$cmd_printf "$entry" | $cmd_cut -d ' ' -f 7`
			local uuid=`partition_uuid $filesystem`
			local label=`partition_label $filesystem`
			local usage="`format_memory $total $free | sed 's/%/%%/g' | sed 's/^/    /g'`"

			$cmd_printf "  -\n    filesystem: \"$filesystem\"\n    mountpoint: \"$mounted\"\n    label: \"$label\"\n    type: \"$type\"\n    uuid: \"$uuid\"\n    usage:\n$usage\n"
		fi
    done

	$cmd_printf "\n"
}

# Vérification de la présence des commandes nécessaires
scriptCheckEnvironment() {
	local commands="$1"
	local missing=""
	for command in $commands; do
		command -v $command > /dev/null 2>&1
		if [ $? -ne 0 ] ; then
			missing="$missing $command"
		fi
	done
	if [ ! -z "$missing" ] ; then
        version=`allo_instanceinfos_version`
        echo "$version" >&2
		echo "Commande(s) manquante(s):$missing" >&2
		exit 1
	fi
}

# Lecture des options
scriptParseOptions() {
    TEMP=`getopt --options ho:qu:v --long help,output:,quiet,url:,version --name "$scriptName" -- "$@"`
    success="$?"
    if [ $success != 0 ] ; then
        exit $success
    fi
    eval set -- "${TEMP}"

    # Extraction des options
    while true ; do
        case "$1" in
            -h|--help)
                allo_instanceinfos_help
                exit 0
            ;;
            -o|--output)
                scriptOutputFile="$2"
                shift 2
    		;;
            -q|--quiet)
                scriptQuiet=true
                shift
            ;;
            -u|--url)
                scriptOutputUrl="$2"
                shift 2
    		;;
            -v|--version)
                allo_instanceinfos_version
                exit 0
            ;;
            :)
                $cmd_printf "Erreur! :\n"
                exit 1
            ;;
            \?)
                $cmd_printf "Erreur! ?\n"
                exit 1
            ;;
            --)
                shift
                break
            ;;
            *)
                $cmd_printf "Erreur! *\n"
                exit 1
            ;;
        esac
    done
}

scriptOutput() {
	local cmd_printf="`cmdmap printf`"
	local version="`allo_instanceinfos_version`"

	$cmd_printf "# %s\n" "$version" && \
	$cmd_printf "%s\n" "%YAML 1.2" && \
	$cmd_printf "%s\n" "---" && \
	allo_read_current_date && \
	allo_read_host_domain_names && \
	allo_read_uptime && \
	allo_read_system && \
	allo_read_cpu && \
	allo_read_kernel && \
	allo_read_memory && \
	allo_read_partitions && \
	$cmd_printf "%s\n" "..."
}

# Export des informations vers une URL via cURL
scriptOutputToUrl() {
	local output="$1"
	local cmd_curl="`cmdmap curl`"
	local cmd_mktemp="`cmdmap mktemp`"
	local cmd_rm="`cmdmap rm`"

	local contentFile="$scriptOutputFile"
	local curl_command=""
	local url=""
	local tmp_file="${scriptName}_XXXXXXXXXX.txt"
	local success=0

	if [ -z "$scriptOutputFile" ] ; then
		contentFile="`$cmd_mktemp -t ${tmp_file} 2>&1`"
		if [ $? -ne 0 ] ; then
			echo "Erreur lors de la création du fichier temporaire"
			echo "$contentFile"
			return $?
		fi
		echo "$output" > "$contentFile"
		if [ $? -ne 0 ] ; then
			echo "Erreur lors du remplissage du fichier temporaire"
			return $?
		fi
	fi

	curl_command="$cmd_curl --show-error --silent --location --upload-file "$contentFile" "$scriptOutputUrl/allo.txt""
	url="`$curl_command 2>&1`"
	if [ $? -ne 0 ] ; then
		echo "Erreur lors de la commande: $curl_command"
		echo "$url"
		return $?
	fi

	if [ -z "$scriptOutputFile" ] ; then
		$cmd_rm "$contentFile" 2>&1
		if [ $? -ne 0 ] ; then
			echo "Erreur lors de la suppression du fichier $contentFile"
			success=$?
		fi
	fi

	echo "Sortie du script transférée sur $url"
	return $success
}

#-------------------------------------------------------------------------------

# Fonction principale
main() {
    scriptCheckEnvironment "awk cat cut date df expr getopt grep hostname ls printf readlink sed sort tr uname uniq wc"
    scriptParseOptions "$@"

	# Si on veut transférer le résultat sur une URL, il faut des commandes supplémentaires
	if [ ! -z "$scriptOutputUrl" ] ; then
		scriptCheckEnvironment "curl mktemp rm"
	fi

	local output="`scriptOutput 2>&1`"
    local result=$?

	if [ $result -eq 0 ] ; then
		if [ $scriptQuiet != true ] ; then
			echo "$output"
		fi

		if [ ! -z "$scriptOutputFile" ] ; then
			touch "$scriptOutputFile" && \
			echo "$output" > "$scriptOutputFile" && \
			echo "Sortie du script écrite dans $scriptOutputFile"
		fi

		if [ ! -z "$scriptOutputUrl" ] ; then
			output="`scriptOutputToUrl "$output"`"
			result=$?
			echo "$output"
		fi
	else
		echo "Erreur lors de la récupération des informations"
		echo "$output"
	fi

    exit $result
}

main "$@"