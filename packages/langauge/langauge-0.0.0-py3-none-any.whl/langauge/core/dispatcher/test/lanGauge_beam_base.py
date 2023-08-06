#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# pytype: skip-file

from __future__ import absolute_import

import argparse
import logging

import apache_beam as beam
import torch
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from transformers import AutoTokenizer, AutoModelForTokenClassification


class Tokenize(beam.DoFn):

    def __init__(self, modelName):
        self.tokenizer = None
        self.modelName = modelName

    def setup(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.modelName)

    def process(self, sequence):
        input_ids = torch.tensor(self.tokenizer.encode(sequence)).unsqueeze(0)
        yield {'tokens': self.tokenizer.tokenize(sequence), 'inputs': input_ids}
        # tokens = self.tokenizer.tokenize(sequence)
        # inputs = self.tokenizer.encode(sequence, return_tensors="pt")
        # yield {'tokens': tokens, 'inputs': inputs}


# loads the pretrained model which is then used for predicting values
# can read more about it here: https://github.com/huggingface/transformers
class Predict(beam.DoFn):
    def __init__(self, modelName):
        self.model = None
        self.modelName = modelName

    def setup(self):
        self.model = AutoModelForTokenClassification.from_pretrained(self.modelName)

    def process(self, inputs):
        with torch.no_grad():
            outputs = self.model(inputs['inputs'])
        predictions = outputs[0].argmax(axis=-1)[0][1:-1]
        for token, pred in zip(inputs['tokens'], predictions):
            yield {'token': token, 'prediction': self.model.config.id2label[pred.numpy().item()]}
        # outputs = self.model(inputs['inputs'])[0]
        # predictions = torch.argmax(outputs, dim=2)
        # for token, prediction in zip(inputs['tokens'], predictions[0].numpy()):
        #     yield {'token': token, 'prediction': prediction}


def run(modelName, source, sink, beam_options=None):
    with beam.Pipeline(options=beam_options) as p:
        _ = (p
             | 'Read file' >> source
             | 'Split' >> beam.Map(lambda text: text.split('\t')[0])
             | 'Tokenize' >> beam.ParDo(Tokenize(modelName))
             | 'Predict' >> beam.ParDo(Predict(modelName))
             #  | "print" >> task.Map(print)
             # | 'Format as JSON' >> task.Map(json.dumps)
             | 'Write predictions' >> sink
             )


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--input',
        dest='input',
        # default='/home/subham/PycharmProjects/LanGauge-INTERNAL/data/dev/two.txt',
        default='/home/subham/PycharmProjects/LanGauge-INTERNAL/data/dev/one.txt',
        help='Input file to process.')
    parser.add_argument(
        '--output',
        dest='output',
        default='/home/subham/PycharmProjects/LanGauge-INTERNAL/out.txt',
        help='Output file to write results to.')
    parser.add_argument(
        '--modelName',
        dest='modelName',
        # default='allenai/scibert_scivocab_uncased',
        # default='microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract',
        # default='fran-martinez/scibert_scivocab_cased_ner_jnlpba',
        default='/home/subham/Downloads/ner_trained_models/pubMedBERT_model_BC5CDR_chem',
        help='Model Name for prediction')
    args, pipeline_args = parser.parse_known_args()

    pipeline_args.extend([
        "--runner=PortableRunner",
        "--job_endpoint=localhost:8099",
        # "--runner=FlinkRunner",
        # "--flink_master=localhost:8081",
        # User code is executed within the same process that submitted the dispatcher.
        # This option is useful for local testing. However, it is not suitable for a
        # production environment, as it performs work on the machine the job originated from.
        "--environment_type=LOOPBACK"
        # "--environment_type=DOCKER"
    ])
    print(pipeline_args)
    beam_options = PipelineOptions(pipeline_args)
    beam_options.view_as(SetupOptions).save_main_session = True
    source = beam.io.ReadFromText(args.input)
    sink = beam.io.WriteToText(args.output)
    # [START predict_call_run]
    run(
        args.modelName,
        source,
        sink,
        beam_options)
    # [END predict_call_run]
