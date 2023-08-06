# Name: audio.py
# Description: defines functionality to process audio from audio files

import logging
import librosa
import numpy as np
import os
import pkg_resources
import pandas as pd
import glob
import json

from genreml.model.processing.audio_features import SpectrogramGenerator, LibrosaFeatureGenerator, WavePlotGenerator
from genreml.model.processing.config import AudioConfig, DisplayConfig
from genreml.model.utils import file_handling


class Audio(object):

    def __init__(self, file_name: str, audio_signal, sample_rate, file_type: str = AudioConfig.AUDIO_FORMAT):
        """ Instantiates an AudioFile object that collects various attributes related to an audio file and exposes
        methods to extract features from that file
        """
        self.file_name = file_name
        self.audio_type = "." + file_type
        self.audio_signal = audio_signal
        self.sample_rate = sample_rate

    def _get_figure_filepath(self, destination_filepath: str, figure_type: str) -> str:
        return "{0}{1}_{2}".format(
            destination_filepath, figure_type, self.file_name.replace(self.audio_type, ""))

    def _save_figure(self, generator, figure, destination_filepath: str, figure_type: str) -> str:
        path = self._get_figure_filepath(destination_filepath, figure_type)
        logging.info("saving {0} to {1}".format(figure_type, path))
        figure.savefig(path)
        generator.close_img(figure)
        return path + ".png"

    def to_spectrogram(
            self, destination_filepath: str = None, spec_generator=None,
            spectrogram_type: str = "spectrogram", cmap: str = None,
            figure_width: float = DisplayConfig.FIGSIZE_WIDTH, figure_height: float = DisplayConfig.FIGSIZE_HEIGHT):
        """ Extract spectrogram from the audio data and saves the resulting image to the destination path

        :param string destination_filepath: the file path to save the spectrogram to
        :param model.processing.audio_features.SpectrogramGenerator spec_generator: option. spectrogram generator to use
        :param spectrogram_type: the type of spectrogram to generate
        :param cmap: https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.axes.Axes.imshow.html
        :param figure_width: the spectrogram width in inches
        :param figure_height: the spectrogram height in inches
        :returns the full path location of the saved melspetrogram image
        """
        logging.info("generating {0} for {1}".format(spectrogram_type, self.file_name))
        if not spec_generator:
            spec_generator = SpectrogramGenerator(
                self.audio_signal, self.sample_rate, spectrogram_type=spectrogram_type)
        spectrogram = spec_generator.generate(cmap=cmap, figure_width=figure_width, figure_height=figure_height)
        path = None
        if destination_filepath:
            path = self._save_figure(spec_generator, spectrogram, destination_filepath, spectrogram_type)
        return spectrogram, path

    def to_melspectrogram(self, destination_filepath: str = None, spec_generator=None, cmap: str = None,
                          figure_width: float = DisplayConfig.FIGSIZE_WIDTH,
                          figure_height: float = DisplayConfig.FIGSIZE_HEIGHT):
        """ Extract melspectrogram from the audio data and saves the resulting image to the destination path

        :param string destination_filepath: the file path to save the melspectrogram to
        :param model.processing.audio_features.SpectrogramGenerator spec_generator: option. spectrogram generator to use
        :param cmap: https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.axes.Axes.imshow.html
        :param figure_width: the melspectrogram width in inches
        :param figure_height: the melspectrogram height in inches
        :returns the full path location of the saved melspetrogram image
        """
        return self.to_spectrogram(
            destination_filepath, spec_generator, spectrogram_type="melspectrogram", cmap=cmap,
            figure_width=figure_width, figure_height=figure_height)

    def to_chromagram(self, destination_filepath: str = None, spec_generator=None, cmap: str = None,
                      figure_width: float = DisplayConfig.FIGSIZE_WIDTH,
                      figure_height: float = DisplayConfig.FIGSIZE_HEIGHT
                      ):
        """ Extract chromagram from the audio data and saves the resulting image to the destination path

        :param string destination_filepath: the file path to save the chromagram to
        :param model.processing.audio_features.SpectrogramGenerator spec_generator: option. spectrogram generator to use
        :param cmap: https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.axes.Axes.imshow.html
        :param figure_width: the chromogram width in inches
        :param figure_height: the chromogram height in inches
        :returns the full path location of the saved chromagram image
        """
        return self.to_spectrogram(
            destination_filepath, spec_generator, spectrogram_type="chromagram", cmap=cmap,
            figure_width=figure_width, figure_height=figure_height
        )

    def to_waveplot(self, destination_filepath: str = None, waveplot_generator=None, cmap: str = None,
                    figure_width: float = DisplayConfig.FIGSIZE_WIDTH,
                    figure_height: float = DisplayConfig.FIGSIZE_HEIGHT
                    ) -> tuple:
        logging.info("generating waveplot for {0}".format(self.file_name))
        if not waveplot_generator:
            waveplot_generator = WavePlotGenerator(self.audio_signal, self.sample_rate)
        waveplot = waveplot_generator.generate(cmap=cmap, figure_width=figure_width, figure_height=figure_height)
        path = None
        if destination_filepath:
            path = self._save_figure(waveplot_generator, waveplot, destination_filepath, "waveplot")
        return waveplot, path

    def extract_visual_features(
            self, destination_filepath: str = None, cmap: str = DisplayConfig.CMAP, exclusion_set: set = None,
            figure_width: float = DisplayConfig.FIGSIZE_WIDTH, figure_height: float = DisplayConfig.FIGSIZE_HEIGHT
    ) -> tuple:
        visual_features_to_method_map = {
            "spectrogram": self.to_spectrogram,
            "melspectrogram": self.to_melspectrogram,
            "chromagram": self.to_chromagram,
            "waveplot": self.to_waveplot
        }
        visual_features = []
        visual_paths = []
        for feature_name, feature_method in visual_features_to_method_map.items():
            if feature_name not in exclusion_set:
                visual, path = feature_method(destination_filepath, cmap=cmap, figure_width=figure_width,
                                              figure_height=figure_height)
                visual_features.append(visual)
                visual_paths.append(path)

        return visual_features, visual_paths

    def extract_features(self,
                         aggregate_features: bool = True,
                         exclusion_set: set = None,
                         feature_generator: LibrosaFeatureGenerator = None) -> tuple:
        """ Extract librosa features from the audio data

        :param aggregate_features - whether to aggregate the features extracted or not
        :param exclusion_set - an optional set of feature names to exclude from the feature generation
        :param feature_generator - an optional generator to use for generating the features
        :returns a dictionary containing the feature names as keys and the data as values
            and a list of feature names in order of processing
        """
        logging.info("generating librosa features for {0}".format(self.file_name))
        if not feature_generator:
            feature_generator = LibrosaFeatureGenerator(
                self.audio_signal, self.sample_rate, aggregate_features, exclusion_set)
        # Extract features
        features, feature_names = feature_generator.generate()
        # Append the identifiers for the current audio file to the feature object
        features['file_name'] = self.file_name
        logging.info("generated {0} features for {1}".format(len(features), self.file_name))
        return features, feature_names

    def __repr__(self):
        return "Audio file of type {0} with ID {1}".format(self.audio_type, self.file_name)

    def __str__(self):
        return self.__repr__()


