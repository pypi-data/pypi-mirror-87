import argparse
import logging
import pkg_resources
from PIL import Image
import numpy as np
import pandas as pd

from genreml.model.acquisition import extraction
from genreml.model.processing import audio, config
from genreml.model.cnn import cnn, config as model_config
from genreml.model.utils import string_parsing, file_handling, logger, model_utils


def parse_args():
    """ Parse arguments passed in via the CLI

    :returns a parsed argument object from argparse
    """
    parser = argparse.ArgumentParser()
    # Accept the operation to perform
    parser.add_argument('operation', choices=['download', 'process', 'classify'], help='''the operation to perform:
    download - search for and download an audio clip for the given song name and artist  
    process - extract data from an audio clip stored in a given file path
    classify - categorize song data into genres using genreml machine learning model 
    ''')
    parser.add_argument('-s', '--song_name', help='the name of the song to download')
    parser.add_argument('-a', '--artist_name', help='the name of song\'s artist')
    parser.add_argument('-fp', '--file_path', help='the file path of an audio clip or directory of clips to process')
    parser.add_argument('-yu', '--youtube_url', help='url to youtube song ')
    parser.add_argument('-ex', '--example', action='store_true', help='whether to run an example of feature extraction')
    parser.add_argument('-dp', '--destination_path', help='where to store the results of feature processing')
    parser.add_argument('-mp', '--model_path', help='the file path to an .h5 file of a classification model')
    parser.add_argument('-e', '--exclude_features', help='a list of feature names to exclude from processing')
    parser.add_argument(
        '-af', '--audio_format', default=config.AudioConfig.AUDIO_FORMAT, help='the format of the audio to process')
    parser.add_argument(
        '-cmap', '--cmap', default=config.DisplayConfig.CMAP,
        help='matplotlib colormap https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html ("None" = default color)'
    )
    parser.add_argument(
        '-fw', '--figure_width', default=config.DisplayConfig.FIGSIZE_WIDTH, help='the width of the figures created')
    parser.add_argument(
        '-fh', '--figure_height', default=config.DisplayConfig.FIGSIZE_HEIGHT, help='the height of the figures created')
    parser.add_argument(
        '-cf', '--checkpoint_frequency', default=config.AudioConfig.CHECKPOINT_FREQUENCY,
        help='how many tracks to process before saving features'
    )
    return parser.parse_args()


def validate_args(args):
    """ Validates the arguments passed in via the CLI """
    if args.operation == 'download' and not (args.song_name and args.artist_name):
        raise RuntimeError('both the song name and artist must be provided to download a clip')
    elif args.operation == 'process' and not (args.file_path or args.example):
        raise RuntimeError(
            'you must either pass in a path to an audio file to process or a path to a directory with audio files')
    elif args.operation == 'classify' and not (args.file_path or args.youtube_url or args.example):
        raise RuntimeError(
            'you must either pass in a path to an audio file or a url to YouTube song')
    elif args.operation == 'process' and args.example and not args.destination_path:
        raise RuntimeError(
            'if running an example feature extraction you must provide a destination path to save the results in'
        )


def set_config(args):
    """ Sets any config attributes provided through CLI """
    # Set the audio format to use in processing
    config.AudioConfig.AUDIO_FORMAT = args.audio_format
    # Set the checkpointing frequency in number of tracks processed
    config.AudioConfig.CHECKPOINT_FREQUENCY = args.checkpoint_frequency


def get_audio_data(args):
    if args.file_path:
        return
    elif args.youtube_url:
        extractor = extraction.SongExtractor()
        extractor.extract(file_path=model_config.FMAModelConfig.TMP_SONG_PATH, yt_url=args.youtube_url)
        args.file_path = '{0}.{1}'.format(model_config.FMAModelConfig.TMP_SONG_PATH,
                                          model_config.AudioConfig.AUDIO_FORMAT)
    elif args.example:
        args.file_path = pkg_resources.resource_filename('genreml', 'fma_data/000002.mp3')
        return


def run(args):
    """ Run the operation as specified via CLI argument """
    # Download clips
    if args.operation == 'download':
        extractor = extraction.SongExtractor()
        extractor.extract(args.song_name, args.artist_name)
    # Extract features from clips
    elif args.operation == 'process':
        processor = audio.AudioFiles()
        features_to_exclude = string_parsing.str_to_collection(args.exclude_features, set)
        cmap = args.cmap
        if cmap.lower() == "none":
            cmap = None
        # Define the destination path
        if not args.destination_path and not args.example:
            # Use same path as input file_path if a -dp is not provided
            feature_destination_path = file_handling.get_parent_directory(args.file_path)
        else:
            # Otherwise use the path provided via -dp; if running example, always require a destination path
            feature_destination_path = args.destination_path
        # Run the feature extraction
        if args.example:
            processor.extract_sample_fma_features(
                destination_filepath=feature_destination_path, audio_format=args.audio_format)
        else:
            processor.extract_features(args.file_path, feature_destination_path,
                                       features_to_exclude=features_to_exclude,
                                       cmap=cmap, figure_width=float(args.figure_width),
                                       figure_height=float(args.figure_height),
                                       audio_format=args.audio_format
                                       )

    elif args.operation == 'classify':
        # check for model_path, default to FMA_model if not specified
        if args.model_path:
            print(args.model_path)
            model = cnn.CnnModel.from_h5_file(args.model_path)
        else:
            # download FMA file if not located in model/cnn/data directory
            if not file_handling.file_exists(model_config.FMAModelConfig.FMA_MODEL_PATH):
                model_utils.download_model()
            # load keras model
            model = cnn.CnnModel.from_h5_file(model_config.FMAModelConfig.FMA_MODEL_PATH)

        # get input data
        get_audio_data(args)

        # run model prediction
        prediction = model.get_prediction(audio_path=args.file_path)

        # display prediction results
        # Log top 5 predictions to console
        n = 5
        top_n_genres = []
        top_n = np.argsort(prediction)
        top_n = top_n[::-1][:n]
        for i, val in enumerate(top_n, start=1):
            top_n_genres.append(pd.read_csv(model_config.FMAModelConfig.LABELS_PATH)['category'][val])
        print(f'\nTop 5 predicted genres: {top_n_genres}\n')

        if args.youtube_url:
            # delete temporary audio file
            file_handling.delete_file(args.file_path)


def main():
    # Step 1: parse the arguments passed in via the CLI
    args = parse_args()
    # Step 2: validates that the arguments passed in are correct; throws exception if not the case
    validate_args(args)
    # Step 3: Set the config with any eligible inputs to update configs with
    set_config(args)
    # Step 4: Set up logger
    logger.setup_logger()
    # Step 5: run the operation
    run(args)


if __name__ == '__main__':
    main()
