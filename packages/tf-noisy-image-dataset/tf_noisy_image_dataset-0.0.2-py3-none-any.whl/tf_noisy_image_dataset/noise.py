import tensorflow as tf


def draw_gaussian_noise_power(batch_size, noise_power_spec):
    noise_power = tf.random.normal(
        shape=(batch_size,),
        mean=0.0,
        stddev=noise_power_spec,
    )
    return noise_power

def draw_uniform_noise_power(batch_size, noise_power_spec):
    if isinstance(noise_power_spec, (float, int)):
        noise_max = noise_power_spec
        noise_min = 0
    else:
        noise_max = noise_power_spec[1]
        noise_min = noise_power_spec[0]
    noise_power = tf.random.uniform(
        shape=(batch_size,),
        minval=noise_min,
        maxval=noise_max,
    )
    return noise_power

def add_noise(image, noise_power_spec=30, fixed_noise=False, noise_input=False, noise_range_type='gaussian'):
    if fixed_noise:
        noise_power = tf.constant(noise_power_spec, dtype=image.dtype)[None]
    else:
        if noise_range_type == 'gaussian':
            drawing_function = draw_gaussian_noise_power
        elif noise_range_type == 'uniform':
            drawing_function = draw_uniform_noise_power
        noise_power = drawing_function(
            batch_size=tf.shape(image)[0],
            noise_power_spec=noise_power_spec,
        )
    normal_noise = tf.random.normal(
        shape=tf.shape(image),
        mean=tf.cast(0.0, dtype=image.dtype),
        stddev=tf.cast(1.0, dtype=image.dtype),
        dtype=image.dtype,
    )
    noise_power_bdcast = noise_power[:, None, None, None]
    noise = normal_noise * noise_power_bdcast
    image_noisy = image + noise
    # this is to allow quick change in case we want to change the network's
    # input/output
    image_noisy.set_shape([None, None, None, image.shape[-1]])
    if noise_input:
        model_inputs = (image_noisy, noise_power[:, None])
    else:
        model_inputs = image_noisy
    model_outputs = image
    return model_inputs, model_outputs
