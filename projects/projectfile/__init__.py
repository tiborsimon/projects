from .data_processor import generate_processing_tree, finalize_data


def get_data_for_root(project_root):
    processing_tree = generate_processing_tree(project_root)
    return finalize_data(processing_tree)
