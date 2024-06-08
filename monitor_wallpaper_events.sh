# !/bin/bash

# Function to get the current wallpaper
get_current_wallpaper() {
    xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitoreDP-1/workspace0/last-image
}

# Initial wallpaper
current_wallpaper=$(get_current_wallpaper)
echo $current_wallpaper

# Monitor for changes
while true; do
    new_wallpaper=$(get_current_wallpaper)
    if [ "$current_wallpaper" != "$new_wallpaper" ]; then
        current_wallpaper=$new_wallpaper
        echo "wallpaper chagned"
        ~/Documents/projects/Themer/on_wallpaper_change.sh $new_wallpaper
    fi
    sleep 1
done
