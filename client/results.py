from collections import defaultdict

class SpeedTestReport(object):

    def __init__(self, results):
        self.results = results
        self.highest_scores = defaultdict(lambda: {'score': 0,
                                                   'score_str': '',
                                                   'browsers': []})

    def record_highest_score(self, test, score, score_str, browser):
        if self.highest_scores[test]['score'] < score:
            self.highest_scores[test]['score'] = score
            self.highest_scores[test]['score_str'] = score_str
            self.highest_scores[test]['browsers'] = [browser]
        elif self.highest_scores[test]['score'] == score:
            self.highest_scores[test]['browsers'].append(browser)

    def report(self):
        s = 'Results by browser:\n\n'
        for browser, tests in self.results.iteritems():
            s += '%s\n%s\n\n' % (browser, '=' * len(browser))
            for test, results_strs in tests.iteritems():
                s += '  %s\n  %s\n\n' % (test, '-' * len(test))

                if test == 'PsychedelicBrowsing':
                    colorwheel = int(results_strs[0]['colorwheel'])
                    checkerboard = int(results_strs[0]['checkerboard'])
                    s += '  Psychedelic (colorwheel): %d rpm\n' % colorwheel
                    s += '  Hallucinogenic (checkerboard): %d rpm\n\n' % \
                        checkerboard
                    total = colorwheel + checkerboard
                    self.record_highest_score(test, total, '%d/%d rpm' %
                                              (colorwheel, checkerboard),
                                              browser)
                    continue

                score = 0
                results = map(lambda x: int(x['fps']), results_strs)
                if len(results) == 1:
                    score = results[0]
                    score_str = '%d fps' % score
                    s += '  %s\n' % score_str
                else:
                    if len(results) > 0:
                        s += '  Series:'
                        for r in results:
                            s += ' %3d' % r
                        s += '\n  Mean: %.1d\n' % (sum(results) / len(results))
                        sorted_results = results[:]
                        sorted_results.sort()
                        if len(sorted_results) % 2 == 0:
                            median = (sorted_results[len(sorted_results)/2 - 1] + sorted_results[len(sorted_results)/2]) / 2
                        else:
                            median = sorted_results[len(sorted_results)/2]
                        s += '  Median: %d\n' % median
                        score = median
                        score_str = '%d fps' % score
                    else:
                        s += '  No data.\n'
                if score:
                    self.record_highest_score(test, score, score_str, browser)
                s += '\n'
            s += '\n'
        test_list = self.highest_scores.keys()
        test_list.sort()
        s += 'Results by test:\n\n'
        for test in test_list:
            s += '%s\n%s\n\n' % (test, '=' * len(test))
            s += ' Highest median score: %s (%s)\n\n' % \
                (self.highest_scores[test]['score_str'],
                 ', '.join(self.highest_scores[test]['browsers']))
        return s


def main():
    results = {
        'firefox': {
            'fishtank': [{'fps': 34}, {'fps': 36}, {'fps': 40}, {'fps': 44}, {'fps': 42}, {'fps': 43}, {'fps': 44}, {'fps': 43}, {'fps': 42}, {'fps': 44}, {'fps': 43}, {'fps': 42}],
            'SantasWorkshop': [{'fps': 10}, {'fps': 7}, {'fps': 4}, {'fps': 3}, {'fps': 3}, {'fps': 3}, {'fps': 3}, {'fps': 3}],
            'PsychedelicBrowsing': [{'colorwheel': 1944, 'checkerboard': 966}]
         },
         'safari': {
            'fishtank': [{'fps': 10}, {'fps': 9}, {'fps': 8}, {'fps': 7}, {'fps': 6}, {'fps': 6}, {'fps': 6}, {'fps': 6}],
            'SantasWorkshop': [{'fps': 3}, {'fps': 3}, {'fps': 3}, {'fps': 3}, {'fps': 3}, {'fps': 3}, {'fps': 3}],
            'PsychedelicBrowsing': [{'colorwheel': 1820, 'checkerboard': 840}]
         }
    }
    report = SpeedTestReport(results)
    print report.report()

if __name__ == '__main__':
    main()
