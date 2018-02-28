# CET_batch_query
A University English Grading Test (CET) batch query script



## 说明
一个用于批量查询CET成绩的脚本
Author = Linda


## 许可证

使用 [Apache License 2.0](LICENSE) 授权。


## 使用方式

 1 准备 rsc.xls 表格文件 ， 其中必须包括的列有：*准考证号、姓名、语言级别、学号* （顺序可以不吻合）
 2 运行 main.py


## 输出

 1 rsc_1.csv 内容包括：*准考证号、姓名、语言级别、学号、总成绩、听力、阅读、写作与翻译*
 2 若干 .png  图片文件 文件名为学生学号


## 使用到的python库

pandas、selenium、unittest、time、re
 


## 预计的优化方向

 - docs
 - 输出文件更改为xls/xlsx
 - 输出图片至子文件夹下
 - 开发windows下即开即用版本
 - 开发线上运行版本
