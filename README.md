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
├── bin/                   scripts, linked into ~/.local/bin: `theme`, `sw-mode`
├── current  ->  themes/halo-ce      the ACTIVE theme (one link to switch)
└── themes/
    ├── imperial/            Star Wars Imperial console, with Aurebesh (see below)
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
theme              # list themes, * = active
theme imperial     # switch: relinks `current`, runs the theme's leave/enter hooks, reloads everything
```

hyprlock reads its config each time it starts, so it needs no reload.

## Imperial theme: Aurebesh modes

```bash
sw-mode 1    # Latin text, Aurebesh subtitle
sw-mode 2    # Aurebesh text, Latin subtitle
sw-mode 3    # everything Aurebesh, also apps (fontconfig) and kitty. Type `sw-mode 1` blind to leave
sw-mode      # rebuild with the saved mode (after editing a template)
```

The mode is saved in `~/.local/state/sw-mode` and survives reboots.
Waybar, mako, eww and hyprlock files in `themes/imperial/` are **templates** (`*.in`). `sw-mode` fills in
the fonts and writes the real file next to it (git ignores those). **Edit the `.in` file**, then run `sw-mode`.
Fonts and their licenses: `themes/imperial/fonts/`.

## New theme

Copy `themes/halo-ce` to `themes/<name>` and edit it. Each theme must provide:
- `hypr/theme.lua` and `hypr/hyprlock.conf`
- `waybar/`, `mako/config`, `eww/`
- an eww window named `dashboard` (`hyprland.lua` opens it on empty workspaces)
- optional executable hooks `enter` / `leave`, run by `theme` when switching to / away from it

## New machine

```bash
git clone git@github.com:<you>/hypr-arch-rice.git ~/dotfiles
ln -s ~/dotfiles/hypr ~/.config/hypr
ln -s ~/dotfiles/kitty ~/.config/kitty
for x in waybar eww mako; do ln -s ~/dotfiles/current/$x ~/.config/$x; done
ln -s ~/dotfiles/bin/theme ~/dotfiles/bin/sw-mode ~/.local/bin/
ln -s ~/dotfiles/themes/imperial/fonts ~/.local/share/fonts/imperial
sw-mode --no-reload   # builds the Imperial configs from their templates
```
