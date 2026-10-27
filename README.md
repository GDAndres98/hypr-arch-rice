# dotfiles

Config for my Arch Linux + Hyprland setup, with switchable themes.

## Layout

```
dotfiles/
├── hypr/                  shared, linked from ~/.config/hypr
│   ├── hyprland.lua         monitors, input, keybinds, rules, autostart; does require("theme")
│   ├── hypridle.conf        idle timers
│   ├── theme.lua      ->  ../current/hypr/theme.lua
│   └── hyprlock.conf  ->  ../current/hypr/hyprlock.conf
├── kitty/                 shared, linked from ~/.config/kitty
├── current  ->  themes/halo-ce      the ACTIVE theme (one link to switch)
└── themes/
    └── halo-ce/
        ├── hypr/theme.lua       borders, shadows, blur, animations, background color
        ├── hypr/hyprlock.conf   lock screen
        ├── waybar/              linked from ~/.config/waybar (through current)
        ├── mako/                linked from ~/.config/mako
        └── eww/                 linked from ~/.config/eww
```

`~/.config/waybar`, `mako` and `eww` point at `~/dotfiles/current/...`, so they follow whichever theme is active.

## Switch theme

```bash
ln -sfn themes/<name> ~/dotfiles/current      # -s symlink, -f replace, -n treat the old link as a file
hyprctl reload                                 # Hyprland look
pkill -x waybar; waybar & disown               # bar (if it's showing)
makoctl reload                                 # notifications
eww kill; eww daemon                           # widgets
```

hyprlock reads its config each time it starts, so it needs no reload.

## New theme

Copy `themes/halo-ce` to `themes/<name>` and edit it. Each theme must provide:
- `hypr/theme.lua` and `hypr/hyprlock.conf`
- `waybar/`, `mako/config`, `eww/`
- an eww window named `dashboard` (`hyprland.lua` opens it on empty workspaces)

## New machine

```bash
git clone git@github.com:<you>/hypr-arch-rice.git ~/dotfiles
ln -s ~/dotfiles/hypr ~/.config/hypr
ln -s ~/dotfiles/kitty ~/.config/kitty
for x in waybar eww mako; do ln -s ~/dotfiles/current/$x ~/.config/$x; done
```
