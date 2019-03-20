# Ugly workaround to remove "user" filesystem label for two-partition headless images
if [ -e /dev/disk/by-label/user ];
then
e2label /dev/disk/by-label/user ''
fi
