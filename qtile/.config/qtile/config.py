# This is my Qtile configuration file for hostname TheThing. There are many like it, but this one is mine.
# Updated 2024-10-17

from libqtile import bar, layout, qtile, widget, extension
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()

# Define functions to move windows between monitors

def move_window_to_screen(qtile, window, screen):
    """Moves a window to a screen and focuses it, allowing you to move it
    further if you wish."""
    window.togroup(screen.group.name)
    qtile.focus_screen(screen.index)
    screen.group.focus(window, True)

@lazy.functions
def move_window_to_prev_screen(qtile):
    """Moves a window to the previous screen. Loops around the beginning and
    end."""
    index = qtile.current_screen.index
    index = index - 1 if index > 0 else len(qtile.screens) - 1
    move_window_to_screen(qtile, qtile.current_window, qtile.screens[index])

@lazy.function
def move_window_to_next_screen(qtile):
    """Moves a window to the next screen. Loops around the beginning and
    end."""
    index = qtile.current_screen.index
    index = index + 1 if index < len(qtile.screens) - 1 else 0
    move_window_to_screen(qtile, qtile.current_window, qtile.screens[index])

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html

    # Audio Control
    #Key([mod], "KP_0", lazy.spawn("amixer -q set Master toggle")),
    #Key([mod], "KP_Subtract", lazy.spawn("amixer -c 0 sset Master 1- unmute")),
    #Key([mod], "KP_Add", lazy.spawn("amixer -c 0 sset Master 1+ unmute")),

    # Rofi integration (not working)   

   # Key([], "menu", lazy.spawn('rofi -show drun'),desc="Run app"),
   # Key([mod, "shift"], 'Home', lazy.spawn('rofi -show run'),desc="Run Command"),
#    Key([mod], 'v', lazy.spawn('rofi -modi "clipboard:greenclip print" -show'),desc="Clipboard"),

    #dmenu integration
    Key([],"menu", lazy.run_extension(extension.DmenuRun(
        dmenu_prompt="Launch:",
        background="#1d1f21",
        foreground="#7BC0F5",
        selected_background="#E27OA4",
        selected_foreground="#1d1f21",
        dmenu_bottom=False,
        font="sans",
        fontsize=12,
        #dmenu_lines=42,
    ))),


    # Switch between windows
    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key([mod], "Prior", lazy.move_window_to_prev_screen(), desc='Prev mon'),
    Key([mod], "Next", lazy.move_window_to_next_screen(), desc='Next mon'),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

groups = [
    # Screen affinity here is used to make
    # sure the groups startup on the right screens
    Group(name="1", screen_affinity=0, layout="treetab"),
    Group(name="2", screen_affinity=0, layout="treetab"),
    Group(name="3", screen_affinity=0, layout="max"),
    Group(name="4", screen_affinity=1, layout="max"),
    Group(name="5", screen_affinity=1, layout="max"),
    Group(name="6", screen_affinity=1, layout="max"),
    Group(name="7", screen_affinity=2, layout="treetab"),
    Group(name="8", screen_affinity=2, layout="treetab"),
    Group(name="9", screen_affinity=2, layout="max")    
]

def go_to_group(name: str):
    def _inner(qtile):
        if len(qtile.screens) == 1:
            qtile.groups_map[name].toscreen()
            return

        elif name in '123':
            qtile.focus_screen(0)
            qtile.groups_map[name].toscreen()

        elif name in '456':
            qtile.focus_screen(1)
            qtile.groups_map[name].toscreen()
             
        else:
            qtile.focus_screen(2)
            qtile.groups_map[name].toscreen()

    return _inner

for i in groups:
    keys.append(Key([mod], i.name, lazy.function(go_to_group(i.name))))


def go_to_group_and_move_window(name: str):
    def _inner(qtile):
        if len(qtile.screens) == 1:
            qtile.current_window.togroup(name, switch_group=True)
            return

        elif name in "123":
            qtile.current_window.togroup(name, switch_group=False)
            qtile.focus_screen(0)
            qtile.groups_map[name].toscreen()

        elif name in "456":
            qtile.current_window.togroup(name, switch_group=False)
            qtile.focus_screen(1)
            qtile.groups_map[name].toscreen()

        else:
            qtile.current_window.togroup(name, switch_group=False)
            qtile.focus_screen(2)
            qtile.groups_map[name].toscreen()

    return _inner

for i in groups:
    keys.append(Key([mod, "shift"], i.name, lazy.function(go_to_group_and_move_window(i.name))))

layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # Try more layouts by unleashing below layouts.
     layout.Max(),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Floating(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
     layout.TreeTab()
    # layout.VerticalTile(),
    # layout.Zoomy()
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

# Triple Monitor Config

screens = [

    Screen( # Left: DP-1 
     wallpaper='~/Pictures/Wallpaper/Wallpaper002.jpg',
     wallpaper_mode='fill',   
     bottom=bar.Bar(
            [
                widget.GroupBox(visible_groups=['1', '2', '3']),
                widget.CurrentLayout(),
                widget.WindowName(),
                widget.Spacer(length=1750),
                widget.Net(interface='enp8s0',format='{down:.0f}{down_suffix} ↓↑ {up:.0f}{up_suffix}'),
            ],
            24,
            ),
          ),

    Screen( # Center: HDMI-A-1
    wallpaper='~/Pictures/Wallpaper/Wallpaper043.jpg',
    wallpaper_mode='fill',   
        bottom=bar.Bar(
            [
                widget.GroupBox(visible_groups=['4', '5', '6']),
                widget.CurrentLayout(),
                widget.WindowName(),
                widget.StatusNotifier(),
                widget.Systray(),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                widget.QuickExit(default_text='Exit'),
            ],
            24,
            ),
        ),

    Screen( # Right: DVI-D-1
    wallpaper='~/Pictures/Wallpaper/Wallpaper044.jpg',
    wallpaper_mode='fill',   
     bottom=bar.Bar(
            [
                widget.GroupBox(visible_groups=['7','8', '9']),
                widget.CurrentLayout(),
                widget.WindowName(),
                widget.Spacer(Length=1650),
                widget.Cmus(),
                widget.Volume(),
            ],
            24,
            ),
          ),
] 

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
