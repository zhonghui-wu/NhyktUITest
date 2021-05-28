import os
from BeautifulReport import BeautifulReport
from BeautifulReport.BeautifulReport import HTML_IMG_TEMPLATE

def force_attach_image(img_nm):
    """
    这是一个让用例运行正常测试报告中也能附上截图的函数
    :param img_nm:
    :return:
    """
    img_path = os.path.abspath('{}'.format(BeautifulReport.img_path))
    data = BeautifulReport.img2base(img_path, img_nm + '.png')
    print(HTML_IMG_TEMPLATE.format(data, data))