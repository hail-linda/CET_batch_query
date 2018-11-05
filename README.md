# CET_batch_query
A University English Grading Test (CET) batch query script



## 说明
一个用于批量查询CET成绩的脚本

Author = Linda


## 许可证

使用 [Apache License 2.0](LICENSE) 授权。

## 性能
目前预计查询10k条信息大约需要2h

所以需要大批量查询的同学可以联系我：i@lixinda.me 以在我的服务器上24小时运行


## 使用方式

 1 准备 rsc.xls 表格文件 ， 其中必须包括的列有：*准考证号、姓名、语言级别、学号* （顺序可以不吻合）
 
 2 运行 main.py


## 输出

 1 rsc_1.csv 内容包括：*准考证号、姓名、语言级别、学号、总成绩、听力、阅读、写作与翻译*
 
 2 若干 .png  图片文件 文件名为学生学号


## 使用到的python库

pandas、selenium、unittest、time、re、os、tensorflow等
 


## 预计的优化方向

 - docs
 - 输出文件更改为xls/xlsx
 - ~~输出图片至子文件夹下~~  (ver2.0解决)
 - ~~开发windows下即开即用版本~~ （经测试由于需要tensorflow，打包后文件超过1G）
 - 开发线上运行版本
 - ~~开发验证码系统~~  （ver2.0解决，正确率约60%）
 
## 大概的过程
 
 - 读取.xls/.xlsx文件，转码至 .csv
 - 顺序读入  selenium + firefox 模拟输入姓名与准考证号
 - 模拟点击验证码输入框，待图片显示 wget 下载图片
 - 将图片去渐变灰色背景，去红黑网格
 - tensorflow 识别验证码
 - 填入识别后结果，若正确记录各项信息，执行下一条
 - 过程中对成绩查询后结果截图至 screenshot/ 
