PRIMARY_VERTEX_TAG = '#'


class LGLReader(object):
    @staticmethod
    def is_starting_vertex(label):
        return True if label and len(label) > 1 and PRIMARY_VERTEX_TAG == label[0] else False

    @staticmethod
    def get_primary_vertex(entry):
        if entry and PRIMARY_VERTEX_TAG in entry:
            split_entry = entry.split()
            if len(split_entry) > 1:
                return split_entry[1]

        return None

    @staticmethod
    def get_vertex_label_and_weight(entry):
        if entry:
            split_entry = entry.split()
            if len(split_entry) == 1:
                return split_entry[0]

            if len(split_entry) == 2:
                label = split_entry[0]
                weight = float(split_entry[1])
                return [label, weight]

        return None

    @staticmethod
    def get_edge_color_entry(entry):
        if not entry:
            return None

        split_entry = entry.split()
        if len(split_entry) != 5:
            return None

        v1 = split_entry[0]
        v2 = split_entry[1]
        try:
            r = float(split_entry[2])
            g = float(split_entry[3])
            b = float(split_entry[4])
        except ValueError:
            return None

        return (v1, v2), (r, g, b)
