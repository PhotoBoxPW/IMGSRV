import random
import math
from decimal import Decimal
from numbers import Real
from typing import Callable, List, Optional, Sequence, Tuple, Union

import numpy as np
from PIL import Image, ImageSequence, ImageChops, ImageColor


class ImageGlitcher:
    # Handles Image/GIF Glitching Operations

    __version__ = '1.0.2'

    def __init__(self):
        # Setting up global variables needed for glitching
        self.pixel_tuple_len = 0
        self.img_width, self.img_height = 0, 0
        self.img_mode = 'Unknown'

        # Creating 3D arrays for pixel data
        self.inputarr = None
        self.outputarr = None

        # Setting glitch_amount max and min
        self.glitch_max = 10.0
        self.glitch_min = 0.1

    def __fetch_image(self, src_img: Image.Image) -> Image.Image:
        if src_img.format == 'GIF':
            # Do not convert GIF file
            return src_img
        elif src_img.format == 'PNG':
            # Convert the Image to RGBA if it's png
            img = src_img.convert('RGBA')
        else:
            # Otherwise convert it to RGB
            img = src_img.convert('RGB')
        return img

    def glitch_image(self, src_img: Image.Image, glitch_amount: Union[int, float], seed: Optional[Union[int, float]] = None,
                     color_offset: bool = False, scan_lines: bool = False) -> Image.Image:
        """
        Sets up values needed for glitching the image
        Returns created Image object if gif=False
        Returns list of Image objects if gif=True
        PARAMETERS:-
        src_img: Either the path to input Image or an Image object itself
        glitch_amount: Level of glitch intensity, [0.1, 10.0] (inclusive)
        color_offset: Specify True if color_offset effect should be applied
        scan_lines: Specify True if scan_lines effect should be applied
        seed: Set a random seed for generating similar images across runs,
            defaults to None (random seed).
        """

        self.seed = seed
        if self.seed:
            # Set the seed if it was given
            self.__reset_rng_seed()

        try:
            # Get Image, whether input was an str path or Image object
            # GIF input is NOT allowed in this method
            img = self.__fetch_image(src_img)
        except FileNotFoundError:
            # Throw DETAILED exception here (Traceback will be present from previous exceptions)
            raise FileNotFoundError(f'No image found at given path: {src_img}')
        except:
            # Throw DETAILED exception here (Traceback will be present from previous exceptions)
            raise Exception(
                'File format not supported - must be a non-animated image file')

        # Fetching image attributes
        self.pixel_tuple_len = len(img.getbands())
        self.img_width, self.img_height = img.size
        self.img_mode = img.mode

        # Assigning the 3D arrays with pixel data
        self.inputarr = np.asarray(img)
        self.outputarr = np.array(img)

        return self.__get_glitched_img(glitch_amount, color_offset, scan_lines)

    def glitch_gif(self, src_gif: Image.Image, glitch_amount: Union[int, float], seed: Union[int, float] = None, glitch_change: Union[int, float] = 0.0,
                   color_offset: bool = False, scan_lines: bool = False, gif: bool = False, cycle: bool = False, step=1) -> Tuple[List[Image.Image], float, int]:
        """
         Glitch each frame of input GIF
         Returns the following:
         * List of PngImage objects,
         * Average duration (in centiseconds)
           of each frame in the original GIF,
         * Number of frames in the original GIF
         NOTE: This is a time consuming process, especially for large GIFs
               with many frames
         PARAMETERS:-
         src_gif: Either the path to input Image or an Image object itself
         glitch_amount: Level of glitch intensity, [0.1, 10.0] (inclusive)
         glitch_change: Increment/Decrement in glitch_amount after every glitch
         cycle: Whether or not to cycle glitch_amount back to glitch_min or glitch_max
                if it over/underflows
         color_offset: Specify True if color_offset effect should be applied
         scan_lines: Specify True if scan_lines effect should be applied
         step: Glitch every step'th frame, defaults to 1 (i.e all frames)
         seed: Set a random seed for generating similar images across runs,
               defaults to None (random seed)
        """

        self.seed = seed
        if self.seed:
            # Set the seed if it was given
            self.__reset_rng_seed()

        gif = self.__fetch_image(src_gif)

        i = 0
        duration = 0
        glitched_imgs = []
        for frame in ImageSequence.Iterator(gif):
            """
             * Save each frame in the temp directory (always png)
             * Glitch the saved image
             * Save the glitched image in temp directory
             * Open the image and append a copy of it to the list
            """
            try:
                duration += frame.info['duration']
            except KeyError as e:
                # Override error message to provide more info
                e.args = (
                    'The key "duration" does not exist in frame.'
                    'This means PIL(pillow) could not extract necessary information from the input image',
                )
                raise
            if not i % step == 0:
                # Only every step'th frame should be glitched
                # Other frames will be appended as they are
                glitched_imgs.append(frame.copy())
                i += 1
                continue
            glitched_img: Image.Image = self.glitch_image(frame, glitch_amount,
                                                          color_offset=color_offset, scan_lines=scan_lines)
            glitched_imgs.append(glitched_img.copy())
            # Change glitch_amount by given value
            glitch_amount = self.__change_glitch(
                glitch_amount, glitch_change, cycle)
            i += 1

        return glitched_imgs, duration / i, i

    def glitch_image_to_gif(self, src_img: Image.Image, glitch_amount: Union[int, float], seed: Optional[Union[int, float]] = None, glitch_change: Union[int, float] = 0.0,
                     color_offset: bool = False, scan_lines: bool = False, cycle: bool = False, frames: int = 23, step: int = 1) -> List[Image.Image]:
        """
         Sets up values needed for glitching the image
         Returns created Image object if gif=False
         Returns list of Image objects if gif=True
         PARAMETERS:-
         src_img: Either the path to input Image or an Image object itself
         glitch_amount: Level of glitch intensity, [0.1, 10.0] (inclusive)
         glitch_change: Increment/Decrement in glitch_amount after every glitch
         cycle: Whether or not to cycle glitch_amount back to glitch_min or glitch_max
                if it over/underflows
         color_offset: Specify True if color_offset effect should be applied
         scan_lines: Specify True if scan_lines effect should be applied
         frames: How many glitched frames should be generated for GIF
         step: Glitch every step'th frame, defaults to 1 (i.e all frames)
         seed: Set a random seed for generating similar images across runs,
               defaults to None (random seed).
        """

        self.seed = seed
        if self.seed:
            # Set the seed if it was given
            self.__reset_rng_seed()

        img = self.__fetch_image(src_img)

        # Fetching image attributes
        self.pixel_tuple_len = len(img.getbands())
        self.img_width, self.img_height = img.size
        self.img_mode = img.mode

        # Assigning the 3D arrays with pixel data
        self.inputarr = np.asarray(img)
        self.outputarr = np.array(img)

        glitched_imgs = []
        for i in range(frames):
            """
             * Glitch the image for n times
             * Where n is 0,1,2...frames
             * Save the image the in temp directory
             * Open the image and append a copy of it to the list
            """
            if not i % step == 0:
                # Only every step'th frame should be glitched
                # Other frames will be appended as they are
                glitched_imgs.append(img.copy())
                continue
            glitched_img = self.__get_glitched_img(
                glitch_amount, color_offset, scan_lines)
            glitched_imgs.append(glitched_img)
            # Change glitch_amount by given value
            glitch_amount = self.__change_glitch(
                glitch_amount, glitch_change, cycle)

        return glitched_imgs

    def __change_glitch(self, glitch_amount: Union[int, float], glitch_change: Union[int, float], cycle: bool) -> float:
        # A function to change glitch_amount by given increment/decrement
        glitch_amount = float(Decimal(glitch_amount) + Decimal(glitch_change))
        # glitch_amount must be between glith_min and glitch_max
        if glitch_amount < self.glitch_min:
            # If it's less, it will be cycled back to max when cycle=True
            # Otherwise, it'll stay at the least possible value -> glitch_min
            glitch_amount = float(
                Decimal(self.glitch_max) + Decimal(glitch_amount)) if cycle else self.glitch_min
        if glitch_amount > self.glitch_max:
            # If it's more, it will be cycled back to min when cycle=True
            # Otherwise, it'll stay at the max possible value -> glitch_max
            glitch_amount = float(Decimal(glitch_amount) % Decimal(
                self.glitch_max)) if cycle else self.glitch_max
        return glitch_amount

    def __get_glitched_img(self, glitch_amount: Union[int, float], color_offset: int, scan_lines: bool) -> Image.Image:
        """
         Glitches the image located at given path
         Intensity of glitch depends on glitch_amount
        """
        max_offset = int((glitch_amount ** 2 / 100) * self.img_width)
        doubled_glitch_amount = int(glitch_amount * 2)
        for shift_number in range(0, doubled_glitch_amount):

            if self.seed:
                # This is not deterministic as glitch amount changes the amount of shifting,
                # so get the same values on each iteration on a new pseudo-seed that is
                # offseted by the index we're iterating
                self.__reset_rng_seed(offset=shift_number)

            # Setting up offset needed for the randomized glitching
            current_offset = random.randint(-max_offset, max_offset)

            if current_offset == 0:
                # Can't wrap left OR right when offset is 0, End of Array
                continue
            if current_offset < 0:
                # Grab a rectangle of specific width and heigh, shift it left
                # by a specified offset
                # Wrap around the lost pixel data from the right
                self.__glitch_left(-current_offset)
            else:
                # Grab a rectangle of specific width and height, shift it right
                # by a specified offset
                # Wrap around the lost pixel data from the left
                self.__glitch_right(current_offset)

        if self.seed:
            # Get the same channels on the next call, we have to reset the rng seed
            # as the previous loop isn't fixed in size of iterations and depends on glitch amount
            self.__reset_rng_seed()

        if color_offset:
            # Get the next random channel we'll offset, needs to be before the random.randints
            # arguments because they will use up the original seed (if a custom seed is used)
            random_channel = self.__get_random_channel()
            # Add color channel offset if checked true
            self.__color_offset(random.randint(-doubled_glitch_amount, doubled_glitch_amount),
                                random.randint(-doubled_glitch_amount,
                                               doubled_glitch_amount),
                                random_channel)

        if scan_lines:
            # Add scan lines if checked true
            self.__add_scan_lines()

        # Creating glitched image from output array
        return Image.fromarray(self.outputarr, self.img_mode)

    def __add_scan_lines(self):
        # Make every other row have only black pixels
        # Only the R, G, and B channels are assigned 0 values
        # Alpha is left untouched (if present)
        self.outputarr[::2, :, :3] = [0, 0, 0]

    def __glitch_left(self, offset: int):
        """
         Grabs a rectange from inputarr and shifts it leftwards
         Any lost pixel data is wrapped back to the right
         Rectangle's Width and Height are determined from offset
         Consider an array like so-
         [[ 0, 1, 2, 3],
         [ 4, 5, 6, 7],
         [ 8, 9, 10, 11],
         [12, 13, 14, 15]]
         If we were to left shift the first row only, starting from the 1st index;
         i.e a rectangle of width = 3, height = 1, starting at (0, 0)
         We'd grab [1, 2, 3] and left shift it until the start of row
         so it'd look like [[1, 2, 3, 3]]
         Now we wrap around the lost values, i.e 0
         now it'd look like [[1, 2, 3, 0]]
         That's the end result!
        """
        # Setting up values that will determine the rectangle height
        start_y = random.randint(0, self.img_height)
        chunk_height = random.randint(1, int(self.img_height / 4))
        chunk_height = min(chunk_height, self.img_height - start_y)
        stop_y = start_y + chunk_height

        # For copy
        start_x = offset
        # For paste
        stop_x = self.img_width - start_x

        left_chunk = self.inputarr[start_y:stop_y, start_x:]
        wrap_chunk = self.inputarr[start_y:stop_y, :start_x]
        self.outputarr[start_y:stop_y, :stop_x] = left_chunk
        self.outputarr[start_y:stop_y, stop_x:] = wrap_chunk

    def __glitch_right(self, offset: int):
        """
         Grabs a rectange from inputarr and shifts it rightwards
         Any lost pixel data is wrapped back to the left
         Rectangle's Width and Height are determined from offset
         Consider an array like so-
         [[ 0, 1, 2, 3],
         [ 4, 5, 6, 7],
         [ 8, 9, 10, 11],
         [12, 13, 14, 15]]
         If we were to right shift the first row only, starting from
         the 0th index;
         i.e a rectangle of width = 3, height = 1 starting at (0, 0)
         We'd grab [0, 1, 2] and right shift it until the end of row
         so it'd look like [[0, 0, 1, 2]]
         Now we wrap around the lost values, i.e 3
         now it'd look like [[3, 0, 1, 2]]
         That's the end result!
        """
        # Setting up values that will determine the rectangle height
        start_y = random.randint(0, self.img_height)
        chunk_height = random.randint(1, int(self.img_height / 4))
        chunk_height = min(chunk_height, self.img_height - start_y)
        stop_y = start_y + chunk_height

        # For copy
        stop_x = self.img_width - offset
        # For paste
        start_x = offset

        right_chunk = self.inputarr[start_y:stop_y, :stop_x]
        wrap_chunk = self.inputarr[start_y:stop_y, stop_x:]
        self.outputarr[start_y:stop_y, start_x:] = right_chunk
        self.outputarr[start_y:stop_y, :start_x] = wrap_chunk

    def __color_offset(self, offset_x: int, offset_y: int, channel_index: int):
        """
         Takes the given channel's color value from inputarr,
         starting from (0, 0)
         and puts it in the same channel's slot in outputarr,
         starting from (offset_y, offset_x)
        """
        # Make sure offset_x isn't negative in the actual algo
        offset_x = offset_x if offset_x >= 0 else self.img_width + offset_x
        offset_y = offset_y if offset_y >= 0 else self.img_height + offset_y

        # Assign values from 0th row of inputarr to offset_y th
        # row of outputarr
        # If outputarr's columns run out before inputarr's does,
        # wrap the remaining values around
        self.outputarr[offset_y,
                       offset_x:,
                       channel_index] = self.inputarr[0,
                                                      :self.img_width - offset_x,
                                                      channel_index]
        self.outputarr[offset_y,
                       :offset_x,
                       channel_index] = self.inputarr[0,
                                                      self.img_width - offset_x:,
                                                      channel_index]

        # Continue afterwards till end of outputarr
        # Make sure the width and height match for both slices
        self.outputarr[offset_y + 1:,
                       :,
                       channel_index] = self.inputarr[1:self.img_height - offset_y,
                                                      :,
                                                      channel_index]

        # Restart from 0th row of outputarr and go until the offset_y th row
        # This will assign the remaining values in inputarr to outputarr
        self.outputarr[:offset_y,
                       :,
                       channel_index] = self.inputarr[self.img_height - offset_y:,
                                                      :,
                                                      channel_index]

    def __get_random_channel(self) -> int:
        # Returns a random index from 0 to pixel_tuple_len
        # For an RGB image, a 0th index represents the RED channel

        return random.randint(0, self.pixel_tuple_len - 1)

    def __reset_rng_seed(self, offset: int = 0):
        """
        Calls random.seed() with self.seed variable
        offset is for looping and getting new positions for each iteration that cointains the
        previous one, otherwise we would get the same position on every loop and different
        results afterwards on non fixed size loops
        """
        random.seed(self.seed + offset)


