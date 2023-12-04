import jieba
from operator import itemgetter
from wordcloud import WordCloud

class WordVideo:
    def __init__(self) -> None:
        pass

    def _tosentence(self, text):
        splitors = '。，！？；'
        sentences = ''
        for w in text:
            if w in splitors:
                sentences += '\n'
            else:
                sentences += w
        sentences = sentences.replace('\n\n', '\n')
        return sentences.split('\n')


    def process_text(self, text: str):
        """Splits a long text into words, eliminates the stopwords.

        Parameters
        ----------
        text : string
            The text to be processed.

        Returns
        -------
        sentences : dict (string, int)
            Word tokens with associated frequency.

        Notes
        -----
        There are better ways to do word tokenization, but I don't want to
        include all those things.
        """
        sentences = []
        frequencies = {}
        for s in self._tosentence(text):
            s = s.strip()
            if not s:
                continue
            ws = jieba.cut(s)
            for w in ws:
                frequencies[w] = 1 + frequencies.get(w, 0)
            sentence = {
                'words': ws,
                'text': s,
            }
            sentences.append(sentence)
        return sentences, frequencies
    
    def baidu_tts_api(self, sentences: list):
        '''Generate fake data'''
        word_dur = 2100/13
        sent_timestampe = []
        rtn = {
            "tasks_info": [{
                "task_status": "Success",
                "task_result": {
                     "speech_url": '',
                     "speech_timestamp": {
                         "sentences": sent_timestampe
                     }
                },

            }],
        }
        begin_time = 0
        end_time = 0
        for i,s in enumerate(sentences):
            begin_time = end_time
            characters = []

            for j,c in enumerate(s):
                characters.append({
                    "character_text": c,
                    "begin_time": begin_time + j * word_dur,
                    "end_time": begin_time + (j+1) * word_dur,
                })
            end_time = characters[-1]['end_time']
            sent_timestampe.append({
                "sentence_texts": s['text'],
                "end_time": end_time,
                "begin_time": begin_time,
                "characters": characters,
            })
        return rtn

    def baidu_tts(self, sentences: list):
        #TODU: 目前是假装的
        aodio_info = self.baidu_tts_api(sentences)
        



    
    def to_audio(self, sentences: list):
        '''
        sentences: list of sentence object
        '''
        
        
        word_dur = 2100/13

        for s in sentences:
            dur = len(s['text']) * word_dur


            
        

def positions(sentences, max_words=200):
    counts = {}
    frequencies = [] 
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        ws = list(jieba.cut(s))
        for w in ws:
            counts[w] = 1 + counts.get(w, 0)
        frequencies.append(ws)
    # make sure frequencies are sorted and normalized
    frequencies = sorted(frequencies.items(), key=itemgetter(1), reverse=True)
    if len(frequencies) <= 0:
        raise ValueError("We need at least 1 word to plot a word cloud, "
                            "got %d." % len(frequencies))
    frequencies = frequencies[:self.max_words]

    # largest entry will be 1
    max_frequency = float(frequencies[0][1])

    frequencies = [(word, freq / max_frequency)
                    for word, freq in frequencies]
    


