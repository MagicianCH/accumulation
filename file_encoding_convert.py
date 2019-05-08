"""
文件转码工具

原创：https://github.com/smslit/tools-with-script/blob/master/encoding/encoding

对输入输出稍作了修改
"""

import os
import argparse
from chardet.universaldetector import UniversalDetector


def getargs():
    parser = argparse.ArgumentParser(description='这是一个检测或转换文件编码的工具')
    parser.add_argument('-i', '--indir', help='指定一个文件的路径')
    parser.add_argument(
        '-e',
        '--encoding',
        nargs='?',
        const='UTF-8',
        help='''指定目标编码，可选择的编码：
ASCII, (Default) UTF-8 (with or without a BOM), UTF-16 (with a BOM),
UTF-32 (with a BOM), Big5, GB2312/GB18030, EUC-TW, HZ-GB-2312,
ISO-2022-CN, EUC-JP, SHIFT_JIS, ISO-2022-JP, ISO-2022-KR, KOI8-R,
MacCyrillic, IBM855, IBM866, ISO-8859-5, windows-1251, ISO-8859-2,
windows-1250, EUC-KR, ISO-8859-5, windows-1251, ISO-8859-1, windows-1252,
ISO-8859-7, windows-1253, ISO-8859-8, windows-1255, TIS-620''')
    parser.add_argument('-o', '--outdir', help='指定转换文件的输出目录')
    return parser.parse_args()


def detcect_encoding(filepath):
    """检测文件编码
    Args:
        detector: UniversalDetector 对象
        filepath: 文件路径
    Return:
        fileencoding: 文件编码
        confidence: 检测结果的置信度，百分比
    """
    detector = UniversalDetector()
    detector.reset()
    for each in open(filepath, 'rb'):
        detector.feed(each)
        if detector.done:
            break
    detector.close()
    fileencoding = detector.result['encoding']
    confidence = detector.result['confidence']
    if fileencoding is None:
        fileencoding = 'unknown'
        confidence = 0.99
    return fileencoding, confidence * 100


if __name__ == '__main__':
    args = getargs()
    if args.outdir:
        if not os.path.exists(args.outdir):
            answer = input(
                f'[-] 无效的导出路径: {args.outdir} [-]\n要用转码后的文件直接替换源文件吗? y or n\n')
            if 'y' in answer:
                args.outdir = None
            else:
                exit(1)
    if args.indir:
        if not os.path.exists(args.indir):
            print(f'[-] 无效的导入路径')
            exit(1)
    files = os.listdir(args.indir)
    for fn in files:
        file = os.path.join(args.indir, fn)
        if not os.path.isfile(file):
            print(f'[-] 无效的文件路径: {file} [-]')
            continue
        encoding, confidence = detcect_encoding(file)
        print(f'[+] {file}: 编码 -> {encoding} (置信度 {confidence}%) [+]')
        if args.encoding and (encoding is not 'unknown') and (confidence > 0.75):
            f = open(file, 'r', encoding=encoding, errors='replace')
            text = f.read()
            f.close()
            outpath = os.path.join(args.outdir, fn) if args.outdir else file
            f = open(outpath, 'w', encoding=args.encoding, errors='replace')
            f.write(text)
            f.close()
            print('[+] 转码成功: %s(%s) -> %s(%s) [+] ' % (file, encoding, outpath, args.encoding))