def is_gif(img) -> bool:
    index = 0
    for _ in ImageSequence.Iterator(img):
        # More than one frames means image is animated
        index += 1
        if index >= 2:
            return True
    return False


def soft_glitch(src_img: Image.Image, glitch_amount: Union[int, float], seed: Optional[Union[int, float]] = None,
                     color_offset: bool = False, scan_lines: bool = False):
    glitcher = ImageGlitcher()
    return glitcher.glitch_image(src_img, glitch_amount, seed, color_offset, scan_lines)


def split_color_channels(im, offset: int):
    """
    Return an image where the color channels are horizontally offset.
    The Red and Blue color channels are horizontally offset from the Green
    channel left and right respectively.
    im: Pillow Image
    offset: distance in pixels the color channels should be offset by
    """
    bands = list(im.split())
    bands[0] = ImageChops.offset(bands[0], offset, 0)
    bands[2] = ImageChops.offset(bands[2], -offset, 0)
    merged = Image.merge(im.mode, bands)
    return merged


def shift_corruption(im, offset_mag: int, coverage: float):
    """Return an image with some rows randomly shifted left or right.
    Return an image with some pixel rows randomly shifted left or right by a
    random amount, wrapping around to the opposite side of the image.
    im: Pillow Image
    offset_mag: The greatest magnitude (in pixels) the rows will be shifted by
        in either direction.
    coverage: The fraction of total rows that will be shifted by some amount
        (0.5 = half the rows will be shifted). Note: Because the possible range
        of shifts include zero, some rows may not be shifted even with a
        coverage of 1.
    """
    corrupted = im
    line_count = int(im.size[1] * coverage)
    for ypos in random.choices(range(im.size[1]), k=line_count):
        box = (0, ypos, corrupted.size[0], ypos + 1)
        line = corrupted.crop(box)
        offset = random.randint(-offset_mag, offset_mag)
        line = ImageChops.offset(line, offset, 0)
        corrupted.paste(line, box=box)
    return corrupted


