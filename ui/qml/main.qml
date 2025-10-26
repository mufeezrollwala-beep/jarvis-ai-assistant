import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

Window {
    id: mainWindow
    visible: true
    width: 1600
    height: 900
    minimumWidth: 1280
    minimumHeight: 720
    title: "J.A.R.V.I.S - Just A Rather Very Intelligent System"
    color: Theme.background
    
    property bool highContrast: dashboard.highContrast
    property real fontScale: dashboard.fontScale
    
    Rectangle {
        id: backgroundLayer
        anchors.fill: parent
        color: highContrast ? Theme.highContrastBg : Theme.background
        
        Canvas {
            id: gridCanvas
            anchors.fill: parent
            opacity: highContrast ? 0.3 : 0.15
            
            onPaint: {
                var ctx = getContext("2d")
                ctx.clearRect(0, 0, width, height)
                
                ctx.strokeStyle = highContrast ? Theme.highContrastAccent : Theme.primary
                ctx.lineWidth = 1
                
                var spacing = 50
                for (var x = 0; x < width; x += spacing) {
                    ctx.beginPath()
                    ctx.moveTo(x, 0)
                    ctx.lineTo(x, height)
                    ctx.stroke()
                }
                
                for (var y = 0; y < height; y += spacing) {
                    ctx.beginPath()
                    ctx.moveTo(0, y)
                    ctx.lineTo(width, y)
                    ctx.stroke()
                }
            }
            
            Timer {
                interval: 30000
                running: true
                repeat: true
                onTriggered: gridCanvas.requestPaint()
            }
        }
        
        Canvas {
            id: particleCanvas
            anchors.fill: parent
            opacity: 0.4
            
            property var particles: []
            property int particleCount: 30
            
            Component.onCompleted: {
                for (var i = 0; i < particleCount; i++) {
                    particles.push({
                        x: Math.random() * width,
                        y: Math.random() * height,
                        vx: (Math.random() - 0.5) * 0.5,
                        vy: (Math.random() - 0.5) * 0.5,
                        radius: Math.random() * 2 + 1
                    })
                }
            }
            
            onPaint: {
                var ctx = getContext("2d")
                ctx.clearRect(0, 0, width, height)
                
                ctx.fillStyle = highContrast ? Theme.highContrastAccent : Theme.primary
                ctx.shadowColor = highContrast ? Theme.highContrastAccent : Theme.primary
                ctx.shadowBlur = 10
                
                for (var i = 0; i < particles.length; i++) {
                    var p = particles[i]
                    
                    p.x += p.vx
                    p.y += p.vy
                    
                    if (p.x < 0 || p.x > width) p.vx = -p.vx
                    if (p.y < 0 || p.y > height) p.vy = -p.vy
                    
                    ctx.beginPath()
                    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2)
                    ctx.fill()
                }
            }
            
            Timer {
                interval: 50
                running: Theme.animationsEnabled && !highContrast
                repeat: true
                onTriggered: particleCanvas.requestPaint()
            }
        }
    }
    
    Rectangle {
        id: topBar
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        height: 80
        color: Qt.rgba(0, 0, 0, 0.7)
        border.color: highContrast ? Theme.highContrastAccent : Theme.primary
        border.width: 2
        
        Rectangle {
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            height: 2
            
            gradient: Gradient {
                orientation: Gradient.Horizontal
                GradientStop { position: 0.0; color: "transparent" }
                GradientStop { position: 0.5; color: highContrast ? Theme.highContrastAccent : Theme.primary }
                GradientStop { position: 1.0; color: "transparent" }
            }
        }
        
        RowLayout {
            anchors.fill: parent
            anchors.margins: Theme.spacing
            spacing: Theme.spacing * 2
            
            Rectangle {
                width: 50
                height: 50
                radius: 25
                color: "transparent"
                border.color: highContrast ? Theme.highContrastAccent : Theme.primary
                border.width: 2
                
                Text {
                    anchors.centerIn: parent
                    text: "J"
                    font.pixelSize: Theme.scaledFont(Theme.fontSizeXLarge, fontScale)
                    font.family: Theme.fontFamily
                    font.bold: true
                    color: highContrast ? Theme.highContrastAccent : Theme.primary
                }
                
                SequentialAnimation on scale {
                    running: Theme.animationsEnabled
                    loops: Animation.Infinite
                    NumberAnimation { from: 1.0; to: 1.1; duration: 2000 }
                    NumberAnimation { from: 1.1; to: 1.0; duration: 2000 }
                }
            }
            
            Column {
                Layout.fillWidth: true
                spacing: 4
                
                Text {
                    text: "J.A.R.V.I.S SYSTEM INTERFACE"
                    font.pixelSize: Theme.scaledFont(Theme.fontSizeXLarge, fontScale)
                    font.family: Theme.fontFamily
                    font.bold: true
                    color: highContrast ? Theme.highContrastFg : Theme.textPrimary
                }
                
                Text {
                    text: dashboard.status.toUpperCase()
                    font.pixelSize: Theme.scaledFont(Theme.fontSizeSmall, fontScale)
                    font.family: Theme.fontFamilyMono
                    color: highContrast ? Theme.textSecondary : Theme.textSecondary
                }
            }
            
            Row {
                spacing: Theme.spacing
                
                Button {
                    text: highContrast ? "Normal" : "High Contrast"
                    font.pixelSize: Theme.scaledFont(Theme.fontSizeSmall, fontScale)
                    font.family: Theme.fontFamily
                    
                    background: Rectangle {
                        color: parent.pressed ? Theme.primary : Qt.rgba(0, 0.85, 1, 0.2)
                        border.color: highContrast ? Theme.highContrastAccent : Theme.primary
                        border.width: 1
                        radius: Theme.radius / 2
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: highContrast ? Theme.highContrastFg : Theme.textPrimary
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: dashboard.toggleContrast()
                }
                
                Button {
                    text: "A-"
                    font.pixelSize: Theme.scaledFont(Theme.fontSizeNormal, fontScale)
                    font.family: Theme.fontFamily
                    
                    background: Rectangle {
                        color: parent.pressed ? Theme.secondary : Qt.rgba(0, 0.6, 0.8, 0.2)
                        border.color: highContrast ? Theme.highContrastAccent : Theme.secondary
                        border.width: 1
                        radius: Theme.radius / 2
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: highContrast ? Theme.highContrastFg : Theme.textPrimary
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: dashboard.setFontScale(Math.max(0.5, fontScale - 0.1))
                }
                
                Button {
                    text: "A+"
                    font.pixelSize: Theme.scaledFont(Theme.fontSizeNormal, fontScale)
                    font.family: Theme.fontFamily
                    
                    background: Rectangle {
                        color: parent.pressed ? Theme.secondary : Qt.rgba(0, 0.6, 0.8, 0.2)
                        border.color: highContrast ? Theme.highContrastAccent : Theme.secondary
                        border.width: 1
                        radius: Theme.radius / 2
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: highContrast ? Theme.highContrastFg : Theme.textPrimary
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: dashboard.setFontScale(Math.min(2.0, fontScale + 0.1))
                }
            }
            
            Text {
                text: Qt.formatDateTime(new Date(), "hh:mm:ss")
                font.pixelSize: Theme.scaledFont(Theme.fontSizeLarge, fontScale)
                font.family: Theme.fontFamilyMono
                font.bold: true
                color: highContrast ? Theme.highContrastAccent : Theme.primary
                
                Timer {
                    interval: 1000
                    running: true
                    repeat: true
                    onTriggered: parent.text = Qt.formatDateTime(new Date(), "hh:mm:ss")
                }
            }
        }
    }
    
    GridLayout {
        id: mainGrid
        anchors.top: topBar.bottom
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: Theme.spacing
        
        columns: 3
        rows: 3
        columnSpacing: Theme.spacing
        rowSpacing: Theme.spacing
        
        ConversationPanel {
            Layout.row: 0
            Layout.column: 0
            Layout.rowSpan: 2
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredWidth: mainGrid.width * 0.35
            highContrast: mainWindow.highContrast
            fontScale: mainWindow.fontScale
        }
        
        TaskPanel {
            Layout.row: 0
            Layout.column: 1
            Layout.rowSpan: 2
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredWidth: mainGrid.width * 0.35
            highContrast: mainWindow.highContrast
            fontScale: mainWindow.fontScale
        }
        
        MetricsPanel {
            Layout.row: 0
            Layout.column: 2
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredWidth: mainGrid.width * 0.30
            Layout.preferredHeight: mainGrid.height * 0.45
            highContrast: mainWindow.highContrast
            fontScale: mainWindow.fontScale
        }
        
        MemoryPanel {
            Layout.row: 1
            Layout.column: 2
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredWidth: mainGrid.width * 0.30
            Layout.preferredHeight: mainGrid.height * 0.45
            highContrast: mainWindow.highContrast
            fontScale: mainWindow.fontScale
        }
        
        WaveformPanel {
            Layout.row: 2
            Layout.column: 0
            Layout.columnSpan: 3
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredHeight: mainGrid.height * 0.20
            highContrast: mainWindow.highContrast
            fontScale: mainWindow.fontScale
        }
    }
}
