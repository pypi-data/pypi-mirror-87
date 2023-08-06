使用 python3  + click  编写的个人常用的工具  
* 服务器管理 
```shell script
m server 
```
* 本地常用工具 
```shell script
m local 
```
* 常用脚本管理
```shell script
m script 
```
* 本身配置管理 
```shell script
m config 
```

#### 安装更新工具  
```shell script
# ubuntu 使用python3 版本的pip 名字默认为pip3 
#安装
pip3 install jiuming-tools
#更新
pip3 install --upgrade jiuming-tools 
# 使用
m
#启用自动补全:
#bash:在.bashrc末尾添加 eval "$(_M_COMPLETE=source m)"
#zsh:在.zshrc末尾添加 eval "$(_M_COMPLETE=source_zsh m)"
```