class AudioCollection(dict):

    def __init__(self):
        super(AudioCollection, self).__init__()
        self.visual_features = []
        self.visual_paths = []
        self.features = []
        self.feature_names = []
        self.features_saved = []

    @staticmethod
    def clip_audio_signal(audio_signal: np.array, sample_rate, min_clip_length: int) -> np.array:
        length = len(audio_signal) / sample_rate
        # Check to ensure that the clip has the required length
        if length < min_clip_length:
            raise ValueError("Length {0} for the song is shorted than min required length of {1}".format(
                length, min_clip_length))
        # Take middle section of the clip
        # elif length < min_clip_length * 3 + 1:
        else:
            mid_index = int(len(audio_signal) / 2)
            lower_index = mid_index - int(sample_rate * min_clip_length / 2)
            upper_index = lower_index + int(sample_rate * min_clip_length)
            audio_signal = audio_signal[lower_index:upper_index]
        # Split the clip into three subclips of min_clip_length duration
        '''
        else:
            num_clips = 3
            mid_index = int(len(audio_signal) / 2)
            lower_index = mid_index - int(
                sample_rate * (min_clip_length * num_clips / 2))
            tmp_signal = []
            for i in range(num_clips):
                upper_index = lower_index + int(sample_rate * min_clip_length)
                tmp_signal.append(audio_signal[lower_index:upper_index])
                lower_index = upper_index
            audio_signal = tmp_signal'''
        return audio_signal

    def _load_file(self, file_location, file_type: str = AudioConfig.AUDIO_FORMAT):
        """ Reads in a individual file from the given file_location on disk and keeps a record of those files that
        couldn't be read in

        :param string file_location: the path to a file to read in
        """
        try:
            logging.info("loading audio file from {0}".format(file_location))
            audio_signal, sample_rate = librosa.load(file_location)
            audio_signal = self.clip_audio_signal(audio_signal, sample_rate, AudioConfig.MIN_CLIP_LENGTH)
            self[file_location] = Audio(
                file_handling.get_filename(file_location), audio_signal, sample_rate, file_type=file_type)
        except Exception as e:
            logging.warning("failed to load audio file from {0} due to {1}".format(file_location, e))
            logging.warning(e)

    def _run_feature_extraction(
            self, audio_object, destination_filepath=None,
            features_to_exclude=None, cmap=DisplayConfig.CMAP,
            figure_width: float = DisplayConfig.FIGSIZE_WIDTH, figure_height: float = DisplayConfig.FIGSIZE_HEIGHT
    ):
        """ Extracts features from a given AudioFile object representing a file in the given file_location and
        saves the features to destination_filepath

        :param Audio audio_object: an Audio class instance
        :param string destination_filepath: the filepath to save the extracted features to
        :param set features_to_exclude: a collection of feature names to exclude from the final result
        """
        if not features_to_exclude:
            features_to_exclude = set()
        try:
            if destination_filepath:
                destination_filepath = destination_filepath.replace(" ", "")
                visual_features, visual_paths = audio_object.extract_visual_features(destination_filepath, cmap=cmap,
                                                                                     exclusion_set=features_to_exclude,
                                                                                     figure_width=figure_width,
                                                                                     figure_height=figure_height)
                self.visual_features.append(visual_features)
                self.visual_paths.append(visual_paths)
            feature_dict, feature_names_list = audio_object.extract_features(exclusion_set=features_to_exclude)
            self.features.append(feature_dict)
            self.feature_names.append(feature_names_list)
        except Exception as e:
            logging.warning("failed to extract features from {0}".format(audio_object))
            logging.warning(e)

    @staticmethod
    def _initialize_feature_destination(destination_filepath: str) -> str:
        """ Creates a directory in which to store exported audio features under the given filepath

        :param destination_filepath - the path to a directory in which to store exported features
        :retuns the full path where the features will be saved in
        """
        if destination_filepath:
            destination_filepath = destination_filepath + AudioConfig.FEATURE_DESTINATION
            file_handling.create_directory(destination_filepath)
        return destination_filepath

    def to_df(self):
        """ Store the list of feature dictionaries in a Pandas dataframe where the keys become the columns

        :returns a pandas data frame representation of the audio features
        """
        df = pd.DataFrame()
        record_count = 0
        for idx, feature_dict in enumerate(self.features):
            record_count += 1
            if idx == 0:
                record_to_insert = {key: [val] for key, val in feature_dict.items()}
                df = pd.DataFrame(record_to_insert)
            else:
                df = df.append(feature_dict, ignore_index=True)
        return df, record_count

    def to_csv(self, destination_filepath: str):
        """ Creates a data frame of the features extracted from the current audio files and saves a CSV representation
        of it to the given filepath

        :param destination_filepath - the path to the directory to save the CSV in
        :returns the data frame of features that was saved as CSV
        """
        df, record_count = self.to_df()
        csv_filepath = "{0}{1}{2}.csv".format(destination_filepath, 'feature_data_', str(os.getpid()))
        if file_handling.file_exists(csv_filepath):
            logging.info(
                "appending feature data frame containing {0} records to {1}".format(record_count, csv_filepath))
            df.to_csv(csv_filepath, float_format='%.{}e'.format(10), header=False, index=False, mode='a')
        else:
            logging.info(
                "writing feature data frame containing {0} records to {1}".format(record_count, csv_filepath))
            df.to_csv(csv_filepath, float_format='%.{}e'.format(10), index=False, mode='w')
        return df, csv_filepath

    def _checkpoint_feature_extraction(self, destination_filepath, clear_features=True):
        logging.info("checkpointing progress to {0}".format(destination_filepath))
        _, _ = self.to_csv(destination_filepath)
        self.features_saved.extend(self.features)
        if clear_features:
            self.features = []

    def to_json(self, filepath):
        """ Serializes self as a json in a given file path

        :param string filepath: the file path to save the JSON to
        """
        with open(filepath, 'w') as outfile:
            json.dump(self, outfile)

    @property
    def audio_data(self) -> tuple:
        """ Generates a tuple containing the name of the audio object in the collection, its audio signal data,
        and the sample rate
        """
        for audio_name, audio_obj in self.items():
            yield audio_name, audio_obj.audio_signal, audio_obj.sample_rate


