"""
    PyJAMAS is Just A More Awesome Siesta
    Copyright (C) 2018  Rodrigo Fernandez-Gonzalez (rodrigo.fernandez.gonzalez@utoronto.ca)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Tuple

import keras.layers as kl
import keras.models as km
import keras.optimizers as ko
import keras.preprocessing.image as kpi
import keras.utils as ku
import numpy

from pyjamas.rimage.rimclassifier.rimclassifier import rimclassifier
from pyjamas.rimage.rimclassifier.featurecalculator_rawimage import FeatureCalculatorRawImage
from pyjamas.rimage.rimutils import rimutils
from pyjamas.rutils import RUtils


class DeepCNN(rimclassifier):
    CONV_FILTER_NUMBER: int = 32
    FULLY_CONNECTED_NEURON_NUMBER: int = 512

    OUTPUT_CLASSES: int = 2
    MINI_BATCH_SIZE: int = 32
    EPOCHS: int = 30
    LEARNING_RATE: float = 0.001
    MIN_IMAGE_SIZE = (50, 50, 1)

    def __init__(self, parameters: dict = None):
        """
        The dictionary used for initialization has a 'classifier' attribute that can be
        a DeepCNN object, None, or most often, the result of the get_weights() methods run
        on a Sequential model (for a previously trained network).
        """
        super().__init__(parameters)

        conv_filter_number: int = parameters.get('conv_filter_number', DeepCNN.CONV_FILTER_NUMBER)
        fully_connected_neuron_number = parameters.get('fully_connected_neuron_number', DeepCNN.FULLY_CONNECTED_NEURON_NUMBER)

        output_classes: int = parameters.get('output_classes', DeepCNN.OUTPUT_CLASSES)
        learning_rate: float = parameters.get('learning_rate', DeepCNN.LEARNING_RATE)

        input_size: Tuple[int, int, int] = parameters.get('train_image_size', DeepCNN.MIN_IMAGE_SIZE) + (1,)

        self.epochs: int = parameters.get('epochs', DeepCNN.EPOCHS)
        self.mini_batch_size: int = parameters.get('mini_batch_size', DeepCNN.MINI_BATCH_SIZE)
        self.scaler = None
        self.data_generator = kpi.ImageDataGenerator()

        self.fc = FeatureCalculatorRawImage()

        classifier_representation = parameters.get('classifier')
        if type(classifier_representation) is DeepCNN:
            self.classifier = classifier_representation
        else:
            self.classifier = self.get_3conv2D_model(conv_filter_number, fully_connected_neuron_number, input_size,
                                                     output_classes)

        self.classifier.compile(loss='categorical_crossentropy', optimizer=ko.Adam(learning_rate=learning_rate),
                                metrics=['accuracy'])

        # For pretrained models.
        if type(classifier_representation) is list:
            self.classifier.set_weights(classifier_representation)

    def get_4conv2D_model(self, numfm: int, numnodes: int, input_shape: Tuple[int] = MIN_IMAGE_SIZE,
              output_size: int = OUTPUT_CLASSES) -> km.Sequential:
        """
        This function returns a convolutional neural network Keras model,
        with numfm feature maps in the first convolutional layer,
        2 * numfm in the second convolutional layer, 3* numfm in the third and fourth
        and numnodes neurons in the fully-connected layer.

        Inputs:
        - numfm: int, the number of feature maps in the first convolutional layer.

        - numnodes: int, the number of nodes in the fully-connected layer.

        - intput_shape: Tuple[int], the shape of the input data,
        default = (28, 28, 1).

        - output_size: int, the number of nodes in the output layer,
          default = 10.

        Output: km.Sequential, the constructed Keras model.

        """

        # Initialize the model.
        model: km.Sequential = km.Sequential()

        # Add a 2D convolution layer, with numfm feature maps.
        model.add(kl.Conv2D(numfm, kernel_size=(5, 5),
                            input_shape=input_shape,
                            activation='relu'))

        # Adding batch normalization here  accelerates convergence during training, and improves the accuracy on the test set by 2-5%.
        model.add(kl.BatchNormalization())

        # Add a max pooling layer.
        model.add(kl.MaxPooling2D(pool_size=(2, 2)))

        # Second convolutional layer.
        model.add(kl.Conv2D(numfm * 2, kernel_size=(3, 3), activation='relu'))

        # Add a max pooling layer.
        model.add(kl.MaxPooling2D(pool_size=(2, 2),
                                  strides=(2, 2)))

        # Third convolutional layer.
        model.add(kl.Conv2D(numfm * 3, kernel_size=(3, 3),
                            activation='relu'))

        # Add a max pooling layer.
        model.add(kl.MaxPooling2D(pool_size=(2, 2),
                                  strides=(2, 2)))

        # Fourth convolutional layer.
        model.add(kl.Conv2D(numfm * 3, kernel_size=(3, 3),
                            activation='relu'))

        # Add a max pooling layer.
        model.add(kl.MaxPooling2D(pool_size=(2, 2),
                                  strides=(2, 2)))

        # Convert the network from 2D to 1D.
        model.add(kl.Flatten())

        # Add a fully-connected layer.
        model.add(kl.Dense(numnodes, activation='relu'))

        # Add the output layer.
        model.add(kl.Dense(output_size, activation='softmax'))

        # Return the model.
        return model

    def get_3conv2D_model(self, numfm: int, numnodes: int, input_shape: Tuple[int] = MIN_IMAGE_SIZE,
              output_size: int = OUTPUT_CLASSES) -> km.Sequential:
        """
        This function returns a convolutional neural network Keras model,
        with numfm feature maps in the first convolutional layer,
        2 * numfm in the second convolutional layer, 3* numfm in the third
        and numnodes neurons in the fully-connected layer.

        Inputs:
        - numfm: int, the number of feature maps in the first convolutional layer.

        - numnodes: int, the number of nodes in the fully-connected layer.

        - intput_shape: Tuple[int], the shape of the input data,
        default = (28, 28, 1).

        - output_size: int, the number of nodes in the output layer,
          default = 10.

        Output: km.Sequential, the constructed Keras model.

        """

        # Initialize the model.
        model: km.Sequential = km.Sequential()

        # Add a 2D convolution layer, with numfm feature maps.
        model.add(kl.Conv2D(numfm, kernel_size=(5, 5),
                            input_shape=input_shape,
                            activation='relu'))

        # Adding batch normalization here  accelerates convergence during training, and improves the accuracy on the test set by 2-5%.
        model.add(kl.BatchNormalization())

        # Add a max pooling layer.
        model.add(kl.MaxPooling2D(pool_size=(2, 2)))

        # Second convolutional layer.
        model.add(kl.Conv2D(numfm * 2, kernel_size=(3, 3), activation='relu'))

        # Add a max pooling layer.
        model.add(kl.MaxPooling2D(pool_size=(2, 2),
                                  strides=(2, 2)))

        # Third convolutional layer.
        model.add(kl.Conv2D(numfm * 3, kernel_size=(3, 3),
                            activation='relu'))

        # Add a max pooling layer.
        model.add(kl.MaxPooling2D(pool_size=(2, 2),
                                  strides=(2, 2)))

        # Convert the network from 2D to 1D.
        model.add(kl.Flatten())

        # Add a fully-connected layer.
        model.add(kl.Dense(numnodes, activation='relu'))

        # Add the output layer.
        model.add(kl.Dense(output_size, activation='softmax'))

        # Return the model.
        return model

    # overloaded method.
    def train(self) -> bool:
        if self.features_positive_array is False or self.features_positive_array is None or \
                self.features_negative_array is False or self.features_negative_array is None:
            return False

        features_combined = numpy.vstack((self.features_positive_array, self.features_negative_array))
        class_combined = numpy.concatenate((numpy.ones((self.features_positive_array.shape[0],), dtype=int),
                                            numpy.zeros((self.features_negative_array.shape[0],), dtype=int)))

        if self.scaler is not None:
            self.scaler.fit(features_combined)
            features_combined = self.scaler.transform(features_combined)  # doctest: +SKIP

        class_combined = ku.to_categorical(class_combined, 2)
        self.classifier.fit(features_combined, class_combined, epochs=self.epochs, batch_size=self.mini_batch_size, verbose=2)

        return True

    # overloaded method.
    def predict(self, image: numpy.ndarray) -> (numpy.ndarray, numpy.ndarray):
        if self.fc is None or self.fc is False or image is None or image is False:
            return False

        image = numpy.squeeze(image)

        row_rad = int(numpy.floor(self.train_image_size[0] / 2))
        col_rad = int(numpy.floor(self.train_image_size[1] / 2))

        self.object_positions: list = []
        self.object_map: numpy.ndarray = numpy.zeros(image.shape)

        subimages = rimutils.generate_subimages(image, self.train_image_size, self.step_sz)

        all_images: numpy.ndarray = None
        all_coords: numpy.ndarray = None

        for asubim, row, col in subimages:
            self.fc.calculate_features(asubim)
            if all_images is not None:
                all_images = numpy.vstack((all_images, self.fc.gimme_features()))
                all_coords = numpy.vstack((all_coords, numpy.asarray((row, col))))
            else:
                all_images = self.fc.gimme_features()
                all_coords = numpy.asarray((row, col))

        # Check if image was to small to fill train_image_size, and pad it in that case.
        if all_images is None:
            n_pad_rows: int = self.train_image_size[0] - image.shape[0]
            n_pad_cols: int = self.train_image_size[1] - image.shape[1]

            all_coords = numpy.asarray((int(numpy.floor(image.shape[0]/2)), int(numpy.floor(image.shape[1]/2))))
            image = numpy.pad(image, ((0, n_pad_rows), (0, n_pad_cols)), mode='median')
            self.fc.calculate_features(image)
            all_images = self.fc.gimme_features()


        if all_coords.ndim == 1:
            all_coords = numpy.expand_dims(all_coords, axis=0)

        output = self.classifier.predict(all_images)

        theclass = output.argmax(axis=1)
        theP = numpy.amax(output, axis=1)

        hits = numpy.where(theclass==1)[0]

        self.object_positions = list(all_coords[hits])
        self.object_map[all_coords[hits, 0], all_coords[hits, 1]] = 1
        self.prob_array = theP[hits]
        box_list: list = [[all_coords[ahit][0]-row_rad, all_coords[ahit][1]-col_rad, all_coords[ahit][0]+row_rad, all_coords[ahit][1]+col_rad] for ahit in hits]
        self.box_array = numpy.asarray(box_list)
        if self.train_image_size[0] % 2 == 1:
            self.box_array[:, 2] += 1
        if self.train_image_size[1] % 2 == 1:
            self.box_array[:, 3] += 1

        return self.box_array.copy(), self.prob_array.copy()

    def save_classifier(self, filename: str) -> bool:
        classifier = self.classifier.get_weights() if self.classifier.weights else self.classifier

        theclassifier = {
            'positive_training_folder': self.positive_training_folder,
            'negative_training_folder': self.negative_training_folder,
            'hard_negative_training_folder': self.hard_negative_training_folder,
            'train_image_size': self.train_image_size,
            'scaler': self.scaler,
            'fc': self.fc,
            'step_sz': self.step_sz,
            'iou_threshold': self.iou_threshold,
            'prob_threshold': self.prob_threshold,
            'max_num_objects_dial': self.max_num_objects,
            'classifier': classifier,
            'features_positive_array': self.features_positive_array,
            'features_negative_array': self.features_negative_array,
        }

        return RUtils.pickle_this(theclassifier, RUtils.set_extension(filename, rimclassifier.CLASSIFIER_EXTENSION))
