import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    color: Theme.backgroundPanel
    radius: Theme.radius
    border.color: Theme.accent
    border.width: 1
    
    property bool highContrast: false
    property real fontScale: 1.0
    
    Rectangle {
        anchors.fill: parent
        anchors.margins: 1
        color: "transparent"
        radius: Theme.radius
        
        gradient: Gradient {
            GradientStop { position: 0.0; color: Qt.rgba(0, 1, 1, 0.05) }
            GradientStop { position: 1.0; color: "transparent" }
        }
    }
    
    Column {
        anchors.fill: parent
        anchors.margins: Theme.spacing
        spacing: Theme.spacing
        
        Row {
            width: parent.width
            spacing: Theme.spacing
            
            Rectangle {
                width: 4
                height: titleText.height
                color: Theme.accent
                radius: 2
            }
            
            Text {
                id: titleText
                text: "SYSTEM METRICS"
                font.pixelSize: Theme.scaledFont(Theme.fontSizeLarge, fontScale)
                font.family: Theme.fontFamily
                font.bold: true
                color: highContrast ? Theme.highContrastAccent : Theme.accent
            }
        }
        
        Rectangle {
            width: parent.width
            height: 1
            color: Theme.accent
            opacity: 0.3
        }
        
        GridLayout {
            width: parent.width
            height: parent.height - titleText.height - Theme.spacing * 3 - 1
            columns: 2
            rowSpacing: Theme.spacing
            columnSpacing: Theme.spacing
            
            MetricItem {
                Layout.fillWidth: true
                Layout.fillHeight: true
                label: "CPU"
                value: dashboard.metrics.cpu !== undefined ? dashboard.metrics.cpu.toFixed(1) + "%" : "N/A"
                percentage: dashboard.metrics.cpu || 0
                accentColor: Theme.primary
                highContrast: root.highContrast
                fontScale: root.fontScale
            }
            
            MetricItem {
                Layout.fillWidth: true
                Layout.fillHeight: true
                label: "MEMORY"
                value: dashboard.metrics.memory !== undefined ? dashboard.metrics.memory.toFixed(1) + "%" : "N/A"
                percentage: dashboard.metrics.memory || 0
                accentColor: Theme.success
                highContrast: root.highContrast
                fontScale: root.fontScale
            }
            
            MetricItem {
                Layout.fillWidth: true
                Layout.fillHeight: true
                label: "DISK"
                value: dashboard.metrics.disk !== undefined ? dashboard.metrics.disk.toFixed(1) + "%" : "N/A"
                percentage: dashboard.metrics.disk || 0
                accentColor: Theme.warning
                highContrast: root.highContrast
                fontScale: root.fontScale
            }
            
            MetricItem {
                Layout.fillWidth: true
                Layout.fillHeight: true
                label: "NETWORK"
                value: dashboard.metrics.network_in !== undefined ? 
                       "↓" + dashboard.metrics.network_in.toFixed(1) + " MB" : "N/A"
                percentage: Math.min((dashboard.metrics.network_in || 0) / 100, 100)
                accentColor: Theme.info
                highContrast: root.highContrast
                fontScale: root.fontScale
            }
        }
    }
    
    component MetricItem: Rectangle {
        property string label: ""
        property string value: ""
        property real percentage: 0
        property color accentColor: Theme.primary
        property bool highContrast: false
        property real fontScale: 1.0
        
        color: Qt.rgba(0, 0, 0, 0.3)
        radius: Theme.radius / 2
        border.color: accentColor
        border.width: 1
        
        Column {
            anchors.fill: parent
            anchors.margins: Theme.spacing / 2
            spacing: 4
            
            Text {
                text: label
                font.pixelSize: Theme.scaledFont(Theme.fontSizeSmall, fontScale)
                font.family: Theme.fontFamily
                font.bold: true
                color: highContrast ? Theme.highContrastAccent : accentColor
            }
            
            Text {
                text: value
                font.pixelSize: Theme.scaledFont(Theme.fontSizeXLarge, fontScale)
                font.family: Theme.fontFamilyMono
                font.bold: true
                color: highContrast ? Theme.highContrastFg : Theme.textPrimary
            }
            
            Item { height: 4 }
            
            Rectangle {
                width: parent.width
                height: 8
                color: Qt.rgba(0, 0, 0, 0.5)
                radius: 4
                border.color: accentColor
                border.width: 1
                
                Rectangle {
                    width: parent.width * Math.min(percentage / 100, 1)
                    height: parent.height
                    radius: 4
                    color: accentColor
                    
                    Behavior on width {
                        NumberAnimation { duration: Theme.animationDuration }
                    }
                    
                    Rectangle {
                        anchors.fill: parent
                        radius: 4
                        color: "transparent"
                        border.color: Qt.lighter(accentColor, 1.5)
                        border.width: 1
                        opacity: 0.5
                    }
                }
            }
        }
        
        Rectangle {
            anchors.fill: parent
            radius: Theme.radius / 2
            color: "transparent"
            border.color: accentColor
            border.width: 1
            opacity: 0.3
            
            SequentialAnimation on opacity {
                running: percentage > 80 && Theme.animationsEnabled
                loops: Animation.Infinite
                NumberAnimation { from: 0.3; to: 0.8; duration: 1000 }
                NumberAnimation { from: 0.8; to: 0.3; duration: 1000 }
            }
        }
    }
}