def _random_walk(length: int, max_step_length: int) -> Sequence[int]:
    """Return a list of values that rise and fall randomly."""
    output = []
    pos = 0
    for _ in range(length):
        pos += random.randint(-max_step_length, max_step_length)
        output.append(pos)
    return output


def walk_distortion(im, max_step_length: int):
    """Return an image with rows shifted according to a 1D random-walk.
    im: Pillow Image
    max_step_length: The maximum step size (in pixels) that the random walk can
        take. Essentially, the permitted "abruptness" of the distortion
    """
    waved = im
    curve = _random_walk(im.size[1], max_step_length)
    for ypos in range(im.size[1]):
        box = (0, ypos, waved.size[0], ypos + 1)
        line = waved.crop(box)
        offset = curve[ypos]
        line = ImageChops.offset(line, offset, 0)
        waved.paste(line, box=box)
    return waved


def sin_wave_distortion(im, mag: Real, freq: Real, phase: Real=0):
    """Return an image with rows shifted according to a sine curve.
    im: Pillow Image
    mag: The magnitude of the sine wave
    freq: The frequency of the sine wave
    phase: The degree by which the cycle is offset (rads)
    """
    waved = im
    for ypos in range(im.size[1]):
        box = (0, ypos, waved.size[0], ypos + 1)
        line = waved.crop(box)
        offset = int(
            mag * math.sin(2 * math.pi * freq * (ypos / im.size[1]) + phase)
        )
        line = ImageChops.offset(line, offset, 0)
        waved.paste(line, box=box)
    return waved


