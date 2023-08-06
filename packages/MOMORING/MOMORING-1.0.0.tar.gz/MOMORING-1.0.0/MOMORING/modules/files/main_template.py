def get_main_template():
    txt = """\
import argparse


def run(mode):
    if mode == 'your_mode':
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument(
        '-m', '--mode', help='Running Mode',
        choices=['your_mode']
    )
    opt = parser.parse_args()
    run(opt.mode)
    
    print('Job done. Good luck.')

"""
    return txt
