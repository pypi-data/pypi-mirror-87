import QtQuick 2.3
import Pyblish 0.1
import Pyblish.ListItems 0.1 as ListItem


ListView {
    id: list

    signal itemToggled(int index)
    signal itemDoubleClicked(int index)
    signal itemRightClicked(int index)
    signal actionTriggered(Action action, int index)

    width: 200
    height: 300

    clip: true

    boundsBehavior: Flickable.DragOverBounds
    pixelAligned: true

    delegate: ListItem.StandardActions {
        text: object.label || object.name
        active: object.optional
        checked: object.isToggled
        hidden: object.isHidden

        width: parent.width

        status: {
            if (object.isProcessing)
                return "processing"
            if (object.hasError)
                return "error"
            if (object.hasWarning)
                return "warning"
            if (object.succeeded)
                return "success"
            return "default"
        }

        onToggled: itemToggled(index)
        onPressed: itemRightClicked(index)

        actions: [
            Action {
                name: "repair"
                iconName: "wrench"
                enabled: object.hasError && object.hasRepair ? true : false
                onTriggered: actionTriggered(this, index)
            },

            Action {
                name: "legacyWarning"
                iconName: "exclamation-triangle"
                iconSize: 12
                tooltip: "This plug-in uses deprecated functionality"
                enabled: object.pre11 ? true : false
            },

            Action {
                name: "actionIcon"
                iconName: "adn"
                iconSize: 12
                tooltip: "This plug-in has actions"
                enabled: object.actionsIconVisible ? true : false
                color: object.actionPending ? "white"
                     : object.actionHasError ? Theme.dark.errorColor
                     : Theme.dark.successColor
            },

            Action {
                name: "enter"
                iconName: "angle-right"
                onTriggered: actionTriggered(this, index)
            }
        ]

    }
}