def swap_cells(im, rows: int, cols: int, swaps: int):
    """Return an image which rectangular cells have swapped positions.
    im: Pillow Image
    rows: The number of rows in the grid
    cols: The number of columns in the grid
    swaps: the number of pairs of cells to swap
    """
    modified = im
    grid_boxes = _get_grid_boxes(modified, rows, cols)
    chosen_boxes = random.choices(grid_boxes, k=swaps * 2)
    box_pairs = [
        (chosen_boxes[2*i], chosen_boxes[(2*i)+1])
        for i in range(int(len(chosen_boxes)/2))
    ]
    for box1, box2 in box_pairs:
        cell1 = modified.crop(box1)
        cell2 = modified.crop(box2)
        modified.paste(cell1, box2)
        modified.paste(cell2, box1)
    return modified


def make_noise_data(length: int, min: int, max: int) -> Sequence[Tuple[int, int, int]]:
    """Return a list of RGB tuples of random greyscale values.
    length: The length of the list
    min: The lowest luminosity value (out of 100)
    max: The brightest luminosity value (out of 100)
    """
    return [
        ImageColor.getrgb('hsl(0, 0%, {}%)'.format(random.randint(min, max)))
        for _ in range(length)
    ]


def _get_grid_boxes(im, rows: int, cols: int):
    """Return a list of 4-tuples for every box in a given grid of the image.
    im: Pillow image
    rows: Number of rows in the grid
    cols: Number of columns in the grid
    """
    cell_width = int(im.size[0] / cols)
    cell_height = int(im.size[1] / rows)

    grid_boxes = [
        (
            cell_x * cell_width,
            cell_y * cell_height,
            cell_x * cell_width + cell_width,
            cell_y * cell_height + cell_height
        )
        for cell_y in range(rows)
        for cell_x in range(cols)
    ]
    return grid_boxes


