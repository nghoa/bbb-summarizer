# BBB Summarizer
Follow the below instruction for setup

## Installation
- Start by creating a python virtual environment: `python3 -m venv <name of venv>`
- Activate virtual environment: `source /<name of venv>/bin/activate`
- Before installing the packages, upgrade pip first: `pip install --upgrade pip`
- Install python packages: `pip install -r requirements.txt`
- Install additional dependencies: `./install.sh`
- Start server with:  `. entrypoint.sh`

<<<<<<< HEAD
### Reference:
- https://github.com/jiaaro/pydub/issues/184
### Install ffmpeg
- https://github.com/jiaaro/pydub#dependencies

### Download Glove.6B
Download Glove.6B and put it into the following directory: `/app/hmm_alignment/glove.6B`
Step by Step:
1. Starting from the base directory: `cd /app/hmm_alignment/glove.6B`
2. Download glove: `wget http://nlp.stanford.edu/data/glove.6B.zip`
3. Unzip it & move `glove.6B.300d.txt` in the base dir of `glove.6B`

### HMM Alignment
- Reference: `https://github.com/levguy/talksumm`
@inproceedings{lev-etal-2019-talksumm,
    title = "{T}alk{S}umm: A Dataset and Scalable Annotation Method for Scientific Paper Summarization Based on Conference Talks",
    author = "Lev, Guy  and
      Shmueli-Scheuer, Michal  and
      Herzig, Jonathan  and
      Jerbi, Achiya  and
      Konopnicki, David",
    booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P19-1204",
    pages = "2125--2131",
    abstract = "Currently, no large-scale training data is available for the task of scientific paper summarization. In this paper, we propose a novel method that automatically generates summaries for scientific papers, by utilizing videos of talks at scientific conferences. We hypothesize that such talks constitute a coherent and concise description of the papers{'} content, and can form the basis for good summaries. We collected 1716 papers and their corresponding videos, and created a dataset of paper summaries. A model trained on this dataset achieves similar performance as models trained on a dataset of summaries created manually. In addition, we validated the quality of our summaries by human experts.",
}
=======
# Reference:
- https://github.com/jiaaro/pydub/issues/184
# Install ffmpeg
- https://github.com/jiaaro/pydub#dependencies
>>>>>>> c0d0e473154025293f467780255fffe69ddd7c63
