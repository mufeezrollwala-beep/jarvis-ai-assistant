import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    color: Theme.backgroundPanel
    radius: Theme.radius
    border.color: Theme.warning
    border.width: 1
    
    property bool highContrast: false
    property real fontScale: 1.0
    
    Rectangle {
        anchors.fill: parent
        anchors.margins: 1
        color: "transparent"
        radius: Theme.radius
        
        gradient: Gradient {
            GradientStop { position: 0.0; color: Qt.rgba(1, 0.67, 0, 0.05) }
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
                color: Theme.warning
                radius: 2
                
                SequentialAnimation on opacity {
                    running: Theme.animationsEnabled
                    loops: Animation.Infinite
                    NumberAnimation { from: 0.5; to: 1.0; duration: 500 }
                    NumberAnimation { from: 1.0; to: 0.5; duration: 500 }
                }
            }
            
            Text {
                id: titleText
                text: "AUDIO WAVEFORM"
                font.pixelSize: Theme.scaledFont(Theme.fontSizeLarge, fontScale)
                font.family: Theme.fontFamily
                font.bold: true
                color: highContrast ? Theme.highContrastAccent : Theme.warning
            }
            
            Item { 
                width: parent.width - titleText.width - liveIndicator.width - liveText.width - Theme.spacing * 4
                height: 1
            }
            
            Rectangle {
                id: liveIndicator
                width: 10
                height: 10
                radius: 5
                color: Theme.error
                anchors.verticalCenter: titleText.verticalCenter
                
                SequentialAnimation on opacity {
                    running: Theme.animationsEnabled
                    loops: Animation.Infinite
                    NumberAnimation { from: 0.3; to: 1.0; duration: 800 }
                    NumberAnimation { from: 1.0; to: 0.3; duration: 800 }
                }
            }
            
            Text {
                id: liveText
                text: "LIVE"
                font.pixelSize: Theme.scaledFont(Theme.fontSizeSmall, fontScale)
                font.family: Theme.fontFamily
                font.bold: true
                color: highContrast ? Theme.highContrastFg : Theme.error
                anchors.verticalCenter: titleText.verticalCenter
            }
        }
        
        Rectangle {
            width: parent.width
            height: 1
            color: Theme.warning
            opacity: 0.3
        }
        
        Item {
            width: parent.width
            height: parent.height - titleText.height - Theme.spacing * 3 - 1
            
            Canvas {
                id: waveformCanvas
                anchors.fill: parent
                
                property var audioData: dashboard.audioData
                
                onAudioDataChanged: {
                    requestPaint()
                }
                
                onPaint: {
                    var ctx = getContext("2d")
                    ctx.clearRect(0, 0, width, height)
                    
                    if (!audioData || audioData.length === 0) {
                        return
                    }
                    
                    var centerY = height / 2
                    var maxAmplitude = height / 2 - 10
                    
                    ctx.strokeStyle = Qt.rgba(1, 0.67, 0, 0.2)
                    ctx.lineWidth = 1
                    ctx.beginPath()
                    ctx.moveTo(0, centerY)
                    ctx.lineTo(width, centerY)
                    ctx.stroke()
                    
                    var gradient = ctx.createLinearGradient(0, 0, 0, height)
                    if (root.highContrast) {
                        gradient.addColorStop(0, Theme.highContrastAccent)
                        gradient.addColorStop(0.5, Theme.highContrastFg)
                        gradient.addColorStop(1, Theme.highContrastAccent)
                    } else {
                        gradient.addColorStop(0, Theme.warning)
                        gradient.addColorStop(0.5, Theme.accent)
                        gradient.addColorStop(1, Theme.warning)
                    }
                    
                    ctx.strokeStyle = gradient
                    ctx.lineWidth = 2
                    ctx.lineCap = "round"
                    ctx.lineJoin = "round"
                    
                    ctx.beginPath()
                    var stepX = width / (audioData.length - 1)
                    
                    for (var i = 0; i < audioData.length; i++) {
                        var x = i * stepX
                        var y = centerY - (audioData[i] * maxAmplitude)
                        
                        if (i === 0) {
                            ctx.moveTo(x, y)
                        } else {
                            ctx.lineTo(x, y)
                        }
                    }
                    ctx.stroke()
                    
                    ctx.strokeStyle = Qt.rgba(0, 0.85, 1, 0.3)
                    ctx.lineWidth = 1
                    ctx.beginPath()
                    
                    for (var i = 0; i < audioData.length; i++) {
                        var x = i * stepX
                        var y = centerY - (audioData[i] * maxAmplitude)
                        ctx.moveTo(x, centerY)
                        ctx.lineTo(x, y)
                    }
                    ctx.stroke()
                    
                    ctx.fillStyle = root.highContrast ? 
                        Qt.rgba(1, 1, 0, 0.6) : Qt.rgba(0, 0.85, 1, 0.6)
                    ctx.shadowColor = root.highContrast ? 
                        Theme.highContrastAccent : Theme.primary
                    ctx.shadowBlur = 10
                    
                    for (var i = 0; i < audioData.length; i++) {
                        var x = i * stepX
                        var y = centerY - (audioData[i] * maxAmplitude)
                        ctx.beginPath()
                        ctx.arc(x, y, 2, 0, Math.PI * 2)
                        ctx.fill()
                    }
                }
            }
            
            Rectangle {
                anchors.fill: parent
                color: "transparent"
                border.color: Theme.warning
                border.width: 1
                radius: Theme.radius / 2
                opacity: 0.2
            }
        }
    }
}
