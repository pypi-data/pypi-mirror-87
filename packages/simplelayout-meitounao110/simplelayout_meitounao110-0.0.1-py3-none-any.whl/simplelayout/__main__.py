# TODO 正确导入函数 generate_matrix, save_matrix, save_fig
from simplelayout.cli import get_options  # TODO: 保证不修改本行也可以正确导入
from simplelayout.generator import utils
from simplelayout.generator import core


def main():
    options = get_options()
    print(options)
    utils.make_dir(options.outdir)
    matrix = core.generate_matrix(options.board_grid, options.unit_grid,
                                  options.unit_n, options.positions)
    utils.save_matrix(matrix, options.outdir+'/'+options.file_name)
    utils.save_fig(matrix, options.outdir+'/'+options.file_name)


if __name__ == "__main__":
    main()
