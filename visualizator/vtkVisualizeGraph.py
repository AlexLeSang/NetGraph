import os
import vtk

from vtk.vtkRenderingCorePython import vtkGraphToGlyphs

from visualizator.LGLReader import LGLReader

SCALINGS = "Scalings"

WEIGHTS = "Weights"

LABELS = "Labels"


class VTKVisualizer(object):
    def __init__(self, filename, max_num_of_vertices=-1):
        super(VTKVisualizer, self).__init__()
        self.filename = filename
        self.max_num_of_vertices = max_num_of_vertices
        self.g = vtk.vtkMutableDirectedGraph()

        self.labels = vtk.vtkStringArray()
        self.labels.SetNumberOfComponents(1)
        self.labels.SetName(LABELS)

        self.glyph_scales = vtk.vtkFloatArray()
        self.glyph_scales.SetNumberOfComponents(1)
        self.glyph_scales.SetName(SCALINGS)

        self.edge_weights = vtk.vtkDoubleArray()
        self.edge_weights.SetNumberOfComponents(1)
        self.edge_weights.SetName(WEIGHTS)

    def vizualize_grapth(self):
        self.insert_graph()
        self.g.GetEdgeData().AddArray(self.edge_weights)
        self.g.GetVertexData().AddArray(self.labels)
        self.g.GetVertexData().AddArray(self.glyph_scales)

        # num_of_tuples = self.glyph_scales.GetNumberOfTuples()
        # for i in range(num_of_tuples):
        #     scale = self.glyph_scales.GetTuple1(i)
        #     print(scale)
        #     # scale = 1.0 + 1.0/scale
        #     # self.glyph_scales.SetTuple1(i, scale)

        graphLayoutView = vtk.vtkGraphLayoutView()
        graphLayoutView.AddRepresentationFromInput(self.g)
        graphLayoutView.SetLayoutStrategy("Random")
        graphLayoutView.GetLayoutStrategy().SetEdgeWeightField(WEIGHTS)
        graphLayoutView.GetLayoutStrategy().SetWeightEdges(1)

        graphLayoutView.SetEdgeLabelArrayName(WEIGHTS)
        graphLayoutView.SetEdgeLabelVisibility(1)

        graphLayoutView.SetVertexLabelArrayName(LABELS)
        graphLayoutView.SetVertexLabelVisibility(1)

        graphLayoutView.ScaledGlyphsOn()
        graphLayoutView.SetScalingArrayName(SCALINGS)
        graphLayoutView.GetRepresentation().SetGlyphType(vtkGraphToGlyphs.SPHERE)

        graphLayoutView.GetRenderWindow().SetSize(1024, 768)
        graphLayoutView.ResetCamera()
        graphLayoutView.Render()
        graphLayoutView.GetLayoutStrategy().SetRandomSeed(0)
        graphLayoutView.GetInteractor().SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        graphLayoutView.GetInteractor().Start()

    def insert_graph(self):
        with open(self.filename, 'rb') as lgl_file:
            lgl = lgl_file.read()

        starting_vertex = None
        starting_vertex_index = -1
        num_of_references = 0
        for i, entry in enumerate(lgl.split(os.linesep)):
            if i > self.max_num_of_vertices:
                break

            self.glyph_scales.InsertNextValue(float(1.0))

            if LGLReader.is_starting_vertex(entry):
                primary_label = LGLReader.get_primary_vertex(entry)
                if not primary_label:
                    raise ValueError

                p_v = self.g.AddVertex()
                starting_vertex = p_v
                if starting_vertex_index != -1:
                    self.glyph_scales.SetTuple1(starting_vertex_index, 0.5 * num_of_references)

                starting_vertex_index = i
                num_of_references = 0
                self.labels.InsertNextValue(primary_label)

            else:
                secondary_label = LGLReader.get_vertex_label_and_weight(entry)
                if not secondary_label:
                    raise ValueError

                if isinstance(secondary_label, list):
                    self.labels.InsertNextValue(secondary_label[0])
                    self.edge_weights.InsertNextValue(secondary_label[1])

                else:
                    self.labels.InsertNextValue(secondary_label)
                    self.edge_weights.InsertNextValue(0.5)

                s_v = self.g.AddVertex()
                self.g.AddGraphEdge(starting_vertex, s_v)
                num_of_references += 1