def swap_cells(im, rows: int, cols: int, swaps: int):
    """Return an image which rectangular cells have swapped positions.
    im: Pillow Image
    rows: The number of rows in the grid
    cols: The number of columns in the grid
    swaps: the number of pairs of cells to swap
    """
    modified = im
    grid_boxes = _get_grid_boxes(modified, rows, cols)
    chosen_boxes = random.choices(grid_boxes, k=swaps * 2)
    box_pairs = [
        (chosen_boxes[2*i], chosen_boxes[(2*i)+1])
        for i in range(int(len(chosen_boxes)/2))
    ]
    for box1, box2 in box_pairs:
        cell1 = modified.crop(box1)
        cell2 = modified.crop(box2)
        modified.paste(cell1, box2)
        modified.paste(cell2, box1)
    return modified


def add_noise_cells(im, rows: int, cols: int, cells: int):
    """Return an image with randomly placed cells of noise.
    im: Pillow Image
    rows: The number of rows in the cell grid
    cols: The number of columns in the cell grid
    cells: number of noise cells to be created
    """
    modified = im
    grid_boxes = _get_grid_boxes(modified, rows, cols)
    chosen_boxes = random.choices(grid_boxes, k=cells)
    for box in chosen_boxes:
        noise_cell = Image.new(modified.mode, (box[2]-box[0], box[3]-box[1]))
        noise_cell.putdata(
            make_noise_data(noise_cell.size[0] * noise_cell.size[1], 0, 75)
        )
        modified.paste(ImageChops.lighter(modified.crop(box), noise_cell), box)

    return modified


