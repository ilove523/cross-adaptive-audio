import unittest
import settings
import sound_file
import fitness_evaluator
import analyze


class TestFitnessEvaluator(unittest.TestCase):
    def setUp(self):
        settings.INPUT_DIRECTORY = 'test_audio'

    def test_fitness_evaluator(self):
        drums = sound_file.SoundFile('drums.wav')
        synth = sound_file.SoundFile('synth.wav')
        vocal = sound_file.SoundFile('vocal.wav')

        analyze.Analyzer.analyze_multiple([drums, synth, vocal], standardize=True)

        fitness1 = fitness_evaluator.FitnessEvaluator.evaluate(drums, drums)
        fitness2 = fitness_evaluator.FitnessEvaluator.evaluate(drums, synth)
        fitness3 = fitness_evaluator.FitnessEvaluator.evaluate(drums, vocal)
        print('fitness1', fitness1)
        print('fitness2', fitness2)
        print('fitness3', fitness3)
        self.assertAlmostEqual(fitness1, 1.0)

if __name__ == '__main__':
    unittest.main()
