**环境说明**

python 3以上

tesseract环境，用于截图识别

BeautifulReport生成测试报告库

unittest + selenium 框架

traceback打印报错信息库

os库

stat库

**运行说明**

安装tesseract-ocr并配置环境变量

1.安装tesseract4.0

双击软件安装，默认下一步，有几处需要注意：
数据包和语言包，需要勾选，安装位置自己选择，或者默认。安装完成后就可以设置环境变量了。

2.设置系统环境变量Path

桌面上此电脑->右键属性->点击高级系统设置->在打开的系统属性界面->高级下面点击环境变量->在环境变量界面选择系统变量中选中path，然后点下面的编辑，打开编辑环境变量界面新建一个C:\Program Files (x86)\Tesseract-OCR（这里填Tesseract-OCR的安装路径）的值，然后确定

3.新建系统变量TESSDATA_PREFIX

系统变量下面新建一个TESSDATA_PREFIX变量名，路径就是tessdata文件夹的路径地址，复制过来即可

4.查看软件版本及语言库

运行CMD命令

输入：tesseract -v，可以看到版本信息。

输入：tesseract --list-langs来查看本地Tesseract-OCR支持语言库

5.在cmd执行下面命令

pip install pillow  #一个python的图像处理库，pytesseract依赖

pip install pytesseract

6.安装BeautifulReport库

在cmd输入pip install BeautifulReport

7.运行脚本

在cmd中cd进入到该目录下面，再输入python beautifulReport.py 即可
