import argparse
import time
import template_handler
import csound_handler


class Main(object):
    def __init__(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '-i',
            '--input',
            dest='input_filename',
            type=str,
            help='The name of the input file',
            required=True
        )
        arg_parser.add_argument(
            '--print-execution-time',
            nargs='?',
            dest='print_execution_time',
            help='At the end of the run, print the execution time',
            const=True,
            required=False,
            default=False
        )
        self.args = arg_parser.parse_args()

        if self.args.print_execution_time:
            self.start_time = time.time()

        self.run()

        if self.args.print_execution_time:
            print "execution time: %s seconds" % (time.time() - self.start_time)

    def run(self):
        template = template_handler.TemplateHandler('templates/analyzer.csd.jinja2')
        template.compile(filename=self.args.input_filename, krate=441)
        csd_path = 'csd/analyzer.csd'
        template.write_result(csd_path)
        csound = csound_handler.CsoundHandler(csd_path)
        csound.run()

if __name__ == '__main__':
    Main()