from flutter_debugger import *
import os
import time
import tempfile
import hashlib
import site
import sys

from flutter_debugger.config import Config

logger = create_logger()

XDeltaExe = '/usr/local/bin/XdeltaCLI'
exe_path = os.path.join(sys.prefix, "bins/XdeltaCLI")
if os.path.exists(exe_path):
    XDeltaExe = exe_path
# logger.info("在 {0} 找到XdeltaCLI".format(XDeltaExe))

def get_package_root_dir(proj_name: str):
    archive_folder = proj_name + '_debug_archives'
    flutter_assets_archive_dir = os.path.abspath(tempfile.gettempdir() + "/" + archive_folder)
    return flutter_assets_archive_dir


def clean_packages(proj_name: str):
    pkg_root = get_package_root_dir(proj_name)
    if os.path.exists(pkg_root):
        logger.info("清除之前的包...")
        shutil.rmtree(pkg_root)
        logger.info("清除完毕")
    os.mkdir(pkg_root)


def get_cache_package(proj_name, md5):
    old_pkg_path = os.path.join(get_package_root_dir(proj_name), md5 + ".zip")
    logger.info("检查旧包：{0}".format(old_pkg_path))
    if os.path.exists(old_pkg_path):
        logger.info("旧包存在：{0}".format(old_pkg_path))
        return old_pkg_path
    logger.info("旧包不存在：{0}".format(old_pkg_path))
    return None


def diff_patch(proj_name, old_pkg_path, new_pkg_path):
    begin_time = time.time()
    logger.info("找到旧包，开始差分计算")
    patch_path = os.path.join(get_package_root_dir(proj_name), "{0}-{1}.patch".format(os.path.basename(old_pkg_path), os.path.basename(new_pkg_path)))
    os.system("{0} {1} {2} {3}".format(XDeltaExe, old_pkg_path, new_pkg_path, patch_path))
    logger.info("找到旧包，差分结果：{0}".format(patch_path))
    end_time = time.time()
    cost_time = end_time - begin_time
    logger.info("差分耗时: {0}s".format(cost_time))
    return patch_path


def package_flutter_assets(proj_name: str, port: int) -> (bool, str):
    begin_time = time.time()
    zip_md5 = ''

    pkg_root_dir = get_package_root_dir(proj_name)

    # 运行flutter的打包代码
    if not check_shcommand_exist("flutter"):
        logger.error("Flutter命令不存在，无法打包")
        return False, "Flutter命令不存在，无法打包", ""
    else:
        logger.info("准备打包Flutter项目")

    if Config.disableIncrementalCompile:
        logger.info("use release mode")
        run_command("flutter build bundle --release")
    else:
        logger.info("use release mode inc")
        run_command("flutter build bundle --release --extra-front-end-options=\"--incremental\"")

    # 将flutter的打包产物压缩成zip包
    archive_file_name = proj_name + '_debug'
    flutter_assets_dirs = [os.path.abspath('./build/flutter_assets'),
                           os.path.abspath('./ios/Flutter/App.framework/flutter_assets'),
                           os.path.abspath('./.ios/Flutter/App.framework/flutter_assets')]
    flutter_assets_archive_path = os.path.join(pkg_root_dir, archive_file_name + '.zip')
    if os.path.exists(flutter_assets_archive_path):
        os.system("rm -rf {0}".format(flutter_assets_archive_path))
    have_avaliable_flutter_dir = False
    for flutter_assets_dir in flutter_assets_dirs:
        if os.path.exists(flutter_assets_dir):
            have_avaliable_flutter_dir = True
            logger.info("开始归档flutter_assets目录")
            logger.info("flutter_assets目录位置：{0}".format(flutter_assets_dir))
            archive_file_path = archive(flutter_assets_dir, flutter_assets_archive_path)
            # caculate file md5
            with open(archive_file_path, "rb") as f:
                zip_md5 = hashlib.md5(f.read()).hexdigest()
                flutter_assets_archive_path = os.path.join(pkg_root_dir, zip_md5 + '.zip')
                os.rename(archive_file_path, flutter_assets_archive_path)
            logger.info(str.format("归档flutter_assets目录结束，路径：{0}", flutter_assets_archive_path))
            break

    if not have_avaliable_flutter_dir:
        logger.error("打包Flutter项目失败，不存在可用的flutter_assets目录")
        return False, "打包Flutter项目失败，不存在可用的flutter_assets目录", ""

    end_time = time.time()
    cost_time = end_time - begin_time
    logger.info("打包耗时: {0}s".format(cost_time))

    return True, archive_file_name, flutter_assets_archive_path, zip_md5

