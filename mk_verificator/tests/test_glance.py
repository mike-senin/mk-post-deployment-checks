import pytest
import time
import subprocess
import mk_verificator.utils as utils


@pytest.fixture
def create_image():
    config = utils.get_configuration(__file__)

    line = 'dd if=/dev/zero of=/tmp/image_mk_framework.dd ' \
           'bs=1M count={}'.format(config['size_image_mb'])

    subprocess.call(line.split())
    yield
    # teardown
    subprocess.call('rm /tmp/image_mk_framework.dd'.split())
    subprocess.call('rm /tmp/image_mk_framework.download'.split())


def test_speed_glance(create_image, glance_client):
    """
    Simplified Performance Tests Download / upload lance

    1. Step download image
    2. Step upload image
    """
    config = utils.get_configuration(__file__)

    image = glance_client.images.create(
        name="test_image",
        disk_format='iso',
        container_format='bare')

    start_time = time.time()
    glance_client.images.upload(
        image.id,
        image_data=open("/tmp/image_mk_framework.dd", 'rb'))
    end_time = time.time()

    speed_upload = int(config['size_image_mb']) / (end_time - start_time)

    start_time = time.time()
    with open("/tmp/image_mk_framework.download", 'wb') as image_file:
        for item in glance_client.images.data(image.id):
            image_file.write(item)
    end_time = time.time()

    speed_download = int(config['size_image_mb']) / (end_time - start_time)

    glance_client.images.delete(image.id)

    print "++++++++++++++++++++++++++++++++++++++++"
    print 'upload - {} Mb/s'.format(speed_upload)
    print 'download - {} Mb/s'.format(speed_download)
