import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    color: Theme.backgroundPanel
    radius: Theme.radius
    border.color: Theme.secondary
    border.width: 1
    
    property bool highContrast: false
    property real fontScale: 1.0
    
    Rectangle {
        anchors.fill: parent
        anchors.margins: 1
        color: "transparent"
        radius: Theme.radius
        
        gradient: Gradient {
            GradientStop { position: 0.0; color: Qt.rgba(0, 0.6, 0.8, 0.05) }
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
                color: Theme.secondary
                radius: 2
            }
            
            Text {
                id: titleText
                text: "TASK STATUS"
                font.pixelSize: Theme.scaledFont(Theme.fontSizeLarge, fontScale)
                font.family: Theme.fontFamily
                font.bold: true
                color: highContrast ? Theme.highContrastAccent : Theme.secondary
            }
            
            Item { 
                width: parent.width - titleText.width - countText.width - Theme.spacing * 3
                height: 1
            }
            
            Text {
                id: countText
                text: taskView.count + " tasks"
                font.pixelSize: Theme.scaledFont(Theme.fontSizeSmall, fontScale)
                font.family: Theme.fontFamilyMono
                color: highContrast ? Theme.textSecondary : Theme.textMuted
                anchors.verticalCenter: titleText.verticalCenter
            }
        }
        
        Rectangle {
            width: parent.width
            height: 1
            color: Theme.secondary
            opacity: 0.3
        }
        
        ListView {
            id: taskView
            width: parent.width
            height: parent.height - titleText.height - Theme.spacing * 3 - 1
            clip: true
            spacing: Theme.spacing / 2
            
            model: dashboard.tasks
            
            ScrollBar.vertical: ScrollBar {
                policy: ScrollBar.AsNeeded
                width: 8
                
                contentItem: Rectangle {
                    implicitWidth: 8
                    radius: 4
                    color: Theme.secondary
                    opacity: 0.5
                }
            }
            
            delegate: Rectangle {
                width: taskView.width
                height: 60
                color: Qt.rgba(0, 0.6, 0.8, 0.1)
                radius: Theme.radius / 2
                border.color: {
                    if (modelData.status === "completed") return Theme.success
                    if (modelData.status === "running") return Theme.warning
                    return Theme.info
                }
                border.width: 1
                
                Row {
                    anchors.fill: parent
                    anchors.margins: Theme.spacing / 2
                    spacing: Theme.spacing
                    
                    Rectangle {
                        width: 8
                        height: parent.height
                        radius: 4
                        color: {
                            if (modelData.status === "completed") return Theme.success
                            if (modelData.status === "running") return Theme.warning
                            return Theme.info
                        }
                        
                        SequentialAnimation on opacity {
                            running: modelData.status === "running" && Theme.animationsEnabled
                            loops: Animation.Infinite
                            NumberAnimation { from: 0.3; to: 1.0; duration: 800 }
                            NumberAnimation { from: 1.0; to: 0.3; duration: 800 }
                        }
                    }
                    
                    Column {
                        width: parent.width - 20
                        spacing: 4
                        anchors.verticalCenter: parent.verticalCenter
                        
                        Row {
                            width: parent.width
                            spacing: Theme.spacing
                            
                            Text {
                                text: modelData.id
                                font.pixelSize: Theme.scaledFont(Theme.fontSizeSmall, fontScale)
                                font.family: Theme.fontFamilyMono
                                color: highContrast ? Theme.textSecondary : Theme.textMuted
                            }
                            
                            Rectangle {
                                width: statusText.width + 12
                                height: statusText.height + 4
                                radius: 10
                                color: {
                                    if (modelData.status === "completed") return Qt.rgba(0, 1, 0.53, 0.2)
                                    if (modelData.status === "running") return Qt.rgba(1, 0.67, 0, 0.2)
                                    return Qt.rgba(0, 0.67, 1, 0.2)
                                }
                                border.color: {
                                    if (modelData.status === "completed") return Theme.success
                                    if (modelData.status === "running") return Theme.warning
                                    return Theme.info
                                }
                                border.width: 1
                                anchors.verticalCenter: parent.verticalCenter
                                
                                Text {
                                    id: statusText
                                    text: modelData.status.toUpperCase()
                                    font.pixelSize: Theme.scaledFont(Theme.fontSizeSmall - 1, fontScale)
                                    font.family: Theme.fontFamily
                                    font.bold: true
                                    color: {
                                        if (highContrast) return Theme.highContrastFg
                                        if (modelData.status === "completed") return Theme.success
                                        if (modelData.status === "running") return Theme.warning
                                        return Theme.info
                                    }
                                    anchors.centerIn: parent
                                }
                            }
                        }
                        
                        Text {
                            text: modelData.description
                            font.pixelSize: Theme.scaledFont(Theme.fontSizeNormal, fontScale)
                            font.family: Theme.fontFamily
                            color: highContrast ? Theme.highContrastFg : Theme.textPrimary
                            elide: Text.ElideRight
                            width: parent.width
                        }
                        
                        Text {
                            text: new Date(modelData.timestamp).toLocaleString()
                            font.pixelSize: Theme.scaledFont(Theme.fontSizeSmall - 1, fontScale)
                            font.family: Theme.fontFamilyMono
                            color: highContrast ? Theme.textSecondary : Theme.textMuted
                        }
                    }
                }
            }
            
            add: Transition {
                NumberAnimation { properties: "opacity"; from: 0; to: 1; duration: Theme.animationDuration }
                NumberAnimation { properties: "x"; from: -taskView.width; duration: Theme.animationDuration }
            }
        }
    }
}
