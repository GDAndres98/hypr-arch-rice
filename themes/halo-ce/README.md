# Halo CE

The menus of **Halo: Combat Evolved** (Xbox, 2001): space navy, shield-blue frames, soft blue glow, segmented slanted meters,
wide Michroma titles. Built on the design system of [halo-ce-latam-audio](https://github.com/GDAndres98/halo-ce-latam-audio)
(`docs/ui-design-system.md`). Switch to it with `theme halo-ce`.

![Halo CE: work mode](screenshots/work.webp)

## Desktop mode and work mode

An empty workspace shows the **eww dashboard** (no bar). As soon as a window opens, the dashboard closes and **waybar** appears
(`update_mode()` in `hypr/hyprland.lua`).

| Desktop mode: eww dashboard | Work mode: waybar + windows |
|---|---|
| ![dashboard](screenshots/desktop.webp) | ![work mode](screenshots/work.webp) |

**Dashboard** (`eww/`), a MJOLNIR Mark V HUD: Legion banner (machine + uptime), Energy Shield (battery as a health bar,
power draw, power profile), CPU Telemetry (CPU / memory / GPU on slanted segment meters), Network / Comms and Storage / I-O
(30-second graphs), Thermal (CPU / GPU core temperatures).

**Bar** (`waybar/`): plain space navy. Workspaces as blue menu words (active one near-white with a glow), date and time
centered in the wide title face, then volume (click: wiremix), brightness, Wi-Fi (shown here as UNSC-NET; left-click:
saved connections, right-click: join a network) and the battery as a shield/health meter of 10 slanted segments.

Windows: square corners, 2 px frame blue (`#2f8cff`) border with a blue glow on the focused window only, no border on the others.

## Rofi menus

| App finder (`Super+R`) | Calculator (`Super+Shift+C`) | Clipboard history (`Super+Shift+V`) |
|---|---|---|
| ![apps](screenshots/rofi-apps.webp) | ![calculator](screenshots/rofi-calc.webp) | ![clipboard](screenshots/rofi-clipboard.webp) |

UNSC // Index, Ballistics and Comm Log: translucent navy over blur (a layer rule in `hypr/theme.lua`), Warthog-yellow results.

## Palette and fonts

| | Color |
|---|---|
| Space navy (background) | `#03091a` |
| Panel | `#061230` |
| Frame / dim frame / hairline | `#2f8cff` / `#1d4e8f` / `#17345f` |
| Menu blue (labels) | `#4da3ff` |
| Near-white (values) / muted | `#dce9f8` / `#8fa9cc` |
| Cyan (focus) | `#7fe3ff` |
| Amber / coral / green | `#f2c25c` / `#ff8f80` / `#97d468` |

Fonts: **Michroma** (wide titles) and **Saira** (everything else), both OFL from Google Fonts, installed in
`~/.local/share/fonts/` (not in this repo).
