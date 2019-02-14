## QQzone_crawler
QQ 空间动态爬虫，利用cookie登录获取所有可访问好友空间的动态并保存到本地

需要先安装第三方库 **requests** <br />
本程序使用的是**python3.5**，在**Linux**下完成。由于自己的电脑上同时有python2.7和python3.5，默认是python2。所以在每个程序头部我写的都是

```
#!/usr/bin/env python3
```

由于程序使用`from urllib import parse`，利用parse模块来构造URL，所以如果使用python2的朋友需要在对应的地方修改，此外print语句也是要相应修改的。

# 各程序文件说明

**main.py**： 程序主入口，运行时执行`python3 main.py`即可

**get_my_friends.py**： 用于从QQ空间服务器获取包括自己的QQ好友信息的文件，其中包括他们的QQ号和名称（此处是备注名），保存到本地，每个文件中保存有50个。每完成一个文件请求后，会暂停5秒。在程序运行时，会自动将这些文件保存在friends文件夹中。

**get_qq_number.py**： 用于从上一步保存好的文件中提取出所有好友的QQ号和名称，QQ号和名称以字典形式保存，再以它们组成的字典为作元素构造列表，再保存到本地，文件名为qqnumber.inc

**get_moods.py**： 用于从QQ空间服务器获取包含每个好友空间发表的说说的文件，其中包含每个说说的发表时间、内容、地点信息、手机信息等，保存到本地，每个文件中保存20条信息。每完成一个文件请求后，会暂停5秒。在程序运行时，会自动将这些文件保存在mood_result文件夹中。

**cookie_file**： 用于放置自己登录QQ空间后得到的cookie。从浏览器中复制出来放在这个文件内即可，在负责处理cookie的函数中有对应的处理代码来处理换行符，但还是希望不要出现多行，末尾也不要有多余的空行。**但要注意的是，这个文件里面只能放一个cookie。它的作用是方便设置cookie，而不是用于反反爬虫。** 如果不知道怎么获取cookie，请看[这里](http://www.xjr7670.com/articles/how-to-get-qzone-cookie.html)

---

# 可视化部分

**operate_table.py**：这个程序创建用于保存说说信息的数据库。里面写了创建数据表和删除数据表的两个函数。需要单独执行。
创建数据表：

```
python3 operate_table.py create_table
```

删除数据表：

```
python3 operate_table.py drop_table
```

**get_moods_detail.py**：程序在执行完 get_moods.py 中的功能之后，会把包含有每个好友的说说文件保存到本地。而这个程序就是用于把说说信息从这些文件里面提取出来，放到sqlite数据库里面去的。这个程序需要单独执行。执行完后在当前目录下会生成 moods.sqlite 数据库文件。**本程序需要在成功执行 operate_table.py 程序创建数据表后执行**。

**get_single_report**：这个是个 Web 程序，用于在浏览器中查看指定好友说说的简单报告。也需要单独执行，并且必须要在执行完 get_moods_details.py 文件以生成 moods.sqlite 数据库文件，这个 web 程序才可以正确执行。直接执行本文件夹中的index.py即可。需要先安装 flask、pandas、sqlalchemy、jieba、wordcloud 这几个库。**执行 `python3 index.py` 后**，在浏览器中输入 http://localhost:5000/qqnum=QQ号码 就可以查看到结果了

**get_word.py**：用来生成词云，背景图为 mask.jpg，为QQ空间的五角星。ttf文件路径请根据自己系统修改。**本程序不需要单独执行。**

## 注意事项

1. **获取QQ好友信息是间接获取的。需要先在QQ空间中将自己空间的访问权限先设置为仅QQ好友可访问。然后程序才能够正常运行**

2. 最终获取到的各好友的空间动态会以文件形式保存在以其QQ号为名的文件夹当中（它们又位于mood\_result文件夹中）。它们是由QQ空间服务器返回的文件，还需要自行进行处理才能得到自己想要的信息。其实内容的格式已经很接近JSON了
2.1 更新后的版本，可以通过依次执行operate_table.py、get_moods_detail.py两个程序来把动态保存在sqlite数据库文件中

3. 在get_moods_detail.py程序中，我只提取了当时所需要的部分信息，而不是与说说相关的所有信息。有需要其它信息的还要自己去operate_table.py中修改创建数据表的函数以及在get_moods_detail.py程序中修改提取说说信息的函数

4. 程序开始运行后，会产生一个日志文件crawler_log.log，它记录了程序运行期间的一些必要的信息，比如什么时候抓取到了哪个号码的空间，这个空间能不能被访问等

5. 在创建了数据库表后，如果有需要重新执行提取动态插入数据库表的操作的话，建议先删除原表，再执行提取
