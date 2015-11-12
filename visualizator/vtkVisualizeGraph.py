import os
import vtk

from vtk.vtkRenderingCorePython import vtkGraphToGlyphs

from visualizator.LGLReader import LGLReader

VERTEX_ID = "VertexID"
SCALINGS = "Scalings"
WEIGHTS = "Weights"
LABELS = "Labels"


class VTKVisualizer(object):
    def __init__(self, filename, max_num_of_vertices=-1):
        super(VTKVisualizer, self).__init__()
        self.label_vertex_id_map = {}
        self.starting_vertex = None
        self.starting_vertex_index = -1
        self.num_of_references = 0
        self.filename = filename
        self.max_num_of_vertices = max_num_of_vertices
        self.g = vtk.vtkMutableDirectedGraph()

        self.vertex_ids = vtk.vtkIntArray()
        self.vertex_ids.SetNumberOfComponents(1)
        self.vertex_ids.SetName(VERTEX_ID)

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
        self.g.GetEdgeData().AddArray(self.edge_weights)
        self.g.GetVertexData().AddArray(self.labels)
        self.g.GetVertexData().AddArray(self.vertex_ids)
        self.g.GetVertexData().SetPedigreeIds(self.vertex_ids)
        self.g.GetVertexData().AddArray(self.glyph_scales)
        self.insert_graph()

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

        for i, entry in enumerate(lgl.split(os.linesep)):
            if self.max_num_of_vertices != -1 and i > self.max_num_of_vertices:
                break

            self.glyph_scales.InsertNextValue(float(1.0))

            if LGLReader.is_starting_vertex(entry):
                self._process_primary_vertex(entry, i)

            else:
                self._process_secondary_vertex(entry, i)

    def _process_secondary_vertex(self, entry, i):
        secondary_label = self.get_secondary_vertex_label(entry)
        s_v = self._add_vertex(i, secondary_label)
        self.g.AddGraphEdge(self.starting_vertex, s_v)
        self.num_of_references += 1

    def _process_primary_vertex(self, entry, i):
        primary_label = self._get_primary_label(entry)
        p_v = self._add_vertex(i, primary_label)
        self._set_primary_vertex_scaling()
        self.starting_vertex = p_v
        self.starting_vertex_index = i
        self.num_of_references = 0

    def _set_primary_vertex_scaling(self):
        if self.starting_vertex_index != -1:
            self.glyph_scales.SetTuple1(self.starting_vertex_index, 0.5 * self.num_of_references)

    def _add_vertex(self, i, label):
        if label not in self.label_vertex_id_map:
            self.labels.InsertNextValue(label)
            vertex_id = self.g.AddVertex(i)
            self.vertex_ids.InsertNextValue(i)
            self.label_vertex_id_map[label] = vertex_id
        else:
            vertex_id = self.label_vertex_id_map[label]

        return vertex_id

    @staticmethod
    def _get_primary_label(entry):
        primary_label = LGLReader.get_primary_vertex(entry)
        if not primary_label:
            raise ValueError
        return primary_label

    def get_secondary_vertex_label(self, entry):
        label_weight = LGLReader.get_vertex_label_and_weight(entry)
        if not label_weight:
            raise ValueError
        if isinstance(label_weight, list):
            secondary_label = label_weight[0]
            self.edge_weights.InsertNextValue(label_weight[1])

        else:
            secondary_label = label_weight
            self.edge_weights.InsertNextValue(0.5)
        return secondary_label
