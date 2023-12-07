from wordcloud.wordcloud import *
import jieba

def sample_position(integral_image, size_x, size_y, center: tuple):
    cx, cy = center
    x = integral_image.shape[0]
    y = integral_image.shape[1]
    def area_avilable(i, j):
        for p in (i, j, i+size_x, j+size_y):
            if i < 0 or j < 0 or i+size_x>x-1 or j+size_y>y-1:
                return False
        area = integral_image[i, j] + integral_image[i + size_x, j + size_y]
        area -= integral_image[i + size_x, j] + integral_image[i, j + size_y]
        if not area:
            return True
    for r in range(max(x-cx, cx, y-cy, cy)):
        for j in (cy+r, cy-r):
            if j < 0 or j > y:
                continue
            for i in range(cx-r, cx+r):
                if i < 0 or i > x:
                    continue
                if area_avilable(i, j):
                    return i, j
        for i in (cx+r, cx-r):
            if i < 0 or i > x:
                continue
            for j in range(cy-r, cy+r):
                if j < 0 or j > y:
                    continue
                if area_avilable(i, j):
                    return i, j
    

class WC(WordCloud):
    
    def process_text(self, text: str):
        words = jieba.cut(text)
        if self.stopwords:
            words = [w for w in words if w not in self.stopwords]
        freqs = [(w, 1) for w in words]
        return freqs
        
        
    
    def generate_from_frequencies(self, frequencies, max_font_size=None):  # noqa: C901
        """Create a word_cloud from words and frequencies.

        Parameters
        ----------
        frequencies : list of 2-element list like [["word": 12]]
            A contains words and associated frequency.

        max_font_size : int
            Use this font-size instead of self.max_font_size

        Returns
        -------
        self

        """
        # make sure frequencies are sorted and normalized
        # frequencies = sorted(frequencies.items(), key=lambda x:x[1], reverse=True)
        if len(frequencies) <= 0:
            raise ValueError("We need at least 1 word to plot a word cloud, "
                             "got %d." % len(frequencies))
        print(type(frequencies))
        frequencies = frequencies[:self.max_words]

        # largest entry will be 1
        max_frequency = float(frequencies[0][1])

        frequencies = [(word, freq / max_frequency)
                       for word, freq in frequencies]

        if self.random_state is not None:
            random_state = self.random_state
        else:
            random_state = Random()

        if self.mask is not None:
            boolean_mask = self._get_bolean_mask(self.mask)
            width = self.mask.shape[1]
            height = self.mask.shape[0]
        else:
            boolean_mask = None
            height, width = self.height, self.width
        occupancy = IntegralOccupancyMap(height, width, boolean_mask)

        # create image
        img_grey = Image.new("L", (width, height))
        draw = ImageDraw.Draw(img_grey)
        img_array = np.asarray(img_grey)
        font_sizes, positions, orientations, colors = [], [], [], []

        last_freq = 1.

        if max_font_size is None:
            # if not provided use default font_size
            max_font_size = self.max_font_size

        if max_font_size is None:
            # figure out a good font size by trying to draw with
            # just the first two words
            if len(frequencies) == 1:
                # we only have one word. We make it big!
                font_size = self.height
            else:
                fqs = sorted(frequencies, key=lambda x:x[1], reverse=True)
                self.generate_from_frequencies(fqs[:20],
                                               max_font_size=self.height)
                # find font sizes
                sizes = [x[1] for x in self.layout_]
                try:
                    font_size = int(2 * sizes[0] * sizes[1]
                                    / (sizes[0] + sizes[1]))
                # quick fix for if self.layout_ contains less than 2 values
                # on very small images it can be empty
                except IndexError:
                    try:
                        font_size = sizes[0]
                    except IndexError:
                        raise ValueError(
                            "Couldn't find space to draw. Either the Canvas size"
                            " is too small or too much of the image is masked "
                            "out.")
        else:
            font_size = max_font_size

        # we set self.words_ here because we called generate_from_frequencies
        # above... hurray for good design?
        self.words_ = dict(frequencies)

        if self.repeat and len(frequencies) < self.max_words:
            # pad frequencies with repeating words.
            times_extend = int(np.ceil(self.max_words / len(frequencies))) - 1
            # get smallest frequency
            frequencies_org = list(frequencies)
            downweight = frequencies[-1][1]
            for i in range(times_extend):
                frequencies.extend([(word, freq * downweight ** (i + 1))
                                    for word, freq in frequencies_org])

        # start drawing grey image
        pre_position = (random_state.randint(1, height), random_state.randint(1, width))
        for word, freq in frequencies:
            if freq == 0:
                continue
            # select the font size
            rs = self.relative_scaling
            if rs != 0:
                font_size = int(round((rs * (freq / float(last_freq))
                                       + (1 - rs)) * font_size))
            if random_state.random() < self.prefer_horizontal:
                orientation = None
            else:
                orientation = Image.ROTATE_90
            tried_other_orientation = False
            
            while True:
                if font_size < self.min_font_size:
                    # font-size went too small
                    break
                # try to find a position
                font = ImageFont.truetype(self.font_path, font_size)
                # transpose font optionally
                transposed_font = ImageFont.TransposedFont(
                    font, orientation=orientation)
                # get size of resulting text
                box_size = draw.textbbox((0, 0), word, font=transposed_font, anchor="lt")
                # find possible places using integral image:
                result = sample_position(occupancy.integral,box_size[3] + self.margin,
                                                   box_size[2] + self.margin,
                                                   pre_position)
                if result is not None:
                    # Found a place
                    break
                # if we didn't find a place, make font smaller
                # but first try to rotate!
                if not tried_other_orientation and self.prefer_horizontal < 1:
                    orientation = (Image.ROTATE_90 if orientation is None else
                                   Image.ROTATE_90)
                    tried_other_orientation = True
                else:
                    font_size -= self.font_step
                    orientation = None

            if font_size < self.min_font_size:
                # we were unable to draw any more
                break

            x, y = np.array(result) + self.margin // 2
            pre_position = result
            # actually draw the text
            draw.text((y, x), word, fill="white", font=transposed_font)
            positions.append((x, y))
            orientations.append(orientation)
            font_sizes.append(font_size)
            colors.append(self.color_func(word, font_size=font_size,
                                          position=(x, y),
                                          orientation=orientation,
                                          random_state=random_state,
                                          font_path=self.font_path))
            # recompute integral image
            if self.mask is None:
                img_array = np.asarray(img_grey)
            else:
                img_array = np.asarray(img_grey) + boolean_mask
            # recompute bottom right
            # the order of the cumsum's is important for speed ?!
            occupancy.update(img_array, x, y)
            last_freq = freq

        self.layout_ = list(zip(frequencies, font_sizes, positions,
                                orientations, colors))
        return self