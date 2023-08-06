class RunMock:

    def __init__(self, exp):
        self.experiment = exp

    def add_properties(self, properties):
        self.properties = properties


class ExperimentMock:

    def __init__(self, ws):
        self.workspace = ws


class WorkspaceMock:

    def __init__(self, datastore):
        self._datastore = datastore

    def get_default_datastore(self):
        return self._datastore


class DatastoreMock:

    def __init__(self, name):
        self.name = name
        self.files = []
        self.dataset_file_content = []

    def path(self, file_path):
        return file_path

    def upload_files(self, files, relative_root=None, target_path=None, overwrite=False):
        self.files.append((files, relative_root, target_path, overwrite))
        if relative_root is None and len(files) == 1:
            with open(files[0], "r") as f:
                self.dataset_file_content = f.readlines()


class DatasetMock:

    def __init__(self, id):
        self.id = id


class LabeledDatasetFactoryMock:

    def __init__(self, dataset_id):
        self.task = ""
        self.path = ""
        self.dataset_id = dataset_id

    def from_json_lines(self, task, path):
        self.task = task
        self.path = path
        return DatasetMock(self.dataset_id)
