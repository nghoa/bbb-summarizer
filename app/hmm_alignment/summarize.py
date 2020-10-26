import sys
import os
from multiprocessing import Pool
import math
import argparse
import copy
import itertools
import numpy as np
import json

from Logger import Logger
from util import print_table, files_in_dir
from SummaryCreator import SummaryCreator
from ArticleDataSample import ArticleDataSample
from HmmArticle import HmmArticle, HmmArticleConfig, PredictedSeqInfoKey

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class npEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int32):
            return int(obj)
        return json.JSONEncoder.default(self, obj)

def summarize(args):
    col_order = PredictedSeqInfoKey.get_columns_order()
    failed_articles = []

    articles_folder = os.path.join(args.data_folder, "presentation_text")
    transcript_folder = os.path.join(args.data_folder, "transcript")
    sections_info_folder = os.path.join(args.data_folder, "sections_info")
    section_per_sent_folder = os.path.join(args.data_folder, "section_per_sent")

    article_names = args.article_names
    print("number of articles: {}".format(len(article_names)))

    predict_enable = not args.no_predict
    # log only if we are in predict mode
    logging_enable = predict_enable

    for article_i, article_name in enumerate(article_names):
        if logging_enable:
            # set up log file for current article
            log_filename = os.path.join(args.log_folder, article_name)
            if os.path.isfile(log_filename):
                raise Exception("log file already exists: {}".format(log_filename))

            logger = Logger(log_filename)
            sys.stdout = sys.stderr = logger
            print("Logging to file: {}\n".format(log_filename))

        print("--- paper {}: {}\n".format(article_i, article_name))

        article_fname = os.path.join(articles_folder, article_name)
        transcript_fname = os.path.join(transcript_folder, article_name)
        sections_info_fname = os.path.join(sections_info_folder, article_name)
        section_per_sent_fname = os.path.join(section_per_sent_folder, article_name)

        # remove the ".txt" extension and add numpy extension
        similarity_fname = article_name[:-4] + '.npy'
        similarity_fname = os.path.join(args.similarity_folder, similarity_fname)

        try:
            article_data_sample = ArticleDataSample(transcript_fname,
                                                    article_fname,
                                                    sections_info_fname,
                                                    section_per_sent_fname)

            # prepare configuration
            cfg = HmmArticleConfig(args.word_embed_path, labeled_data_mode=False)
            cfg.similarity_fname = similarity_fname

            cfg.print_configuration()
            print("")

            durations_folder = os.path.join(args.base_summaries_folder, "durations")
            if not os.path.exists(durations_folder):
                os.makedirs(durations_folder, mode=0o775, exist_ok=True)
            durations_fname = os.path.join(durations_folder, article_name)

            alignment_folder = os.path.join(args.base_summaries_folder, "alignment")
            if not os.path.exists(alignment_folder):
                os.makedirs(alignment_folder, mode=0o775, exist_ok=True)
            alignment_fname = os.path.join(alignment_folder, article_name)

            # Output json alignment for further processessing
            json_article_name = article_name.split('.')[0] + '.json'
            json_alignment = os.path.join(alignment_folder, json_article_name)

            top_scored_sents_folder = os.path.join(args.base_summaries_folder,
                                                   "top_scored_sents.num_sents_{}_thresh_{}".format(args.num_sents,
                                                                                                    args.thresh))
            
            if not os.path.exists(top_scored_sents_folder):
                os.makedirs(top_scored_sents_folder, mode=0o775, exist_ok=True)

            top_scored_sents_fname = os.path.join(top_scored_sents_folder, article_name)

            if predict_enable:
                hmm_article = HmmArticle(article_data_sample, cfg)

                predicted_seq_info, log_prob = hmm_article.predict()

                print('predicted_seq_info: ')
                print(predicted_seq_info)

                print("log_prob = {}".format(log_prob))

                print("predicted sequence info:\n")
                alignment_str = print_table(predicted_seq_info, col_order)

                with open(alignment_fname, 'w', encoding='utf-8') as out_file:
                    out_file.write(alignment_str + "\n")

                # TODO: prototype Error Output:  0 is not JSON serializable
                with open(json_alignment, 'w', encoding='utf-8') as f:
                    json.dump(predicted_seq_info, f, ensure_ascii=False, indent=4, cls=npEncoder)              

                print("\n")

                hmm_article.create_durations_file(durations_fname)

            summary_creator = SummaryCreator(article_data_sample,
                                             durations_fname=durations_fname)

            if os.path.isfile(top_scored_sents_fname):
                print("file exists: {}".format(top_scored_sents_fname))
            else:
                summary_creator.create_top_scored_sents_file(args.num_sents,
                                                             args.thresh,
                                                             top_scored_sents_fname)

            if predict_enable:
                warnings = hmm_article.get_warnings()
                if len(warnings) > 0:
                    for warning in warnings:
                        print("- {}".format(warning))

        except Exception as ex:
            print("EXCEPTION WAS CAUGHT FOR PAPER: {}".format(article_name))
            print(ex)
            failed_articles.append(article_name)

    return failed_articles


def main(args):
    predict_enable = not args.no_predict

    if not os.path.exists(args.out_folder):
        os.makedirs(args.out_folder, mode=0o775, exist_ok=True)

    # take the basename and remove the extension
    word_embed_description = os.path.basename(args.word_embed_path)[:-4]

    args.base_summaries_folder = os.path.join(args.out_folder, "output")
    if not os.path.exists(args.base_summaries_folder):
        os.makedirs(args.base_summaries_folder, mode=0o775, exist_ok=(not predict_enable))

    args.similarity_folder = os.path.join(args.out_folder, "similarity")
    if not os.path.exists(args.similarity_folder):
        os.makedirs(args.similarity_folder, mode=0o775, exist_ok=True)

    args.log_folder = os.path.join(args.base_summaries_folder, "log")
    if not os.path.exists(args.log_folder):
        os.makedirs(args.log_folder, mode=0o775, exist_ok=(not predict_enable))

    article_names = files_in_dir(os.path.join(args.data_folder, "transcript"))

    num_processors = args.num_processors
    print("num_processors: {}".format(num_processors))

    if args.num_processors > 1:  # multiprocessing
        num_articles = len(article_names)
        papers_per_process = math.ceil(num_articles / num_processors)
        args_list = [copy.copy(args) for _ in range(num_processors)]
        for i in range(num_processors):
            args_list[i].article_names = article_names[i*papers_per_process: (i+1)*papers_per_process]

        p = Pool(num_processors)
        failed_lists = p.map(summarize, args_list)

        # list of lists -> one list
        failed_list = list(itertools.chain.from_iterable(failed_lists))

    else:  # run on single processor
        args.article_names = article_names
        failed_list = summarize(args)

    num_failed = len(failed_list)
    if num_failed > 0:
        print("FAILED ARTICLES ({}):".format(num_failed))
        for article_name in failed_list:
            print(article_name)

''' 
Namespace(data_folder='example', no_predict=False, num_processors=1, num_sents=30, out_folder='example/output', thresh=1, word_embed_path='glove.6B/glove.6B.300d.txt')
'''

if __name__ == '__main__':
    args = Namespace(
        data_folder='data',
        no_predict=False,
        num_processors = 1,
        num_sents = 30,
        out_folder = 'data/results',
        thresh = 1,
        word_embed_path='glove.6B/glove.6B.300d.txt'
    )

    main(args)
