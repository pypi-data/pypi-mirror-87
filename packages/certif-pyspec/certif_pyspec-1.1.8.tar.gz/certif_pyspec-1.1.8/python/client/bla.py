
from pyspec.client.SpecConnection import QSpecConnection
from pyspec.graphics.QVariant import *
from pyspec.css_logger import log

log.start()

s = QSpecConnection("fourc")
def run_mac():
    answ = s.run_cmd("roi_cntmnes()")
    log.log(2, "got answer %s" % answ)

def update_conn():
    if not s.is_connected():
        log.log(2, "not connected")
    s.update_events()

app = QApplication([])
but = QPushButton("click")
timer = QTimer()
but.clicked.connect(run_mac)
but.show()
timer.timeout.connect(update_conn)
timer.start(100)
app.exec_()


