# -*- coding:utf-8 -*-

import click

from src.config import global_config, config_manager
from src.config.global_config import compile_ip, compile_host_mame
from src.local import http_server, pc_info, net_manager, pc_test
from src.script import script_manager
from src.server import server_config


def validate_ip_or_host_name_type(ctx, param, value):
    err_msg = '{}不符合ip/域名格式!请检查后输入'.format(value)
    try:
        if compile_ip.match(value):
            return value
        elif compile_host_mame.match(value):
            return value
        else:
            raise click.BadParameter(err_msg)
    except ValueError:
        raise click.BadParameter(err_msg)


def print_version(ctx, param, value):
    """
    输出工具版本
    :param ctx:   click上下文
    :param param: 参数
    :param value:  值
    :return:
    """
    if not value or ctx.resilient_parsing:
        return

    version_info = """
    作者:ming 
    仅适用linux 其他平台兼容性不做保证
    启用自动补全:
    bash:在.bashrc末尾添加 eval "$(_M_COMPLETE=source m)"
    zsh:在.zshrc末尾添加 eval "$(_M_COMPLETE=source_zsh m)"
    依赖的工具：ssh、sftp、vi、dd、git、free、ip、cat、graphviz
    jiuming-tools Version {}""".format(global_config.version)
    click.echo(version_info)
    ctx.exit()


@click.group()
@click.option('--version', '-v', help='工具版本', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def cli():
    pass


# ---------------------- server tools ----------------------------------------------------------------------------------
@cli.group(help='远程服务器管理')
def server():
    pass


@server.command("list", help='显示所有服务器配置')
def server_list():
    server_config.server_list()


@server.command("add", help='添加服务器配置')
@click.option('--name', '-n', prompt='请输入服务器名称')
@click.option('--host', '-h', prompt='请输入服务器地址', callback=validate_ip_or_host_name_type)
@click.option('--port', '-p', prompt='请输入服务器ssh端口,默认为22', default=22)
@click.option('--username', '-u', prompt='请输入服务器用户名')
@click.option('--password', '-pwd', prompt='请输入密码')
@click.option('--path', '-path', prompt='密钥位置')
def server_add(name, host, port, username, password, path):
    server_config.server_add(str(name).strip(), host, port, username, password, path)


@server.command("remove", help='根据名称删除服务器配置')
@click.option('--name', '-n', type=str, prompt='请输入服务器名称', help='服务器名称')
def server_remove(name):
    server_config.server_remove(name)


@server.command('edit', help='使用vi编辑服务器配置')
def server_edit():
    server_config.server_edit()


@server.command('connect', help='连接服务器')
@click.option('--name', '-n', type=str, prompt='请输入服务器名称', help='服务器名称')
def server_connect(name):
    server_config.server_connect(name)


@server.command('sftp', help='打开sftp客户端')
@click.option('--name', '-n', type=str, prompt='请输入服务器名称', help='服务器名称')
@click.option('--cwd', '-cwd', type=click.Path(exists=True), default='.', help='本地工作目录,默认为.')
def server_sftp(name, cwd):
    server_config.server_sftp(name, cwd)


# ----------------------------------- local tools ----------------------------------------------------------------------

@cli.group(help='本机使用的工具')
def local():
    pass


@local.command('pc', help='电脑配置')
def local_pc_info():
    pc_info.echo_pc_info()


@local.command('http', help='根据指定文件夹开启临时http服务器')
@click.option('--dir', '-d', type=click.Path(exists=True), default='.', nargs=1, help='指定静态文件目录,默认为.')
@click.option('--port', '-p', default=20000, type=int, nargs=1, help='指定服务端口,默认为20000')
@click.option('--host', '-h', default='0.0.0.0', callback=validate_ip_or_host_name_type, type=str, nargs=1,
              help='指定服务监听地址,默认为0.0.0.0')
def local_tmp_http(dir, port, host):
    http_server.http_server(dir, port, host)


@local.command('traceroute', help='路由跟踪,需要root权限')
@click.option('--dir', '-d', type=click.Path(exists=True), default='.', nargs=1, help='生成svg文件目录,默认为.')
@click.option('--port', '-p', default=80, type=int, nargs=1, help='端口,默认为80')
@click.option('--host', '-h', default='0.0.0.0', callback=validate_ip_or_host_name_type, type=str, nargs=1,
              help='跟踪地址,默认为0.0.0.0')
def local_traceroute(dir, port, host):
    net_manager.trace_route(dir, port, host)


@local.command('socket-test', help='测试服务器是否可以打开socket')
@click.option('--host', '-h', type=str, prompt='请输入服务器地址', callback=validate_ip_or_host_name_type, help='服务器地址')
@click.option('--port', '-p', type=int, default=80, help='探测端口号(默认为80)')
def socket_test(host, port):
    net_manager.net_test(host, port)


@local.command('test-disk', help='测试服务器磁盘性能')
@click.option('--size', '-s', type=int, default=2, help='测试磁盘数据大小，单位GB，默认2GB')
def test_disk(size):
    pc_test.testDisk(size)


@local.command('test-net', help='测试服务器网络速度')
@click.option('--threads', '-t', type=int, default=None, help='线程数,默认为speettest的默认参数')
def test_network(threads):
    pc_test.testNetwork(threads)


# ----------------------------------- tools config manager  -----------------------------------------------------------

config_remark = """
配置管理 \n
使用私有git仓库作为配置保存\n  
如github 私有仓库等 \n
"""


@cli.group(help=config_remark)
def config():
    pass


@config.command('details', help='查看当前配置仓库配置')
def config_details():
    config_manager.details()


@config.command('save', help='创建当前配置仓库配置')
@click.option('--url', '-url', type=str, prompt='同步仓库url地址')
@click.option('--username', '-u', type=str, prompt='同步仓库用户名')
@click.option('--password', '-p', type=str, prompt='同步仓库密码')
def config_save(url, username, password):
    config_manager.save(url=url, username=username, password=password)


@config.command('remove', help='删除当前配置仓库配置')
def config_remove():
    config_manager.remove()


@config.command('pull', help='同步配置远程到本地')
def config_pull():
    config_manager.pull()


@config.command('push', help='同步配置本地到远程仓库')
@click.option('--remark', '-r', type=str, help='推送备注')
def config_push(remark):
    config_manager.push(remark)


@config.command('clone', help='clone配置到本地')
def config_clone():
    config_manager.clone()


# ----------------------------------- tools config manager  -----------------------------------------------------------
# linux 各种脚本管理   shell 、py 等脚本


@cli.group(help='管理常用linux的脚本')
def script():
    pass


@script.command('remove', help='删除脚本')
@click.option('--name', '-n', prompt='脚本名称')
def script_remove(name):
    script_manager.script_remove(name)


@script.command('create', help='创建脚本')
@click.option('--type', '-t', prompt='脚本类型(执行引擎名称)')
@click.option('--name', '-n', prompt='脚本名称')
@click.option('--remark', '-r', prompt='备注描述')
def script_create(type, name, remark):
    script_manager.script_create(type, name, remark)


@script.command('details', help='查看脚本详情')
@click.option('--name', '-n', prompt='脚本名称')
def script_details(name):
    script_manager.script_details(name)


@script.command('list', help='列出当前脚本')
def script_list():
    script_manager.script_list()


@script.command('exec', help='执行脚本')
@click.option('--name', '-n', prompt='脚本名称')
def script_exec(name):
    script_manager.script_exec(name)


# main 函数
if __name__ == '__main__':
    cli()
