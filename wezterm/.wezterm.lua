-- Wezterm Config for TheThing

-- WEZTERM API - DO NOT CHANGE
local wezterm = require 'wezterm'

-- CONFIG BUILDER - DO NOT CHANGE
local config = wezterm.config_builder()

-- START CONFIGURATION SETTINGS

-- Set color scheme:
config.color_scheme = 'Argonaut'

-- Set Font
config.font = wezterm.font 'JetBrains Mono'



-- Toggle Full Screen
config.keys = {
  {
    key = 'n',
    mods = 'SHIFT|CTRL',
    action = wezterm.action.ToggleFullScreen,
  },
}

-- END CONFIGURATION SETTINGS

-- RETURN CONFIG TO WEZTERM - DO NOT CHANGE
return config
