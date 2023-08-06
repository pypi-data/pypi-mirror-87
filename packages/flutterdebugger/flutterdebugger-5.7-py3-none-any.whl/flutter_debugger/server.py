from twisted.web import server, resource
from twisted.internet import reactor, endpoints
import json
from flutter_debugger.packager import *
import hashlib

def patch_increment_support_files():
    flutter_path = run_command_and_return("which flutter")
    buildDartFilePath = os.path.join(os.path.dirname(flutter_path), "../packages/flutter_tools/lib/src/bundle.dart")
    buildDartFilePatchPath = os.path.join(sys.prefix, "bins/bundle.dart.patch")
    if not os.path.exists(buildDartFilePatchPath):
        return
    md5Origin = md5_of_file(buildDartFilePath)
    md5Patch = md5_of_file(buildDartFilePatchPath)
    if md5Origin != md5Patch:
        logger.info("替换bundle.dart")
        shutil.move(buildDartFilePath, buildDartFilePath + ".bak")
        shutil.copy(buildDartFilePatchPath, buildDartFilePath)
        cache_tool_path = "{0}/cache/flutter_tools.snapshot".format(os.path.dirname(flutter_path))
        logger.info("移除编译工具缓存: {0}".format(cache_tool_path))
        os.system("rm {0}".format(cache_tool_path))
    else:
        logger.info("bundle.dart已经是最新，无需patch")

class FlutterDebuggerServer(resource.Resource):
    isLeaf = True
    numberRequests = 0
    port = 8006
    _is_running = False
    proj_id: str

    def __init__(self, port=8006):
        self.port = port
        self.mac_name = run_command_and_return("id -un") + "'s MacBook"
        m = hashlib.md5()
        m.update(os.path.abspath("./").encode("utf8"))
        self.proj_id = m.hexdigest()
        clean_packages(self.proj_id)
        patch_increment_support_files()

    def render_GET(self, request):
        old_pkg_path = None
        old_pkg_md5 = None
        if b'old_pkg_md5' in request.args:
            old_pkg_md5 = request.args[b'old_pkg_md5']
            old_pkg_md5 = old_pkg_md5[0].decode("utf-8")
            old_pkg_path = get_cache_package(self.proj_id, old_pkg_md5)
        request.setHeader(b"content-type", b"application/json")
        request.setHeader(b"host-name", bytes(self.mac_name, "utf8"))
        if str(request.path, 'utf8') == '/package':
            # flutter进行打包
            result, file_name, zip_file_path, pkg_md5 = package_flutter_assets(self.proj_id, self.port)

            if (not Config.disablePackagePatch) and old_pkg_path:
                if pkg_md5 == old_pkg_md5:
                    request.setHeader(b"content-type", b"application/oct-stream")
                    request.setHeader(b"type", b"none")
                    return ''.encode("utf-8")
                patch_file = diff_patch(self.proj_id, old_pkg_path, zip_file_path)
                with open(patch_file, 'rb') as file:
                    all_bytes = file.read()
                    request.setHeader(b"content-type", b"application/zip")
                    request.setHeader(b"type", b"patch")
                    request.setHeader(b"md5", pkg_md5.encode('utf-8'))
                    logger.info("Patch file size: {0}".format(len(all_bytes)))
                    return all_bytes
            else:
                with open(zip_file_path, 'rb') as file:
                    all_bytes = file.read()
                    request.setHeader(b"content-type", b"application/zip")
                    request.setHeader(b"type", b"all")
                    request.setHeader(b"md5", pkg_md5.encode('utf-8'))
                    return all_bytes
        elif str(request.path, 'utf8') == '/old':
            if b'md5' in request.args:
                old_pkg_md5 = request.args[b'md5']
                pkg_path = get_cache_package(self.proj_id, old_pkg_md5[0].decode("utf-8"))
                if pkg_path:
                    return json.dumps({
                        "ret": 0,
                        "data": pkg_path,
                        "message": "调用成功"
                    }).encode("ascii")

        return json.dumps({
            "ret": 0,
            "message": "调用成功"
        }).encode("ascii")

    def run(self):
        endpoints.serverFromString(reactor, "tcp:" + str(self.port)).listen(server.Site(self))
        reactor.run()


if __name__ == '__main__':
    flt_server = FlutterDebuggerServer()
    flt_server.run()
