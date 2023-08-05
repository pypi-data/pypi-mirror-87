import argparse
import os


def get_options():
    parser = argparse.ArgumentParser(description="Demo of simplelayout")
    parser.add_argument('--board_grid',
                        help=' Layout panel resolution ', type=int)
    parser.add_argument('--unit_grid',
                        help=' Rectangular component resolution ', type=int)
    parser.add_argument('--unit_n', help=' Numbers of component ', type=int)
    parser.add_argument('--positions',
                        help=' position serial number of component ',
                        nargs='+', type=int)
    parser.add_argument('-o', '--outdir',
                        help=' directory of output ',
                        default='./example_dir', type=str)
    parser.add_argument('--file_name', help=' file name of output ',
                        default='example', type=str)
    # TODO: 按 1-simplelayout-CLI 要求添加相应参数

    options = parser.parse_args()
    # 检验是否被整除
    if options.board_grid % options.unit_grid != 0:
        print("error on unit_grid")
        exit()
    uplimit = (options.board_grid / options.unit_grid) ** 2
    # 检验长度是否标准
    if len(options.positions) != options.unit_n:
        print('position number error')
        exit()
    else:
        for i in range(len(options.positions)):
            if 1 > options.positions[i] or options.positions[i] > uplimit:
                exit()
    path = transpath(options.outdir)
    if not os.path.exists(path):
        os.makedirs(path)
    return options


def transpath(path):
    path = path.replace('/', os.sep)
    path = path.replace('\\', os.sep)
    return path
