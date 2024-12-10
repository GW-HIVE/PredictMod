import matplotlib.pyplot as plt
import io

from base64 import b64encode
from sklearn.metrics import ConfusionMatrixDisplay


def CMtoCMDisplay(cm, labels=None):
    buf = io.BytesIO()
    if not labels:
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot()
        plt.savefig(buf, format="png", bbox_inches="tight")
        return b64encode(buf.getvalue()).decode("utf-8").replace("\n", "")
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot()
    plt.savefig(buf, format="png", bbox_inches="tight")
    return b64encode(buf.getvalue()).decode("utf-8").replace("\n", "")
