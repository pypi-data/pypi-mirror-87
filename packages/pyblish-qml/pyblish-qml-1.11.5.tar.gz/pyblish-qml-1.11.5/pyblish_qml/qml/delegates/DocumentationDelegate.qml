import QtQuick 2.3
import Pyblish 0.1


BaseGroupDelegate {
    item: Item {
        height: textArea.paintedHeight + 20

        TextArea {
            id: textArea

            font.family: "consolas"

            anchors.fill: parent
            anchors.margins: 10
            text: modelData.item.doc || "No documentation"
            onLinkActivated: Qt.openUrlExternally(link)

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.NoButton // we don't want to eat clicks on the Text
                cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
            }
        }
    }
}
