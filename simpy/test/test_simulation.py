from simpy import Simulation, InterruptedException

def test_simple_process():
    def pem(ctx, result):
        while True:
            result.append(ctx.now)
            yield ctx.wait(1)

    result = []
    Simulation(pem, result).simulate(until=4)

    assert result == [0, 1, 2, 3]

def test_interrupt():
    def pem(ctx):
        try:
            yield ctx.wait(10)
            raise RuntimeError('Expected an interrupt')
        except InterruptedException:
            pass

    def root(ctx):
        process = ctx.fork(pem)
        yield ctx.wait(5)
        process.interrupt()

    Simulation(root).simulate(until=20)
