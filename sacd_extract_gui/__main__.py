# File: main.py
import contextlib
import logging
import os
import re
import subprocess
import sys
import time

from PySide6.QtCore import QCoreApplication, QFile, QIODevice, QProcess, Qt, Slot
from PySide6.QtGui import QIcon, QScreen
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox

TOOL = "sacd_extract"
PROG = "Yet another sacd_extract GUI"
VERSION = "0.1.0"
AUTHOR = "Copyright (C) 2024, by Michael John"
DESC = "TBD"
GithubLink = "https://github.com/amstelchen/sacd-extract-gui"

Vlang = ["us", "ru", "de", "es", "fr", "it"]
Tlang = Vlang + ["nl", "po", "cz"]

sheet = """
QGroupBox {
    border: 1px solid gray;
    border-radius: 5px;
    margin-top: 1ex; /* leave space at the top for the title */
}

QGroupBox::title {
    margin-left: 0px;
    subcontrol-origin: margin;
    subcontrol-position: top left; /* position at the top center */
    padding: 0 3px;
}"""


def ReadConfigFile(ConfigPath: str, window):
    """config_lines = {}
    if os.path.exists(ConfigPath):
        with open(os.path.join(ConfigPath, "user.cfg"), "r") as config_file:
        logging.debug(f"Finished. {len(config_lines)} configuration options read.")
    """
    pass

