import pwd
import sys
import os
import json
import argparse
import urllib.request
from PyQt5.QtWidgets import QApplication

import transphire
from transphire import transphire_utils as tu
from transphire.mainwindow import MainWindow
from transphire.loadwindow import DefaultSettings
from transphire import selectdialog


app = QApplication([])

a = selectdialog.SelectDialog()
a.start_retrain(
    {
        'project_folder': '/home/em-transfer-user/projects/2020_08_04_pmca_nptn_gf_krios1_superres_K3/TranSPHIRE_results',
        'log_folder': '/home/em-transfer-user/projects/2020_08_04_pmca_nptn_gf_krios1_superres_K3/TranSPHIRE_results/XXX_Log_files',
        'Path': {
            'e2proc2d.py': '/home/em-transfer-user/applications/sphire/v1.3/bin/e2proc2d.py',
            'sp_cinderella_train.py': '/home/em-transfer-user/applications/miniconda/v3.6.5/envs/cryolo_1.7.4/bin/sp_cinderella_train.py',
            'sp_cinderella_predict.py': '/home/em-transfer-user/applications/miniconda/v3.6.5/envs/cryolo_1.7.4/bin/sp_cinderella_train.py',
            },
        'Copy': {
            'Select2d': 'sp_cinderella_predict.py'
            }
        }
    )
a.enable(True)
a.show()

sys.exit(app.exec_())
