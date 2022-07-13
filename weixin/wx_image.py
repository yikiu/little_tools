import pathlib
import imghdr


base = 0xFF
next1 = 0xD8
gifA = 0x47
gifB = 0x49
pngA = 0x89
pngB = 0x50


def convert(src_dir: pathlib.Path, dest_dir: pathlib.Path):
    """
    微信电脑端存储的图像为经过加密的dat文件，不能被图像软件识别。本函数将指定目录下的dat文件进行转换为正常的图像。
    :param src_dir:微信图像保存目录：xxx/WeChat Files/xxx/FileStorage/Image.
    :param dest_dir:保存到的目的目录
    """
    for p in src_dir.iterdir():

        if p.is_dir():
            d = dest_dir.joinpath(p.name)
            convert(p, d)
        elif p.is_file() and p.suffix == '.dat':
            if not dest_dir.exists():
                dest_dir.mkdir(parents=True)
            d = dest_dir.joinpath(p.stem)
            print(p)
            convert_file(p, d)


def convert_file(src: pathlib.Path, dest: pathlib.Path):
    """
    参考 https://www.zhihu.com/question/393121310/answer/2103786875
    :param src:dat文件
    :param dest:保存的目的路径
    """
    with open(src, 'rb') as fr:
        content = fr.read()
        firstV = content[0]
        nextV = content[1]
        jT = firstV ^ base
        jB = nextV ^ next1
        gT = firstV ^ gifA
        gB = nextV ^ gifB
        pT = firstV ^ pngA
        pB = nextV ^ pngB

        v = firstV ^ base
        if jT == jB:
            v = jT
        elif gT == gB:
            v = gT
        elif pT == pB:
            v = pT

        with open(dest, 'wb') as fw:
            fw.write(bytearray(map(lambda a: v ^ a, content)))
        suffix=imghdr.what(dest)
        if not suffix:
            suffix='.jpg'
        else:
            suffix='.'+suffix
        dest.rename(dest.with_suffix(suffix))
