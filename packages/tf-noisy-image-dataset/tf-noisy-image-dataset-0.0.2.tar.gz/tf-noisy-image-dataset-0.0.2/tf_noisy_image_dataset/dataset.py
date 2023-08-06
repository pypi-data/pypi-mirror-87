from functools import partial

import tensorflow as tf

from tf_noisy_image_dataset.noise import add_noise


class NoisyDatasetBuilder:
    def __init__(
            self,
            paths,
            extension='jpg',
            n_samples=None,
            shuffle=False,
            to_grey=False,
            patch_size=None,
            batch_size=32,
            noise_config=None,
            repeat=True,
            prefetch=True,
        ):
        # TODO: in the future allow to have a custom dataset as input
        # TODO: in a next future allow to use tensorflow image datasets
        if not isinstance(paths, (list, tuple)):
            paths = [paths]
        self.paths = paths
        self.extension = extension
        self.n_samples = n_samples
        self.shuffle = shuffle
        self.to_grey = to_grey
        self.batch_size = batch_size
        self.patch_size = patch_size
        if noise_config is None:
            noise_config = {}
        self.noise_config = noise_config
        self.repeat = repeat
        self.prefetch = prefetch
        self._get_files_ds()
        if self.n_samples is not None:
            self.file_ds = self.file_ds.take(n_samples)
        if self.shuffle:
            self.file_ds = self.file_ds.shuffle(
                800,
                seed=0,
                reshuffle_each_iteration=False,
            )
        self.clean_image_ds = self.files_ds.map(
            self.process_clean_image,
            num_parallel_calls=tf.data.experimental.AUTOTUNE
        )
        self.clean_image_ds = self.clean_image_ds.batch(self.batch_size)
        self.noisy_image_ds = self.clean_image_ds.map(
            partial(
                add_noise,
                **self.noise_config,
            ),
            num_parallel_calls=tf.data.experimental.AUTOTUNE,
        )
        if self.repeat:
            self.noisy_image_ds = self.noisy_image_ds.repeat()
        if self.prefetch:
            self.noisy_image_ds = self.noisy_image_ds.prefetch(
                buffer_size=tf.data.experimental.AUTOTUNE,
            )

    def _get_files_ds(self):
        files_ds = None
        for path in self.paths:
            files_ds_new = tf.data.Dataset.list_files(
                f'{path}/*.{self.extension}',
                shuffle=False,
            )
            if files_ds is None:
                files_ds = files_ds_new
            else:
                files_ds.concatenate(files_ds_new)
        self.files_ds = files_ds

    def process_clean_image(self, filename):
        image_bytes = tf.io.read_file(filename)
        n_channels = 1 if self.to_grey else 3
        image = tf.io.decode_image(image_bytes, channels=n_channels)
        # TODO: allow for different normalisations
        image = (image / 255) - 0.5
        image.set_shape([None, None, n_channels])
        if self.patch_size is not None:
            patch = tf.image.random_crop(
                image,
                [self.patch_size, self.patch_size, 1],
                seed=0,
            )
            return patch
        return image
