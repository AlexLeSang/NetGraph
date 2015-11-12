import sys

from visualizator.vtkVisualizeGraph import VTKVisualizer

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) <= 1 or len(sys.argv) > 4:
        print "Args should be: filename [max_num_of_vertices] [edge_colors_filename]"

    else:
        if len(sys.argv) == 2:
            v = VTKVisualizer(sys.argv[1])
        elif len(sys.argv) == 3:
            v = VTKVisualizer(sys.argv[1], int(sys.argv[2]))
        else:
            v = VTKVisualizer(sys.argv[1], int(sys.argv[2]), sys.argv[3])

        v.vizualize_grapth()
