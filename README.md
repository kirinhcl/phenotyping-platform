# phenotyping-platform
    本项目暂时为三个模块
    针脚图为1.png
![针脚图](https://github.com/kirinhcl/phenotyping-platform/blob/main/1.png)
## 1.自动拍照模块



## 2.自动灌溉模块
### （1）基于土壤湿度传感器浇水（程序为soil.py）
    A.材料：树莓派、土壤湿度传感器、继电器、水泵
    B.引脚及连接：采用BOARD编码
                a.土壤湿度检测模块
                  Ⅰ Vcc引脚连接5v（pin2)
                  Ⅱ GND引脚连接GND（pin6）
                  Ⅲ DO引脚连接IN（pin11）
                b.继电器模块
                  与树莓派相连端：
                  Ⅰ vcc——5V（pin4）
                  Ⅱ gnd——gnd（pin34）
                  Ⅲ IN——GPIO（pin12）
                  与水泵相连端（选择NO,COM常开路连接）：
                  Ⅰ 剪开水泵其中一根电源线，两端分别连接NO和COM
### （2）基于称重传感器浇水(基于https://github.com/tatobari/hx711py 修改)（程序为hx711py文件夹中的weight.py）
[参考教程](https://zhuanlan.zhihu.com/p/132478015)
    
    A.材料：树莓派、压力传感器、HX711模块、跳线
    B.引脚及连接：采用BCM编码
                a.HX711
                  黑色：E- 绿色：A- 白色：A + 红色：E +
                b.HX711接树莓派
                  VCC至Raspberry Pi Pin 2（5V)
                  GND至Raspberry Pi引脚6（GND）
                  DT至Raspberry Pi Pin 29（GPIO 5）
                  SCK至Raspberry Pi引脚31（GPIO 6）
                c.继电器模块同上
    C.运行weight.py
    D.若需要校准见参考教程
        
          
## 3.步进机模块
    暂无
