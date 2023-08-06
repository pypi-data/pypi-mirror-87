import inspect
import typeguard
import typing


class AnnotatedObject:
    def __init__(self, d: dict):
        resolved_types = {}
        for cls in self.__class__.mro():
            annotations = getattr(cls, '__annotations__', None)
            if annotations is None:
                continue

            for k, type_ in annotations.items():
                if k in resolved_types:
                    continue

                v = d.get(k, None)
                resolved_types[k] = type_

                if inspect.isclass(type_) and issubclass(type_, AnnotatedObject):
                    v = type_(v)
                else:
                    typeguard.check_type(k, v, type_)
                setattr(self, k, v)
        self.d = d

    def __str__(self):
        return f'[{self.__class__.__name__}] {self.d}'

    @property
    def dict(self):
        return self.d


class SavviHubUser(AnnotatedObject):
    id: int
    username: str
    name: str
    github_authorized: bool


class SavviHubWorkspace(AnnotatedObject):
    id: int
    slug: str


class SavviHubDatasetSource(AnnotatedObject):
    type: str
    support_snapshot: bool
    bucket_name: typing.Optional[str]
    path: typing.Optional[str]


class SavviHubDataset(AnnotatedObject):
    id: int
    workspace: SavviHubWorkspace
    slug: str
    main_volume_id: int
    source: SavviHubDatasetSource


class SavviHubFileObject(AnnotatedObject):
    path: str

    size: int
    hash: str

    download_url: typing.Optional[typing.Dict]
    upload_url: typing.Optional[typing.Dict]

    is_dir: typing.Optional[bool]


class SavviHubKernelImage(AnnotatedObject):
    id: int
    image_url: str
    name: str


class SavviHubKernelResource(AnnotatedObject):
    id: int
    name: str
    cpu_limit: float
    mem_limit: str


class SavviHubSnapshot(AnnotatedObject):
    id: int
    name: str
    size: int


class SavviHubProject(AnnotatedObject):
    id: int
    workspace: SavviHubWorkspace
    slug: str


class SavviHubExperiment(AnnotatedObject):
    class KernelImage(AnnotatedObject):
        name: str
        image_url: str
        language: str

    class KernelResourceSpec(AnnotatedObject):
        name: str
        cpu_type: str
        cpu_limit: int
        cpu_guarantee: int
        mem_limit: str
        mem_guarantee: str
        gpu_type: str
        gpu_limit: int
        gpu_guarantee: int

    id: int
    slug: str
    created_dt: str
    updated_dt: str
    number: int
    message: str
    status: str
    tensorboard_log_dir: typing.Optional[str]
    kernel_image: KernelImage
    kernel_resource_spec: KernelResourceSpec
    env_vars: typing.Optional[typing.Dict]
    datasets: typing.Optional[typing.List]
    tensorboard: typing.Optional[str]
    histories: typing.Optional[typing.List]
    output_volume_id: int
    metrics: typing.Optional[typing.List]
    source_code_link: str
    start_command: str


class SavviHubExperimentLog(AnnotatedObject):
    container: str
    stream: str
    message: str
    timestamp: float


class SavviHubExperimentMetric(AnnotatedObject):
    step: int
    value: str
    timestamp: float


class SavviHubListResponse(AnnotatedObject):
    results: typing.List


class PaginatedMixin(AnnotatedObject):
    total: int
    startCursor: typing.Optional[str]
    endCursor: typing.Optional[str]
    results: typing.List


class SavviHubVolume(AnnotatedObject):
    id: int
    created_dt: str
    updated_dt: str
    role_type: str
    workspace: typing.Optional[typing.Dict]
    project: typing.Optional[typing.Dict]
    dataset: typing.Optional[typing.Dict]
    experiment: typing.Optional[typing.Dict]


class SavviHubFileMetadata(AnnotatedObject):
    path: str
