import cv2
import numpy as np


def pad_x32(image: np.array) -> np.array:

    h, w = image.shape[:2]

    pad_h = np.ceil(h / 32) * 32 - h
    pad_w = np.ceil(w / 32) * 32 - w

    pad_h_top = int(np.floor(pad_h / 2))
    pad_h_bot = int(np.ceil(pad_h / 2))
    pad_w_top = int(np.floor(pad_w / 2))
    pad_w_bot = int(np.ceil(pad_w / 2))

    padding = ((pad_h_top, pad_h_bot), (pad_w_top, pad_w_bot), (0, 0))
    pad = padding[:2] if image.ndim == 2 else padding
    image = np.pad(image, pad, mode="constant", constant_values=0)

    return image


def load_image(file_name: str) -> np.array:
    """
    Helper loads image from file
        Args:
            file_name: (str) name of the image file

        Output: image as a numpy array
    """
    image = cv2.imread(file_name, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image


def normalize_sar(
    img: np.array,
    mean: np.array = [0.485, 0.456, 0.406, 0.406],
    std: np.array = [0.229, 0.224, 0.225, 0.225],
    max_value: float = 92.88,
) -> np.array:
    """
    Normalize image data in 4 channels to 0-1 range,
    then applymenaand std as in ImageNet pretrain, or any other
    """
    mean = np.array(mean, dtype=np.float32)
    mean *= max_value
    std = np.array(std, dtype=np.float32)
    std *= max_value

    img = img.astype(np.float32)
    img = img - mean
    img = img / std

    return img


def preprocess_minmax(img: np.array) -> np.array:
    """
    Normalize image data to 98-2 percentiles

    """
    im_min = np.percentile(img, 2)
    im_max = np.percentile(img, 98)
    im_range = im_max - im_min
    # print(f'percentile 2 {im_min}, percentile 98 {im_max}, im_range {im_range}')

    # Normalise to the percentile
    img = img.astype(np.float32)
    img = (img - im_min) / im_range
    img = img.clip(0, 1)

    return img
