import pytest
from tensorflow.python.keras.datasets import mnist

import autokeras as ak
from tests import utils


@pytest.fixture(scope='module')
def tmp_dir(tmpdir_factory):
    return tmpdir_factory.mktemp('test_io_api')


def test_io_api(tmp_dir):
    (image_x, train_y), (test_x, test_y) = mnist.load_data()
    (text_x, train_y), (test_x, test_y) = utils.imdb_raw()

    num_instances = 20
    image_x = image_x[:num_instances]
    text_x = text_x[:num_instances]
    structured_data_x = utils.generate_structured_data(num_instances=num_instances)
    classification_y = utils.generate_one_hot_labels(num_instances=num_instances,
                                                     num_classes=3)
    regression_y = utils.generate_data(num_instances=num_instances, shape=(1,))

    # Build model and train.
    automodel = ak.AutoModel(
        inputs=[
            ak.ImageInput(),
            ak.TextInput(),
            ak.StructuredDataInput()
        ],
        outputs=[ak.RegressionHead(metrics=['mae']),
                 ak.ClassificationHead(loss='categorical_crossentropy',
                                       metrics=['accuracy'])],
        directory=tmp_dir,
        max_trials=2,
        seed=utils.SEED)
    automodel.fit([
        image_x,
        text_x,
        structured_data_x
    ],
        [regression_y, classification_y],
        epochs=1,
        validation_split=0.2)
