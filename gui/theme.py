import flet as ft

class ThemeColors:
    # Light Theme
    LIGHT_BG_PAGE = "#FAFAFA"
    LIGHT_BG_CARD = "#FFFFFF"
    LIGHT_TEXT_MAIN = "#1A1A1A"
    LIGHT_TEXT_GREY = "#8E8E93"
    LIGHT_PRIMARY = "#4E75F6"
    LIGHT_BG_LIGHT_BLUE = "#F0F4FF"
    LIGHT_BG_LIGHT_RED = "#FFF0F0"
    LIGHT_BG_LIGHT_GREEN = "#F0FFF4"
    LIGHT_SHADOW = "#08000000"
    LIGHT_SIDEBAR_BG = "#F6F6F6"
    LIGHT_SIDEBAR_BORDER = "#E5E5E5"

    # Dark Theme - Softer grays for better visual comfort
    DARK_BG_PAGE = "#121212"  # Soft dark gray instead of pure black
    DARK_BG_CARD = "#1E1E1E"  # Slightly lighter card
    DARK_TEXT_MAIN = "#E5E5E5"  # Softer white
    DARK_TEXT_GREY = "#98989D"
    DARK_PRIMARY = "#6B93FF"  # Brighter blue for dark mode
    DARK_BG_LIGHT_BLUE = "#1A2842"  # Deeper blue tint
    DARK_BG_LIGHT_RED = "#3D1F1F"  # Deeper red tint
    DARK_BG_LIGHT_GREEN = "#1F3D28"  # Deeper green tint
    DARK_SHADOW = "#10000000"  # Very subtle shadow
    DARK_SIDEBAR_BG = "#1A1A1A"  # Sidebar slightly darker than page
    DARK_SIDEBAR_BORDER = "#2A2A2A"  # Subtle border

class Palette:
    def __init__(self, is_dark):
        self.bg_page = ThemeColors.DARK_BG_PAGE if is_dark else ThemeColors.LIGHT_BG_PAGE
        self.bg_card = ThemeColors.DARK_BG_CARD if is_dark else ThemeColors.LIGHT_BG_CARD
        self.text_main = ThemeColors.DARK_TEXT_MAIN if is_dark else ThemeColors.LIGHT_TEXT_MAIN
        self.text_grey = ThemeColors.DARK_TEXT_GREY if is_dark else ThemeColors.LIGHT_TEXT_GREY
        self.primary = ThemeColors.DARK_PRIMARY if is_dark else ThemeColors.LIGHT_PRIMARY
        self.bg_light_blue = ThemeColors.DARK_BG_LIGHT_BLUE if is_dark else ThemeColors.LIGHT_BG_LIGHT_BLUE
        self.bg_light_red = ThemeColors.DARK_BG_LIGHT_RED if is_dark else ThemeColors.LIGHT_BG_LIGHT_RED
        self.bg_light_green = ThemeColors.DARK_BG_LIGHT_GREEN if is_dark else ThemeColors.LIGHT_BG_LIGHT_GREEN
        self.shadow = ThemeColors.DARK_SHADOW if is_dark else ThemeColors.LIGHT_SHADOW
        self.sidebar_bg = ThemeColors.DARK_SIDEBAR_BG if is_dark else ThemeColors.LIGHT_SIDEBAR_BG
        self.sidebar_border = ThemeColors.DARK_SIDEBAR_BORDER if is_dark else ThemeColors.LIGHT_SIDEBAR_BORDER

def get_palette(page: ft.Page):
    is_dark = page.platform_brightness == ft.Brightness.DARK
    return Palette(is_dark)
