from ..logger import log


class TestSet:
    def __init__(self, cases):
        self.cases = []
        for actual, expect in cases:
            self.cases.append(TestCase(actual, expect))

    def __iter__(self):
        return self.cases.__iter__()

    def __len__(self):
        return len(self.cases)


class TestCase:
    def __init__(self, text, expect):
        self.text = text
        self.expect = expect
        self.actual = None
        self.result = None
        self.done = False

    def run(self, module):
        self.actual = module.query(self.text).text
        if self.actual == self.expect:
            self.result = True
        else:
            self.result = False
        self.done = True

    def __str__(self):
        if self.done:
            if self.result:
                return 'passed, case: {}, expect: {}, actual: {}'.format(self.text, self.expect, self.actual)
            return 'failed, case: {}, expect: {}, actual: {}'.format(self.text, self.expect, self.actual)
        return 'case: {}, expect: {}'.format(self.text, self.expect)


class TestResult:
    def __init__(self, testset):
        self.testset = testset
        self.total = len(testset)
        self.wrong_cases = list(filter(lambda c: not c.result, self.testset))
        self.correct = self.total - len(self.wrong_cases)

    def show(self):
        log.info('report start')
        log.info('total: {}'.format(self.total))
        log.info('correct: {}'.format(self.correct))
        log.info('accuracy: {}'.format(self.correct / self.total))
        for case in self.wrong_cases:
            log.info(case)
        log.info('report end')
        log.info('-' * 20)


class TestRunner:
    def __init__(self, testset, module):
        self.testset = testset
        self.module = module
        self.result = None

    def run(self):
        for case in self.testset:
            case.run(self.module)

        return TestResult(self.testset)
