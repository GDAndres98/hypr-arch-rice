# dotfiles

Config for my Arch Linux + Hyprland setup, with switchable themes.

## Layout

```
dotfiles/
├── hypr/                  shared, linked from ~/.config/hypr
│   ├── hyprland.lua         monitors, input, keybinds, rules, autostart; does require("theme")
│   ├── hypridle.conf        idle timers
│   ├── hyprtoolkit.conf ->  ../current/hypr/hyprtoolkit.conf   (look of Hyprland's own small apps)
│   ├── theme.lua      ->  ../current/hypr/theme.lua
│   └── hyprlock.conf  ->  ../current/hypr/hyprlock.conf
├── kitty/                 shared, linked from ~/.config/kitty
├── xkb/                   local only (gitignored): this laptop's keyboard tweaks, linked from ~/.config/xkb
├── bin/                   scripts, linked into ~/.local/bin: `theme`, `sw-mode`, `comms` (nmtui in theme colors), `doom`/`doom2` (Crispy Doom with the WADs in `/data/games/doom`), `stardew` (Stardew Valley from `/data/games/stardew`, no Steam)
├── current  ->  themes/<name>       the ACTIVE theme (one link to switch)
└── themes/
    ├── imperial/            Star Wars Imperial console, with Aurebesh (see below)
    └── halo-ce/
        ├── hypr/theme.lua       borders, shadows, blur, animations, background color
        ├── hypr/hyprlock.conf   lock screen
        ├── hypr/hyprtoolkit.conf  look of hyprland-run and other hyprtoolkit apps
        ├── rofi/config.rasi     app finder on SUPER + R (blur/dim/animation: layer rule in theme.lua)
        ├── rofi/clipboard.rasi  clipboard history on SUPER + SHIFT + V (imports config.rasi)
        ├── rofi/calc.rasi       calculator on SUPER + SHIFT + C (imports config.rasi)
        ├── imv/                 image viewer, linked from ~/.config/imv
        ├── gtk-3.0/             GTK3 apps (file dialogs, Firefox dialogs): palette + dark, needs adw-gtk-theme; linked from ~/.config/gtk-3.0
        ├── gtk-4.0/             GTK4 apps (= pavucontrol) + dark preference, linked from ~/.config/gtk-4.0
        ├── waybar/              linked from ~/.config/waybar (through current)
        ├── mako/                linked from ~/.config/mako
        └── eww/                 linked from ~/.config/eww
```

`~/.config/waybar`, `mako`, `eww`, `imv`, `gtk-3.0` and `gtk-4.0` point at `~/dotfiles/current/...`, so they follow whichever theme is active.

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
sw-mode 3    # everything Aurebesh, also apps (fontconfig), kitty and Dolphin's file list. Type `sw-mode 1` blind to leave
sw-mode      # rebuild with the saved mode (after editing a template)
```

The mode is saved in `~/.local/state/sw-mode` and survives reboots.
Qt apps ignore the fontconfig rule, so mode 3 also sets Dolphin's view font in `~/.config/dolphinrc` (`kwriteconfig6`); close Dolphin before switching.
Waybar, mako, eww, hyprlock, hyprtoolkit, rofi and imv files in `themes/imperial/` are **templates** (`*.in`). `sw-mode` fills in
the fonts and writes the real file next to it (git ignores those). **Edit the `.in` file**, then run `sw-mode`.
Fonts and their licenses: `themes/imperial/fonts/`.

## New theme

Copy `themes/halo-ce` to `themes/<name>` and edit it. Each theme must provide:
- `hypr/theme.lua`, `hypr/hyprlock.conf` and `hypr/hyprtoolkit.conf`
- `rofi/config.rasi`, `rofi/clipboard.rasi`, `rofi/calc.rasi` (keybinds run them straight from `current/`, no `~/.config` link)
- `imv/config`
- `gtk-3.0/gtk.css` + `settings.ini` (GTK3 palette: `@define-color` only, no selectors, so waybar/eww are untouched; only works on the `adw-gtk3-dark` base theme)
- `gtk-4.0/gtk.css` + `settings.ini` (pavucontrol colors; plain CSS, no template)
- `waybar/`, `mako/config`, `eww/`
- an eww window named `dashboard` (`hyprland.lua` opens it on empty workspaces)
- optional executable hooks `enter` / `leave`, run by `theme` when switching to / away from it

## New machine

```bash
git clone git@github.com:<you>/hypr-arch-rice.git ~/dotfiles
ln -s ~/dotfiles/hypr ~/.config/hypr
ln -s ~/dotfiles/kitty ~/.config/kitty
for x in waybar eww mako imv gtk-3.0 gtk-4.0; do ln -s ~/dotfiles/current/$x ~/.config/$x; done
sudo pacman -S adw-gtk-theme   # GTK3 base theme that reads our palette
gsettings set org.gnome.desktop.interface gtk-theme adw-gtk3-dark
gsettings set org.gnome.desktop.interface color-scheme prefer-dark
ln -s ~/dotfiles/bin/theme ~/dotfiles/bin/sw-mode ~/dotfiles/bin/comms ~/dotfiles/bin/doom ~/dotfiles/bin/doom2 ~/dotfiles/bin/stardew ~/.local/bin/
ln -s ~/dotfiles/themes/imperial/fonts ~/.local/share/fonts/imperial
sw-mode --no-reload   # builds the Imperial configs from their templates
```
