## Sublime操作

* 去除重复项
> (.*)(?=.*\n\1)  或  (^.*\n)(?=\1)
>> (.*) 任意字符 并捕获在第一组  (?=.*\n\1) 这是断言, 表示后面内容将是 任意个字符加上第一组所捕获的内容

* 删除空白行
> find what栏 : \s+$  （正则表达式）   replace with栏 : （这行留空） 