def add_noise_bands(im, count: int, thickness: int):
    """Return an image with randomly placed full-width bands of noise.
    im: Pillow Image
    count: The number of bands of noise
    thickness: Maximum thickness of the bands
    """
    modified = im.convert('RGBA')
    boxes = [
        (0, ypos, im.size[0], ypos + random.randint(1, thickness))
        for ypos in random.choices(range(im.size[1]), k=count)
    ]
    for box in boxes:
        noise_cell = Image.new(modified.mode, (box[2]-box[0], box[3]-box[1]))
        noise_cell.putdata(
            make_noise_data(noise_cell.size[0] * noise_cell.size[1], 0, 75)
        )
        combined_cell = ImageChops.lighter(modified.crop(box), noise_cell)
        combined_cell.putalpha(128)
        modified.alpha_composite(combined_cell, (box[0], box[1]))

    return modified.convert(im.mode)


def _get_lum(rgb: Tuple[int, int, int]) -> int:
    return int(0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2])


def _split_data(data: Sequence[Tuple[int, ...]], width: int) -> Sequence[Sequence[Tuple[int, ...]]]:
    height = int(len(data) / width)
    return [
        data[(row * width):(row * width + width)]
        for row in range(height)
    ]


def pixel_sort(im, mask_function: Callable[[int], int], reverse: bool=False):
    """Return a horizontally pixel-sorted Image based on the mask function.
    The default sorting direction is dark to light from left to right.
    Pixel-sorting algorithm from: http://satyarth.me/articles/pixel-sorting/
    im: Pillow Image
    mask_function: function that takes a pixel's luminance and returns
        255 or 0 depending on whether it should be sorted or not respectively.
    reverse: sort pixels in reverse order if True
    """
    # Create a black-and-white mask to determine which pixels will be sorted
    interval_mask = im.convert('L').point(mask_function)
    interval_mask_data = list(interval_mask.getdata())
    interval_mask_row_data = _split_data(interval_mask_data, im.size[0])

    # Go row by row, recording the starting and ending points of each
    # contiguous block of white pixels in the mask
    interval_boxes = []
    for row_index, row_data in enumerate(interval_mask_row_data):
        for pixel_index, pixel in enumerate(row_data):
            # This is the first pixel on the row and it is white -> start box
            if pixel_index == 0 and pixel == 255:
                start = (pixel_index, row_index)
                continue
            # The pixel is white and the previous pixel was black -> start box
            if pixel == 255 and row_data[pixel_index - 1] == 0:
                start = (pixel_index, row_index)
                continue
            # This is the last pixel in the row and it is white -> end box
            if pixel_index == len(row_data) - 1 and pixel == 255:
                end = (pixel_index, row_index + 1)
                interval_boxes.append((start[0], start[1], end[0], end[1]))
                continue
            # The pixel is (black) and (not the first in the row) and (the
            # previous pixel was white) -> end box
            if (pixel == 0 and pixel_index > 0 and
                    row_data[pixel_index - 1] == 255):
                end = (pixel_index, row_index + 1)
                interval_boxes.append((start[0], start[1], end[0], end[1]))
                continue

    modified = im
    for box in interval_boxes:
        # Take the pixels from each box
        cropped_interval = modified.crop(box)
        interval_data = list(cropped_interval.getdata())
        # sort them by luminance
        cropped_interval.putdata(
            sorted(interval_data, key=_get_lum, reverse=reverse)
        )
        # and paste them back onto the image!
        modified.paste(cropped_interval, box=(box[0], box[1]))

    return modified


def low_res_blocks(im, rows: int, cols: int, cells: int, factor: Real):
    """Return an image with randomly placed cells of low-resolution.
    im: Pillow Image
    rows: The number of rows in the cell grid
    cols: The number of columns in the cell grid
    cells: number of low-res cells to be created
    factor: the deresolution factor (factor 2: 8x8 -> 4x4)
    """
    modified = im
    grid_boxes = _get_grid_boxes(modified, rows, cols)
    chosen_boxes = random.choices(grid_boxes, k=cells)
    for box in chosen_boxes:
        low_res_cell = modified.crop(box)
        low_res_cell = low_res_cell.resize(
            tuple(map(lambda val: int(val / factor), low_res_cell.size)),
            Image.NEAREST
        )
        low_res_cell = low_res_cell.resize(
            tuple(map(lambda val: int(val * factor), low_res_cell.size)),
            Image.NEAREST
        )
        modified.paste(low_res_cell, (box[0], box[1]))

    return modified