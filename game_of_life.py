import argparse

from draw import draw

def main():
    parser = argparse.ArgumentParser(
        description="Conway's Game of Life on a torus",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=35, width=100)
    )
    
    parser.add_argument(
        "-f", "--file",
        type = str,
        default = "",
        help="initial state"
    )

    parser.add_argument(
        "-W", "--width",
        type = int,
        default = 100,
        help="width of the grid"
    )

    parser.add_argument(
        "-H", "--height",
        type = int,
        default = 40,
        help="height of the grid"
    )
    
    parser.add_argument(
        "-c", "--cell-size",
        type = int,
        default = 20,
        help="cell size"
    )

    args = parser.parse_args()
    
    draw(args.file, args.width, args.height, args.cell_size)

if __name__ == "__main__":
    main()
