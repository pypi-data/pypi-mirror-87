# Fonetika
Russian, English, Sweden, Estonian and Finnish Phonetic algorithm based on Soundex/Metaphone.

Package has both implemented phoneme transformation into letter-number sequence and distance engine for comparison of phonetic sequences (based on Levenstein and Hamming distances).

Furthermore, both Russian phonetic algorithms supports preprocessing for specific phoneme cases.

### Quick start
1. Install this package via ```pip```

```python
pip install fonetika
```

2. Import Soundex algorithm.

Package supports a lot of opportunities, it's possible to cut a result sequence (like in the original Soundex version) or also code vowels.

```python
from fonetika.soundex import RussianSoundex

soundex = RussianSoundex(delete_first_letter=True)
soundex.transform('ёлочка')
...

J070530

soundex = RussianSoundex(delete_first_letter=True, code_vowels=True)
soundex.transform('ёлочка')
...

JA7A53A
```

> A structure of the library is scalable, `RussianSoundex` class inherits basic class `Soundex` (original for English language). In order to extend our algorithm, you need just inherit own class from `Soundex` and override methods.

3. Import Soundex distance for usage of string comparision

```python
from fonetika.distance import PhoneticsInnerLanguageDistance

soundex = RussianSoundex(delete_first_letter=True)
phon_distance = PhoneticsInnerLanguageDistance(soundex)
phon_distance.distance('ёлочка', 'йолочка')
...

0
```

4. You can also calculate distance between words of two languages. It would be useful for working with one language family group.

```python
from fonetika.distance import PhoneticsBetweenLanguagesDistance

m1 = FinnishMetaphone(reduce_word=False)
m2 = EstonianMetaphone(reduce_word=False)
phon_distance = PhoneticsBetweenLanguagesDistance(m1, m2)
phon_distance.distance('yö', 'öö')
...

1
```