class AudioFiles(AudioCollection):

    def __init__(self):
        """ Instantiates a collection of AudioFile objects represented as a dictionary where each key is the audio
        file's location on disk and each value the corresponding AudioFile object """
        super(AudioFiles, self).__init__()

    def extract_features(self,
                         file_locations, destination_filepath=None, features_to_exclude=None,
                         load=True, audio_format=AudioConfig.AUDIO_FORMAT, cmap=DisplayConfig.CMAP,
                         figure_width: float = DisplayConfig.FIGSIZE_WIDTH,
                         figure_height: float = DisplayConfig.FIGSIZE_HEIGHT
                         ):
        """ Iterates over all of the files in the file_locations, loads them in to extract audio data, and
        generates features

        :param string file_locations: either the location of a single audio file or directory of files to process
        :param string destination_filepath: the location to save features in
        :param set features_to_exclude: a collection of feature names to exclude from the final result
        :param bool load: whether to load the files before extracting the features
        :param string audio_format: the format of the audio files in directory (wav, mp3, etc.)
        :param cmap: https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.axes.Axes.imshow.html
        :param figure_width: the visual feature figure width in inches
        :param figure_height: the visual feature figure height in inches
        """
        self.features, self.features_saved = [], []
        destination_filepath = self._initialize_feature_destination(destination_filepath)
        # Only load in and process a single file if the given location a file
        if os.path.isfile(file_locations):
            if load:
                self._load_file(file_locations, file_type=audio_format)
            self._run_feature_extraction(
                self[file_locations], destination_filepath, features_to_exclude,
                cmap=cmap, figure_width=figure_width, figure_height=figure_height

            )
        # Load in all applicable files if the given location is a directory
        elif os.path.isdir(file_locations):
            logging.info("extracting features from {0} audio files in directory {1}".format(
                audio_format, file_locations))
            if file_locations[-1] == '/':
                file_locations = file_locations[:-1]
            # Retrieve list of files in directory with the matching audio format
            audio_files_in_dir = glob.glob("{0}/*.{1}".format(file_locations, audio_format))
            # Iterate over each file in the directory, load in if applicable, and extract features
            for idx, file in enumerate(audio_files_in_dir):
                if load:
                    self._load_file(file, file_type=audio_format)
                try:
                    self._run_feature_extraction(
                        self[file], destination_filepath, features_to_exclude,
                        cmap=cmap, figure_width=figure_width, figure_height=figure_height
                    )
                    # Checkpoint features every AudioConfig.CHECKPOINT_FREQUENCY tracks
                    if (idx + 1) % AudioConfig.CHECKPOINT_FREQUENCY == 0 and destination_filepath:
                        self._checkpoint_feature_extraction(destination_filepath)
                except Exception as e:
                    logging.critical("could not run feature extraction for {0}".format(file))
                    logging.critical(e)
                    if destination_filepath:
                        self._checkpoint_feature_extraction(destination_filepath)
        else:
            raise RuntimeError("file location {0} given to load audio clips from is invalid".format(file_locations))
        if destination_filepath:
            self._checkpoint_feature_extraction(destination_filepath)

    def extract_sample_fma_features(self, destination_filepath=None, audio_format=AudioConfig.AUDIO_FORMAT):
        """ Retrieves audio features from sample FMA audio files packaged with the application in genreml/fma_data

        :param str destination_filepath: the optional path to save features to as part of regular feature extraction
        :param string audio_format: the format of the audio files in directory (wav, mp3, etc.)
        """
        path = pkg_resources.resource_filename('genreml', 'fma_data/')
        self.extract_features(
            path, destination_filepath=destination_filepath, audio_format=audio_format)


