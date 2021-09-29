import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.12
import QtMultimedia 5.9
import QtQuick.Dialogs 1.0
import Qt.labs.folderlistmodel 2.1
import Qt.labs.platform 1.0

ApplicationWindow {
    id: main
    width: 1400
    height: 600
    visible: true

    Material.theme: Material.System
    Material.accent: Material.Purple

    ColumnLayout{
        anchors {
          left: parent.left
          right: parent.right
          top: parent.top
          leftMargin: 30
          topMargin: 30
        }
        RowLayout {
            ColumnLayout{
                Label {
                    text: qsTr("Camera image")
                    font.pixelSize: 22
                }
                Image{
                    id: preview
                    width: 500
                    height: 500
                    sourceSize.width: 300
                    sourceSize.height: 500
                    cache: false
                    fillMode: Image.PreserveAspectFit
                    // source: "image://myprovider"
                    // source: "0.0000.jpg"
                }
                Connections{
                    target: camera
                    function onEmit_Qimage() {
                        preview.source= ""
                        preview.source= "image://myprovider"
                    }
                }
            }

            ColumnLayout{
                Label {
                    text: qsTr("Processed image")
                    font.pixelSize: 22
                }
                Image{
                    id: enhance
                    width: 500
                    height: 500
                    sourceSize.width: 300
                    sourceSize.height: 500
                    cache: false
                    fillMode: Image.PreserveAspectFit
                    // source: "0.0000.jpg"
                }
                Connections{
                    target: processor
                    function onEmit_Processed() {
                        enhance.source= ""
                        enhance.source= "image://processprovider"
                    }
                }
            }

            ToolSeparator {
                Layout.fillHeight: true
            }

            ColumnLayout{
                RowLayout {
                    Layout.preferredHeight: 40
                    Layout.fillWidth: true
                    TextField {
                        id: path
                        enabled: false
                        text: folderModel.folder
                        Layout.fillWidth: true
                    }
                    Button {
                        text: "..."
                        onClicked: folderDialog.open();
                    }
                }

                Component {
                    id: highlight
                    Rectangle {
                        id: rooot
                        width: 180; height: 20
                        color: ListView.isCurrentItem ? "black" : "grey"; radius: 5
                        y: list.currentItem.y
                        Behavior on y {
                            SpringAnimation {
                                spring: 3
                                damping: 0.2
                            }
                        }
                    }
                }


                ListView {
                    id: list
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    model: FolderListModel {
                        id: folderModel
                        // folder: "file:///"+"read"
                        folder: ""
                        showDirs: false
                        nameFilters: ["*.tif", "*.png", "*.jpg", "*.avi", "*.mp4"]
                    }
                    highlight: highlight
                    highlightFollowsCurrentItem: false
                    focus: true
                    delegate: Text {
                        text: fileName
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                list.currentIndex = index
                                camera.setImage(folderModel.get(list.currentIndex, "filePath"))
                            }
                        }
                    }
                }
                FolderDialog {
                    id: folderDialog
                    currentFolder: ""
                    folder: StandardPaths.standardLocations(StandardPaths.PicturesLocation)[0]
                    onFolderChanged: {
                        folderModel.folder = folder;
                        watcher.updatepath(folderModel.folder)
                    }
                }

                CheckBox {
                    checked: true
                    text: qsTr("Blurring filter")
                    onClicked: {
                        processor.setblur()
                    }
                }

                CheckBox {
                    checked: true
                    text: qsTr("Crop")
                    onClicked: {
                        processor.setcrop()
                    }
                }

                RowLayout{
                    TextInput {
                        text: "CLAHE Blocksize"
                        cursorVisible: false

                    }
                    TextField {
                        id: blksize
                        text: "28"
                        onEditingFinished:{
                            processor.setblksize(blksize.text)
                        }
                    }

                }

                RowLayout{
                    TextInput {
                        text: "CLAHE ClipLimit"
                        cursorVisible: false

                    }
                    TextField {
                        id: clip
                        text: "3.0"
                        onEditingFinished:{
                            processor.setclip(clip.text)
                        }
                    }

                }

                RowLayout{
                    TextInput {
                        text: "Rolling ball radius"
                        cursorVisible: false
                    }
                    TextField {
                        id: radius
                        text: "0"
                        onEditingFinished:{
                            processor.setradius(radius.text)
                        }
                    }

                }

                RowLayout{
                    TextInput {
                        text: "fps"
                        cursorVisible: false
                    }
                    TextField {
                        id: fps
                        text: "8.0"
                        onEditingFinished:{
                            
                        }
                    }

                }

                FileDialog {
                    id: bgDialog
                    currentFile: ""
                    nameFilters: ["Images (*.jpg)","Images (*.tif)","Images (*.png)"]
                    folder: folderModel.folder
                    onAccepted: {
                        var path = this.currentFile.toString()
                        var c = this.folder.toString()
                        path = path.replace(c,"")
                        background.text = path
                        processor.subtract_bg(c+path)
                    }

                }
                RowLayout{
                    Button {
                        text: "Saturated Background"
                        onClicked: {
                            bgDialog.open()
                        }
                    }
                    TextInput {
                        id: background
                        text: ""
                    }

                }

                Button{
                    id: apply
                    text: qsTr("Apply")
                    onClicked: {
                        processor.updateimage()
                    }
                }
                FileDialog {
                    id: saveDialog
                    fileMode: FileDialog.SaveFile
                    currentFile: ""
                    nameFilters: ["Images (*.jpg)","Images (*.tif)","Images (*.png)", "Videos (*.avi)", "All files (*)"]
                    folder: folderModel.folder
                    // onAccepted: apply.text = currentFile
                    onAccepted: processor.saveimage(currentFile)
                }
                Button{
                    id: save
                    text: qsTr("Save")
                    onClicked: saveDialog.open();
                }
            }
        }
    }
}
