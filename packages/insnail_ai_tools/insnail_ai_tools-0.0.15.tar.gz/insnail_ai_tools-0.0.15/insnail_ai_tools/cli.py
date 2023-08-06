import os
import fire


def test():
    print("test cli")


def init_pre_commit(
    config_url: str = "https://it-snail-dev.oss-cn-shenzhen.aliyuncs.com/jumpserver/.pre-commit-config.yaml",
    filename: str = ".pre-commit-config.yaml",
):
    """
    用来初始化pre_commit
    :param config_url: config远程url
    :param filename: 指定到文件
    :return:
    """
    os.system("pip install pre-commit")
    os.system(f"curl {config_url} > {filename}")


def init_python_project(
    project_name: str,
    remote_url: str = "https://git.woniubaoxian.com/ai/python_tem_project.git",
    use_celery: bool = True,
):
    """
    用来初始化一个python项目，初始化之后项目内有一些字段需要更改一下
    :param project_name: 项目名称
    :param remote_url: temp project 地址
    :param use_celery: 是否使用celery
    :return:
    """
    print("clone project:")
    os.system(f"git clone {remote_url} {project_name}")
    print("delete git folder:")
    os.system(f"rm -rf ./{project_name}/.git")
    if not use_celery:
        os.system(f"rm -rf ./{project_name}/celery_server")


def upload(*files, prefix=""):
    """
    上传文件至oss上，默认路径为 jumpserver。
    :param files: 文件列表， 如果文件名为 aaa/bbb.txt， 会被重命名为 bbb.txt
    :param prefix: 为所有文件增加prefix, 如 prefix="aaa/"，则所有文件会被放到 jumpserver/aaa/文件夹下
    :return:
    """
    from insnail_ai_tools import ossutils

    ossutils.upload(*files, prefix=prefix)


def main():
    fire.Fire()


if __name__ == "__main__":
    fire.Fire()
