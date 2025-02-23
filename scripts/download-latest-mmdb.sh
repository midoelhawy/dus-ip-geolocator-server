#!/bin/sh
latestDbVersion="https://github.com/midoelhawy/global-geo-ip-database-generator/releases/latest/download/ASN_COUNTRY_AND_CITY.mmdb"
latestASNDatabase="https://github.com/midoelhawy/global-geo-ip-database-generator/releases/latest/download/asn_database.sqlite"
destination="db"
force="false"

while [ $# -gt 0 ]; do
    if [ "$1" = "--force" ]; then
        force="true"
    fi
    shift
done



if [ "$DOWNLOAD_LATEST_DB_VERSION" = "true" ]; then
    force="true"
fi


compare_versions() {
    local ver1=$1
    local ver2=$2
    if [ "$ver1" \> "$ver2" ]; then
        return 0
    fi
    return 1
}

github_api_url="https://api.github.com/repos/midoelhawy/global-geo-ip-database-generator/releases/latest"
latest_version=$(curl -s $github_api_url | jq -r '.tag_name')

echo "$latest_version" > latest_version.txt

current_version=$(cat current_db_version.txt)
if [ -z "$current_version" ]; then
    echo "🛑 No Version found Localy"
    force="true"
else
    compare_versions "$latest_version" "$current_version"
    if [ $? -eq 0 ]; then
        echo "🟠 The version of db is out of date; i am going to download the latest db"
        force="true"
    fi
fi




if [ ! -f "$destination/db.mmdb" ] || [ "$force" = "true" ]; then
    wget -O "$destination/db.mmdb" "$latestDbVersion"
    echo "$latest_version" > current_db_version.txt

else
    echo "File already exists in $destination. Use --force to download again."
fi


if [ ! -f "$destination/asn_database.sqlite" ] || [ "$force" = "true" ]; then
    wget -O "$destination/asn_database.sqlite" "$latestASNDatabase"
    #echo "$latest_version" > current_db_version.txt

else
    echo "File already asn_database.sqlite exists in $destination. Use --force to download again."
fi
