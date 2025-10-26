pragma Singleton
import QtQuick

QtObject {
    readonly property color background: "#0a0e27"
    readonly property color backgroundLight: "#131729"
    readonly property color backgroundPanel: "#1a1f3a"
    
    readonly property color primary: "#00d9ff"
    readonly property color primaryGlow: "#00a8cc"
    readonly property color secondary: "#0099cc"
    readonly property color accent: "#00ffff"
    
    readonly property color success: "#00ff88"
    readonly property color warning: "#ffaa00"
    readonly property color error: "#ff3366"
    readonly property color info: "#00aaff"
    
    readonly property color textPrimary: "#ffffff"
    readonly property color textSecondary: "#b0b8c8"
    readonly property color textMuted: "#6b7280"
    
    readonly property color highContrastBg: "#000000"
    readonly property color highContrastFg: "#ffffff"
    readonly property color highContrastAccent: "#ffff00"
    
    readonly property int spacing: 12
    readonly property int radius: 8
    readonly property int borderWidth: 1
    
    readonly property int fontSizeSmall: 11
    readonly property int fontSizeNormal: 14
    readonly property int fontSizeLarge: 18
    readonly property int fontSizeXLarge: 24
    
    readonly property string fontFamily: "Roboto, Arial, sans-serif"
    readonly property string fontFamilyMono: "Consolas, Monaco, monospace"
    
    property bool animationsEnabled: true
    readonly property int animationDuration: 300
    readonly property int animationDurationFast: 150
    readonly property int animationDurationSlow: 500
    
    function scaledFont(baseSize, scale) {
        return Math.round(baseSize * scale);
    }
    
    function glowColor(baseColor, intensity) {
        return Qt.lighter(baseColor, 1 + intensity);
    }
}
