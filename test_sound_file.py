from __future__ import absolute_import
import unittest
import settings
import sound_file
import analyze


class TestSoundFile(unittest.TestCase):
    def setUp(self):
        settings.INPUT_DIRECTORY = 'test_audio'

    def test_sound_file(self):
        my_sound_file = sound_file.SoundFile('drums.wav')
        self.assertEqual(my_sound_file.get_md5(), '1fce4b6c64a5c8c6a416928e60d4f686')
        self.assertAlmostEqual(my_sound_file.get_duration(), 7.89278911565)

        analyze.Analyzer.analyze_multiple([my_sound_file], standardize=True)

        feature_vector_0 = my_sound_file.get_standardized_neural_input_vector(0)
        self.assertEqual(len(feature_vector_0), len(settings.NEURAL_INPUT_CHANNELS))
        feature_vector_1 = my_sound_file.get_standardized_neural_input_vector(1)
        self.assertNotEqual(feature_vector_0, feature_vector_1)

if __name__ == '__main__':
    unittest.main()
