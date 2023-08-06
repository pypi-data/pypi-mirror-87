import re

from savvihub.common.constants import INQUIRER_NAME_IMAGE, INQUIRER_NAME_RESOURCE, INQUIRER_NAME_DATASET


def parse_title(choice):
    numbers = re.findall("[\s+]", choice)
    return numbers[0]


def parse_image_choice(image):
    return f'[{image.image_url}] {image.name}'


def parse_resource_choice(resource):
    return f'[{resource.name}] CPU: {resource.cpu_limit} | Memory: {resource.mem_limit}'


def parse_dataset_choice(dataset, dataset_type):
    return f'[{dataset.workspace.slug}/{dataset.slug}]'


def get_choices(client, req_type, workspace):
    if req_type == INQUIRER_NAME_IMAGE:
        savvi_kernel_images = client.kernel_image_list(workspace)
        choices = [None for _ in savvi_kernel_images]
        for (i, image) in enumerate(savvi_kernel_images):
            choices[i] = parse_image_choice(image)
        return choices
    elif req_type == INQUIRER_NAME_RESOURCE:
        savvi_kernel_resources = client.kernel_resource_list(workspace)
        choices = [None for _ in savvi_kernel_resources]
        for (i, resource) in enumerate(savvi_kernel_resources):
            choices[i] = parse_resource_choice(resource)
        return choices
    elif req_type == INQUIRER_NAME_DATASET:
        savvi_public_dataset = client.public_dataset_list(raise_error=True)
        savvi_private_dataset = client.dataset_list(workspace, raise_error=True)
        choices = []
        for dataset in savvi_public_dataset:
            choices.append(parse_dataset_choice(dataset, 'public'))
        for dataset in savvi_private_dataset:
            choices.append(parse_dataset_choice(dataset, 'private'))
        return choices
    else:
        raise Exception('Wrong type!')