def main():

    if len(sys.argv) > 1:
        loglevel = sys.argv[1]
    else:
        loglevel = "INFO"
    numeric_level = getattr(logging, loglevel.upper(), logging.INFO)
    # logging.debug(loglevel, numeric_level)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(
        format='%(levelname)s:%(asctime)s:%(filename)s:%(lineno)d:%(message)s',
        level=numeric_level)

    # Create a QProcess instance
    process = QProcess()

    def buttonBrowseInput_clicked(s):
        dialog = QFileDialog()
        #dialog.setFileMode(QFileDialog.Directory)
        dialog.setFileMode(QFileDialog.ExistingFile)
        #dialog.setOption(QFileDialog.ShowDirsOnly)
        # directory = dialog.getExistingDirectory(
        #     window, 'Choose Directory', 
        #     window.Steaminstallpath.text())
        file = dialog.getOpenFileName(window)
        if len(file[0]) > 0:
            logging.debug(f"Selected file: {file}")
            window.InputfilesPath.setText(file[0])

    def buttonBrowseConfig_clicked(s):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly)
        directory = dialog.getExistingDirectory(
            window, 'Choose Directory', 
            window.ConfigfilePath.text())
        logging.debug(f"Selected directory: {directory}")
        window.ConfigfilePath.setText(directory)
        ReadConfigFile(directory, window)

    def buttonBrowseExecutable_clicked(s):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly)
        directory = dialog.getExistingDirectory(
            window, 'Choose Directory', 
            os.path.curdir)
        logging.debug(f"Selected directory: {directory}")
        if len(directory) > 0:
            window.ExecutablePath.setText(directory) # TODO

    def buttonBrowseOutput_clicked(s):
        """if os.path.exists(window.Savedgamespath.text()):
            if sys.platform == "linux":
                subprocess.run(["xdg-open", window.Savedgamespath.text()])
            if sys.platform == "win32":
                path = os.path.normpath(window.Savedgamespath.text())
                subprocess.run(["explorer", path])
        """
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly)
        directory = dialog.getExistingDirectory(
            window, 'Choose Directory', 
            os.path.curdir)
        logging.debug(f"Selected directory: {directory}")
        if len(directory) > 0:
            window.OutputPath.setText(directory) # TODO

    def buttonAbout_clicked(s):
        QMessageBox.about(window, 
            f"{PROG} {VERSION}", 
            f"{PROG}\n{VERSION}\n{DESC}\n{AUTHOR}")

    def buttonDonate_clicked(s):
        if sys.platform == "linux":
            subprocess.run(["xdg-open", GithubLink])

    def buttonReportABug_clicked(s):
        if sys.platform == "linux":
            logging.debug(f"Opening {GithubLink}")
            subprocess.run(["xdg-open", GithubLink + "/issues/new"])

    def buttonStart_clicked(s):
        # ExecutablePath = [window.ExecutablePath.text()]
        ExecutablePath = []

        if window.comboBox_Channels.currentText() == "Stereo":
            ExecutablePath.append("-2")
        else:
            ExecutablePath.append("-m")

        if window.comboBox_Format.currentText() == "DSDIFF Edit Master":
            ExecutablePath.append("--output-dsdiff-em")
            switch = "-o"
        if window.comboBox_Format.currentText() == "DSDIFF":
            ExecutablePath.append("--output-dsdiff")
            switch = "-o"
        if window.comboBox_Format.currentText() == "Sony DSF":
            ExecutablePath.append("--output-dsf")
            switch = "-y"

        if window.checkBox_g_dsf_nopad.isChecked():
            ExecutablePath.append("--dsf-nopad")
        if window.checkBox_g_output_iso.isChecked():
            ExecutablePath.append("-output-iso")
        if window.checkBox_g_convert_dst.isChecked():
            ExecutablePath.append("--convert-dst")
        if window.checkBox_g_export_cue.isChecked():
            ExecutablePath.append("--export-cue")
        if window.checkBox_g_print.isChecked():
            ExecutablePath.append("--print")
        if window.checkBox_g_artist.isChecked():
            ExecutablePath.append("--artist")
        if window.checkBox_g_performer.isChecked():
            ExecutablePath.append("--performer")
        if window.checkBox_g_pauses.isChecked():
            ExecutablePath.append("--pauses")

        ExecutablePath.append("-i " + "\"" + window.InputfilesPath.text() + "\"")

        if len(window.OutputPath.text()) > 0:
            ExecutablePath.append(switch + " " + "\"" + window.OutputPath.text() + "\"")

        if len(window.ConfigfilePath.text()) > 0:
            if os.path.exists(window.ConfigfilePath.text()):
                cwd = window.ConfigfilePath.text()
        else:
            cwd = os.path.expanduser('~')
            logging.debug(f"Current working directory: {cwd}")

        # Connect the finished signal to the process_finished slot
        process.finished.connect(process_finished)

        # Connect the readyReadStandardOutput signal to the process_output slot
        process.readyReadStandardOutput.connect(process_output)
        process.readyReadStandardError.connect(process_stderr)

        window.ButtonStart.clicked.disconnect(buttonStart_clicked)
        window.ButtonStart.clicked.connect(kill_process)

        if sys.platform == "linux":
            path = window.ExecutablePath.text() + " " + ' '.join(ExecutablePath)
            logging.debug(f"Running {path}...")
            # result = subprocess.Popen(' '.join(ExecutablePath),
            #   stdout=subprocess.PIPE,
            #   stderr=subprocess.PIPE, shell=True, cwd=cwd)
            window.ButtonStart.setText("Stop conversion")
            window.ButtonStart.setStyleSheet("background-color: rgb(255, 0, 0);")
            process.startCommand(path)
            # process.waitForFinished(-1) # this will block the GUI
        if sys.platform == "win32":
            # TODO: not implemented
            pass
            # subprocess.run([window.ExecutablePath.text()])
        #logging.debug(result.stdout.read().decode("utf8"))
        #logging.debug(result.stderr.read().decode("utf8"))

    def message(self, s):
        self.text.appendPlainText(s)

    def kill_process():
        process.kill()
        process.close()
        window.ButtonStart.clicked.disconnect(kill_process)
        # window.ButtonStart.clicked.connect(buttonStart_clicked)

    # Define a function to handle when the process finishes
    @Slot(int, QProcess.ExitStatus)
    def process_finished(exit_code, exit_status):
        print("Process finished with exit code:", exit_code)
        time.sleep(1)
        process.close()
        # if exit_code == 9:
        window.ButtonStart.setText("Start conversion")
        window.ButtonStart.setStyleSheet("background-color: rgb(0, 170, 0);")
        # window.ButtonStart.clicked.disconnect(kill_process)
        window.ButtonStart.clicked.connect(buttonStart_clicked)

    @Slot()
    def process_output():
        try:
            data = process.readAllStandardOutput().data().decode().strip()
            # Example: Assume progress info is in the format "Progress: XX%"
            progress_pattern = r"Completed: (\d+)%.*Total: (\d+)%"
            match = re.match(progress_pattern, data)
            if match:
                # completed_progress = int(match.group(1))
                # total_progress = int(match.group(2))
                # logging.debug(f"{completed_progress}/{total_progress}")
                logging.debug(data)
            window.plainTextEdit.appendPlainText(data)
        except UnicodeDecodeError:
            pass
    
    @Slot()
    def process_stderr():
        try:
            data = process.readAllStandardError().data().decode().strip()
            window.plainTextEdit.appendPlainText(data)
        except UnicodeDecodeError:
            pass
        
    def check_version():
        window.plainTextEdit.appendPlainText(f"Checking for the existence of {TOOL}...")
        # installed = subprocess.run([TOOL, "-v"], 
        #   capture_output=True).stdout.decode('utf-8')
        process = QProcess()
        process.start(TOOL, ["-v"])
        # process.waitForReadyRead(-1)
        process.waitForFinished(-1)
        installed = process.readAllStandardOutput().data().decode('utf-8')[:-1]
        window.plainTextEdit.appendPlainText(installed)

    # os.environ["PYSIDE_DESIGNER_PLUGINS"]=os.path.dirname(__file__)
    os.environ["MESA_DEBUG"] = "silent"  # https://bugzilla.mozilla.org/show_bug.cgi?id=1744389
    # logging.debug(os.path.dirname(__file__))
    # app = QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # app = QApplication.setAttribute(Qt.AA_ShareOpenGLContexts, False)
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    app = QApplication(sys.argv)
    app.setStyleSheet(sheet)

    ui_file_name = os.path.dirname(__file__) + "/sacd_gui.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        logging.error(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    # loader.pluginPaths = [None]
    # loader.clearPluginPaths()
    with contextlib.redirect_stderr(open(os.devnull, 'w')):
        window = loader.load(ui_file)
        logging.debug("UI initialized.")
    ui_file.close()
    if not window:
        logging.error(loader.errorString())
        sys.exit(-1)

    center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
    # rect = QScreen.geometry(QApplication.primaryScreen())
    # width, height = rect.width(), rect.height()

    geo = window.frameGeometry()
    geo.moveCenter(center)
    window.move(geo.topLeft())

    icon = QIcon(os.path.dirname(__file__) + "/sacd_gui.png")
    window.setWindowIcon(icon)
    window.setWindowTitle(PROG + " " + VERSION)
    window.show()

    # TODO: only in DEBUG
    window.InputfilesPath.setText("/run/media/mic/MEDION/SACD/TOTO IV.iso")
    window.OutputPath.setText("/run/media/mic/MEDION/SACD")
    #window.Configfilepath.setText(ConfigPath)
    window.ExecutablePath.setText(TOOL)

    print(PROG + ' ' + VERSION + '\n' + AUTHOR) 

    #ReadConfigFile(ConfigPath, window)
    check_version()

    #window.lineEdit_Width.setText(str(width))
    #window.lineEdit_Height.setText(str(height))

    window.pushButtonBrowseInput.clicked.connect(buttonBrowseInput_clicked)
    window.pushButtonBrowseConfig.clicked.connect(buttonBrowseConfig_clicked)
    window.pushButtonBrowseExecutable.clicked.connect(buttonBrowseExecutable_clicked)
    window.pushButtonBrowseOutput.clicked.connect(buttonBrowseOutput_clicked)

    window.ButtonStart.clicked.connect(buttonStart_clicked)

    window.ButtonDonate.clicked.connect(buttonDonate_clicked)
    window.ButtonReportABug.clicked.connect(buttonReportABug_clicked)

    #window.comboBoxResolution.currentIndexChanged.connect(comboBoxResolution_changed)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
