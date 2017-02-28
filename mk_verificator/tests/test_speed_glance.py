import pytest
import os
import time
import mk_verificator.utils as utils


@pytest.fixture
def create_image(nova_client):
    config = utils.get_configuration(__file__)
    name_image = '/tmp/test_image.dd.img'

    line = 'dd if=/dev/zero of={} bs=1M count=' \
           '{}'.format(name_image, config['size_image_mb'])

    os.system(line)
    yield name_image

    # teardown
    os.system('rm {}'.format(name_image))


def test_speed_glance(create_image, glance_client):
    """
    Simplified Performance Tests Download / upload lance

    1. Step download image
    2. Step upload image
    """
    config = utils.get_configuration(__file__)
    name_image = '/tmp/test_image.dd.img'

    image = glance_client.images.create(name="test_image")
    start_time = time.time()
    image = glance_client.images.upload(image.id, open(name_image, 'rb'))
    end_time = time.time()
    speed_download = int(config['size_image_mb']) / int(end_time - start_time)

    print 'download - {} Mb/s'.format(speed_download)

    start_time = time.time()
    glance_client.images.data(image.id)
    end_time = time.time()
    speed_upload = int(config['size_image_mb']) / int(end_time - start_time)

    print 'upload - {} Mb/s'.format(speed_upload)

    glance_client.images.delete(image.id)
