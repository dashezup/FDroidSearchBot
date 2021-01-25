#!/bin/sh

# 0 */6 * * * $(realpath fetch-repoindex.sh) && sv restart fdroidsearchbot

BASEDIR=$(dirname $(realpath $0))
download() {
	uri="$1"
	file="$2"
	if test -e "$file"; then
		zflag="-z $file"
	else
		zflag=
	fi
	HTTP_CODE=$(curl -sR --write-out %{http_code} -o "$file" $zflag "$uri")
	LAST_MODIFIED=$(date -r $file -u '+%F %T')
	echo -n 'Download: '
	case "$HTTP_CODE" in
		304) echo "$LAST_MODIFIED $file (bypassed)"; return 1;;
		200) echo "$LAST_MODIFIED $file (update)"; return 0;;
		000) echo "$file (failed)"; return 1;;
	*) echo "$file ($HTTP_CODE)"; return 1;;
	esac
}

NEW_XML=false
download "https://f-droid.org/repo/index.xml" "${BASEDIR}/fdroid.xml" && NEW_XML=true
download "https://apt.izzysoft.de/fdroid/repo/index.xml" "${BASEDIR}/izzy.xml" && NEW_XML=true

if [ "$NEW_XML" = true ]; then
	exit 0
else
	exit 1
fi
