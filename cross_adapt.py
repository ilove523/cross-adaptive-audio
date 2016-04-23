from __future__ import absolute_import
from __future__ import print_function
import template_handler
import csound_handler
import os
import settings
import sound_file
import logger
import hashlib
import json
import neural_output


class CrossAdapter(object):
    @staticmethod
    def cross_adapt(param_sound, input_sound, parameter_vectors, generation):
        channels = zip(*parameter_vectors)
        data_md5 = hashlib.md5(json.dumps(channels)).hexdigest()

        data_file_path = os.path.join(
            settings.NEURAL_OUTPUT_DIRECTORY,
            param_sound.filename + '.neural_output.gen{0:04d}.{1}.json'.format(generation, data_md5)
        )
        l = logger.Logger(data_file_path, features_to_add=None, suppress_initialization=True)
        l.data = channels
        l.write()
        that_neural_output = neural_output.NeuralOutput(data_file_path, channels)

        template = template_handler.TemplateHandler('templates/dist_lpf.csd.jinja2')
        template.compile(
            input_sound_filename=input_sound.filename,
            data_file_path=data_file_path,
            ksmps=settings.CSOUND_KSMPS,
            duration=input_sound.get_duration()
        )

        csd_path = os.path.join(settings.CSD_DIRECTORY, 'cross_adapt.csd')
        template.write_result(csd_path)
        csound = csound_handler.CsoundHandler(csd_path)
        output_filename = input_sound.filename + '.cross_adapted.gen{0:04d}.{1}.wav'.format(generation, data_md5)
        csound.run(output_filename, async=False)
        output_sound_file = sound_file.SoundFile(output_filename, is_input=False)
        return output_sound_file, that_neural_output
