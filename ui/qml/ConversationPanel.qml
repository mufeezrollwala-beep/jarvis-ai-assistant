import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    color: Theme.backgroundPanel
    radius: Theme.radius
    border.color: Theme.primary
    border.width: 1
    
    property bool highContrast: false
    property real fontScale: 1.0
    
    Rectangle {
        anchors.fill: parent
        anchors.margins: 1
        color: "transparent"
        radius: Theme.radius
        
        gradient: Gradient {
            GradientStop { position: 0.0; color: Qt.rgba(0, 0.85, 1, 0.05) }
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
                color: Theme.primary
                radius: 2
                
                SequentialAnimation on opacity {
                    running: Theme.animationsEnabled
                    loops: Animation.Infinite
                    NumberAnimation { from: 0.3; to: 1.0; duration: 1000 }
                    NumberAnimation { from: 1.0; to: 0.3; duration: 1000 }
                }
            }
            
            Text {
                id: titleText
                text: "CONVERSATION FEED"
                font.pixelSize: Theme.scaledFont(Theme.fontSizeLarge, fontScale)
                font.family: Theme.fontFamily
                font.bold: true
                color: highContrast ? Theme.highContrastAccent : Theme.primary
            }
        }
        
        Rectangle {
            width: parent.width
            height: 1
            color: Theme.primary
            opacity: 0.3
        }
        
        ListView {
            id: conversationView
            width: parent.width
            height: parent.height - titleText.height - Theme.spacing * 3 - 1
            clip: true
            spacing: Theme.spacing / 2
            
            model: dashboard.conversation
            
            ScrollBar.vertical: ScrollBar {
                policy: ScrollBar.AsNeeded
                width: 8
                
                contentItem: Rectangle {
                    implicitWidth: 8
                    radius: 4
                    color: Theme.primary
                    opacity: 0.5
                }
            }
            
            delegate: Item {
                width: conversationView.width
                height: messageColumn.height + Theme.spacing
                
                Column {
                    id: messageColumn
                    width: parent.width
                    spacing: 4
                    
                    Row {
                        spacing: Theme.spacing / 2
                        
                        Rectangle {
                            width: 6
                            height: 6
                            radius: 3
                            color: modelData.speaker === "User" ? Theme.accent : Theme.success
                            anchors.verticalCenter: speakerText.verticalCenter
                        }
                        
                        Text {
                            id: speakerText
                            text: modelData.speaker
                            font.pixelSize: Theme.scaledFont(Theme.fontSizeSmall, fontScale)
                            font.family: Theme.fontFamily
                            font.bold: true
                            color: highContrast ? Theme.highContrastFg : 
                                   (modelData.speaker === "User" ? Theme.accent : Theme.success)
                        }
                        
                        Text {
                            text: new Date(modelData.timestamp).toLocaleTimeString()
                            font.pixelSize: Theme.scaledFont(Theme.fontSizeSmall, fontScale)
                            font.family: Theme.fontFamilyMono
                            color: highContrast ? Theme.textSecondary : Theme.textMuted
                            anchors.verticalCenter: speakerText.verticalCenter
                        }
                    }
                    
                    Text {
                        text: modelData.message
                        font.pixelSize: Theme.scaledFont(Theme.fontSizeNormal, fontScale)
                        font.family: Theme.fontFamily
                        color: highContrast ? Theme.highContrastFg : Theme.textPrimary
                        wrapMode: Text.WordWrap
                        width: parent.width - 20
                        leftPadding: 15
                    }
                }
                
                Rectangle {
                    anchors.bottom: parent.bottom
                    width: parent.width
                    height: 1
                    color: Theme.primary
                    opacity: 0.1
                }
            }
            
            onCountChanged: {
                if (count > 0) {
                    positionViewAtEnd()
                }
            }
            
            add: Transition {
                NumberAnimation { properties: "opacity"; from: 0; to: 1; duration: Theme.animationDuration }
                NumberAnimation { properties: "y"; from: conversationView.height; duration: Theme.animationDuration }
            }
        }
    }
    
    layer.enabled: true
    layer.effect: ShaderEffect {
        fragmentShader: "
            varying highp vec2 qt_TexCoord0;
            uniform sampler2D source;
            uniform lowp float qt_Opacity;
            void main() {
                lowp vec4 color = texture2D(source, qt_TexCoord0);
                gl_FragColor = color * qt_Opacity;
            }
        "
    }
}
