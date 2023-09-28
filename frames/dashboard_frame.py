from .base_frame import BaseFrame

from . import constants as csts


class DashboardFrame(BaseFrame):
    def __init__(self,title="Super Sexy Dashboard"):
        super().__init__(title=title,iconpath=csts.DASHICO_PATH,
                         scr_h_pcnt=csts.DASH_H_PCNT,scr_w_pcnt=csts.DASH_W_PCNT)
        # self.root.mainloop()