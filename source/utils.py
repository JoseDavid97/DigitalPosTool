from PyQt5.QtWidgets import QMessageBox

def showAlert(type_msg = "Information", title = "Warning", msg = "Warning"):

    icon_map = {"Question":QMessageBox.Question, 
                "Information":QMessageBox.Information, 
                "Warning":QMessageBox.Warning, 
                "Critical":QMessageBox.Critical}

    msgBox = QMessageBox()
    msgBox.setIcon(icon_map[type_msg])
    msgBox.setText(msg)
    msgBox.setWindowTitle(title)

    if type_msg == "Question":
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        return msgBox
    else:
        msgBox.exec()