-- Imperial theme: the Hyprland look (loaded by require("theme") in hyprland.lua)
-- Death Star / Star Destroyer console: black, cold grey, warning red, hard edges.

-----------------------
---- LOOK AND FEEL ----
-----------------------

hl.config({
    general = {
        gaps_in  = 2,
        gaps_out = 4,

        border_size = 2,

        col = {
            active_border   = "rgba(d81e28ff)", -- Imperial warning red
            inactive_border = "rgba(2a2d31ff)", -- dark console grey
        },

        resize_on_border = false,
        allow_tearing    = false,
        layout = "dwindle",
    },

    decoration = {
        rounding = 0,   -- consoles have hard corners

        active_opacity   = 1.0,
        inactive_opacity = 1.0,

        shadow = {
            enabled = false,  -- flat screens, no glow
        },

        blur = {
            enabled = false,  -- crisp, no frosted glass
        },
    },

    animations = {
        enabled = true,
    },
})

-- Terminal feel: short, mechanical slides instead of springy pop-ins
hl.curve("snap",   { type = "bezier", points = { {0.2, 0.9}, {0.3, 1} } })
hl.curve("linear", { type = "bezier", points = { {0, 0},     {1, 1}   } })

hl.animation({ leaf = "global",     enabled = true, speed = 6, bezier = "snap" })
hl.animation({ leaf = "border",     enabled = true, speed = 3, bezier = "linear" })
hl.animation({ leaf = "windows",    enabled = true, speed = 3, bezier = "snap", style = "slide" })
hl.animation({ leaf = "windowsOut", enabled = true, speed = 2, bezier = "linear", style = "slide" })
hl.animation({ leaf = "fade",       enabled = true, speed = 2, bezier = "linear" })
hl.animation({ leaf = "layers",     enabled = true, speed = 3, bezier = "snap", style = "fade" })
hl.animation({ leaf = "workspaces", enabled = true, speed = 3, bezier = "snap", style = "slidevert" })

hl.config({
    misc = {
        background_color = 0xff050506, -- console black (ARGB)
    },
})
