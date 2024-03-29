#! /bin/sh

specs="linux-api-headers/linux-api-headers.spec linux/linux.spec linux/linux-esx.spec linux/linux-secure.spec linux/linux-rt.spec"

tarball_url=`curl -s https://www.kernel.org  | grep -Eo 'https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.1.[0-9]*.tar.xz' | uniq`
tarball=$(basename $tarball_url)
version=`echo $tarball | sed 's/linux-//; s/.tar.xz//'`
echo latest linux version: $version
test -f stage/SOURCES/$tarball && echo up to date && exit 0
$(cd stage/SOURCES && wget $tarball_url)
sha512=`sha512sum stage/SOURCES/$tarball | awk '{print $1}'`
changelog_entry=$(echo "`date +"%a %b %d %Y"` `git config user.name` <`git config user.email`> $version-1")
for spec in $specs; do
	sed -i '/^Version:/ s/6.1.[0-9]*/'$version'/' SPECS/$spec
	sed -i '/^Release:/ s/[0-9]*%/1%/' SPECS/$spec
	sed -i '/^%define sha512 linux/ s/=[0-9a-f]*$/='$sha512'/' SPECS/$spec
	sed -i '/^%changelog/a* '"$changelog_entry"'\n- Update to version '"$version"'' SPECS/$spec
done
