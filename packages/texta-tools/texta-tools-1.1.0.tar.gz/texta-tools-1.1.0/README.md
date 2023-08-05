# TEXTA Tools Python Package

* Text Processor
* Embedding & Phraser
* MLP Analyzer

## Using TikaOCR with different languages
1. Install language packs: [https://cwiki.apache.org/confluence/display/tika/TikaOCR](https://cwiki.apache.org/confluence/display/tika/TikaOCR)
2. Override the configured language with your request:

    ``` python
    res = parser.from_file("yourfile.png", requestOptions={"headers": {"X-Tika-OCRLanguage": "est+eng+rus"}})
    ```
