from .data_processor import generate_processing_tree, finalize_data, process_variables


def get_data_for_root(project_root):
    processing_tree = generate_processing_tree(project_root)
    data = finalize_data(processing_tree)
    process_variables(data)
    return data
