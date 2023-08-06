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


def upload(*files):
    """
    用来上传文件到阿里云。
    上传后下载链接为 https://it-snail-dev.oss-cn-shenzhen.aliyuncs.com/jumpserver/{filename}
    :param files: 文件列表
    :return:
    """
    from insnail_ai_tools import ossutils

    ossutils.upload(*files)


def main():
    fire.Fire()


if __name__ == "__main__":
    fire.Fire()
