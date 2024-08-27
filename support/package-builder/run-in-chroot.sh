#!/bin/bash

set -o errexit -o nounset +h

SRCPATH=$(dirname $(realpath -s $0))
source $SRCPATH/common.sh

PRGNAME=${0##*/}
if [ $# -lt 1 ]; then
  fail "${PRGNAME}: No build root specified. Usage : ${PRGNAME} <build-root>"
fi

SOURCES=$1
shift
RPMS=$1
shift
BUILDROOT=$1
shift

# Goto chroot and run the command specified as parameter.
if [ ${EUID} -eq 0 ] ; then
  CHROOT_CMD=chroot
else
  #CHROOT_CMD="contain -b $SOURCES:usr/src/photon/SOURCES,$RPMS:usr/src/photon/RPMS -c"
  CHROOT_CMD="$SRCPATH/../../tools/bin/contain -b $RPMS:usr/src/photon/RPMS,$RPMS/../SRPMS:usr/src/photon/SRPMS,$RPMS/../PUBLISHRPMS:publishrpms,$RPMS/../PUBLISHXRPMS:publishxrpms -c -n"
fi

# Close all fds except stdin, stdout and stderr
for fd in $(ls /proc/$$/fd/); do
  [ $fd -gt 2 ] && exec {fd}<&-
done

$CHROOT_CMD "${BUILDROOT}" \
  /usr/bin/env -i \
  HOME=/root \
  TERM="$TERM" \
  PS1='\u:\w\$ ' \
  PATH=/bin:/usr/bin:/sbin:/usr/sbin:/tools/bin \
  SHELL=/bin/bash \
  LC_ALL=en_US.UTF-8 \
  /bin/bash --login +h -c "$*"

exit $?