class AudioData(AudioCollection):

    def __init__(self, audio_signal_data: any, sample_rate_data: any):
        """ Creates AudioData collection containing the raw data for each audio file

       :param audio_signal_data - a collection of individual audio signal arrays or list for each audio file
       :param sample_rate_data - a collection of individual sample rate arrays or list for each audio file
       """
        super(AudioData, self).__init__()
        if len(audio_signal_data) != len(sample_rate_data):
            raise ValueError("The given data for audio signal and sample rate must be the same length")
        self.audio_signal_data = audio_signal_data
        self.sample_rate_data = sample_rate_data
        self.init()

    def init(self) -> None:
        """ Initializes the collection of audio objects for each entry in the audio signal and sample rate data
        """
        audio_count = 1
        # Create individual audio file objects for each signal and sample rate structures in the data
        for audio_signal_data, audio_sample_rate_data in zip(self.audio_signal_data, self.sample_rate_data):
            file_name = "AudioFile{0}".format(audio_count)
            self[file_name] = Audio(file_name, audio_signal_data, audio_sample_rate_data)
            audio_count += 1

    def extract_features(self, destination_filepath: str = None, features_to_exclude: set = None,
                         cmap: str = DisplayConfig.CMAP, figure_width: float = DisplayConfig.FIGSIZE_WIDTH,
                         figure_height: float = DisplayConfig.FIGSIZE_HEIGHT
                         ) -> None:
        """ Iterates over all of the audio data in the collection and generates relevant features

        :param string destination_filepath: the location to save features in
        :param set features_to_exclude: a collection of feature names to exclude from the final result
        :param cmap: https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.axes.Axes.imshow.html
        :param figure_width: the visual feature figure width in inches
        :param figure_height: the visual feature figure height in inches
        """
        self.features, self.features_saved = [], []
        destination_filepath = self._initialize_feature_destination(destination_filepath)
        # Only load in and process a single file if the given location a file
        for _, audio_object in self.items():
            self._run_feature_extraction(audio_object=audio_object, destination_filepath=destination_filepath,
                                         features_to_exclude=features_to_exclude,
                                         cmap=cmap, figure_width=figure_width, figure_height=figure_height)
