import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    color: Theme.backgroundPanel
    radius: Theme.radius
    border.color: Theme.success
    border.width: 1
    
    property bool highContrast: false
    property real fontScale: 1.0
    
    Rectangle {
        anchors.fill: parent
        anchors.margins: 1
        color: "transparent"
        radius: Theme.radius
        
        gradient: Gradient {
            GradientStop { position: 0.0; color: Qt.rgba(0, 1, 0.53, 0.05) }
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
                color: Theme.success
                radius: 2
            }
            
            Text {
                id: titleText
                text: "MEMORY SNIPPETS"
                font.pixelSize: Theme.scaledFont(Theme.fontSizeLarge, fontScale)
                font.family: Theme.fontFamily
                font.bold: true
                color: highContrast ? Theme.highContrastAccent : Theme.success
            }
        }
        
        Rectangle {
            width: parent.width
            height: 1
            color: Theme.success
            opacity: 0.3
        }
        
        ListView {
            id: memoryView
            width: parent.width
            height: parent.height - titleText.height - Theme.spacing * 3 - 1
            clip: true
            spacing: Theme.spacing / 2
            
            model: dashboard.memory
            
            ScrollBar.vertical: ScrollBar {
                policy: ScrollBar.AsNeeded
                width: 8
                
                contentItem: Rectangle {
                    implicitWidth: 8
                    radius: 4
                    color: Theme.success
                    opacity: 0.5
                }
            }
            
            delegate: Rectangle {
                width: memoryView.width
                height: contentColumn.height + Theme.spacing
                color: Qt.rgba(0, 1, 0.53, 0.08)
                radius: Theme.radius / 2
                border.color: Theme.success
                border.width: 1
                
                Column {
                    id: contentColumn
                    width: parent.width - Theme.spacing
                    anchors.centerIn: parent
                    spacing: 4
                    
                    Row {
                        width: parent.width
                        spacing: Theme.spacing / 2
                        
                        Rectangle {
                            width: 8
                            height: 8
                            radius: 4
                            color: Theme.success
                            anchors.verticalCenter: parent.verticalCenter
                            
                            SequentialAnimation on scale {
                                running: Theme.animationsEnabled
                                loops: Animation.Infinite
                                NumberAnimation { from: 1.0; to: 1.3; duration: 1500 }
                                NumberAnimation { from: 1.3; to: 1.0; duration: 1500 }
                            }
                        }
                        
                        Text {
                            text: modelData.key
                            font.pixelSize: Theme.scaledFont(Theme.fontSizeSmall, fontScale)
                            font.family: Theme.fontFamily
                            font.bold: true
                            color: highContrast ? Theme.highContrastAccent : Theme.success
                        }
                        
                        Item { width: 1; height: 1 }
                        
                        Text {
                            text: new Date(modelData.timestamp).toLocaleTimeString()
                            font.pixelSize: Theme.scaledFont(Theme.fontSizeSmall - 1, fontScale)
                            font.family: Theme.fontFamilyMono
                            color: highContrast ? Theme.textSecondary : Theme.textMuted
                            anchors.verticalCenter: parent.verticalCenter
                        }
                    }
                    
                    Text {
                        text: modelData.value
                        font.pixelSize: Theme.scaledFont(Theme.fontSizeNormal, fontScale)
                        font.family: Theme.fontFamilyMono
                        color: highContrast ? Theme.highContrastFg : Theme.textPrimary
                        wrapMode: Text.WordWrap
                        width: parent.width
                        leftPadding: 15
                    }
                }
                
                Rectangle {
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    width: 2
                    color: Theme.success
                    
                    SequentialAnimation on opacity {
                        running: Theme.animationsEnabled
                        loops: Animation.Infinite
                        NumberAnimation { from: 0.2; to: 1.0; duration: 2000 }
                        NumberAnimation { from: 1.0; to: 0.2; duration: 2000 }
                    }
                }
            }
            
            add: Transition {
                NumberAnimation { properties: "opacity"; from: 0; to: 1; duration: Theme.animationDuration }
                NumberAnimation { properties: "scale"; from: 0.8; to: 1.0; duration: Theme.animationDuration }
            }
        }
    }
}
